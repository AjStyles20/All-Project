"""Speech arbitration methods B0–B4 (Pass 003).

Input is one utterance with its context; output is a ruling in one of six states. No method
sanctions anyone: rulings are notices for a human arbiter, and the platform never ends or
forfeits a game on its own.

Text stands in for speech-to-text output; `normalise` absorbs common recognition errors
("night" for knight, "f six" for f6).
"""
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum

from p010.chess import FILES, Board, square


class Ruling(str, Enum):
    NO_VIOLATION = "NO VIOLATION"
    CONDUCT_WARNING = "CONDUCT WARNING"
    POSSIBLE_RULE_VIOLATION = "POSSIBLE RULE VIOLATION"
    HIGH_CONFIDENCE_VIOLATION = "HIGH-CONFIDENCE VIOLATION"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT EVIDENCE"
    ESCALATE = "ESCALATE / HUMAN REVIEW"


PENALTIES = {Ruling.CONDUCT_WARNING, Ruling.POSSIBLE_RULE_VIOLATION, Ruling.HIGH_CONFIDENCE_VIOLATION, Ruling.ESCALATE}


class Contract(str, Enum):
    STRICT = "STRICT"          # rated play: no help, no position talk aimed at the opponent
    SOCIAL = "SOCIAL"          # casual: players may chat about the game; outside help still banned
    OPEN = "OPEN"              # anything goes except abuse
    TRAINING = "TRAINING"      # coaching and analysis welcome


class Role(str, Enum):
    PLAYER = "PLAYER"
    SPECTATOR = "SPECTATOR"
    UNKNOWN = "UNKNOWN"        # speaker could not be identified


class Phase(str, Enum):
    PRE = "PRE"
    DURING = "DURING"
    POST = "POST"


@dataclass(frozen=True)
class Utterance:
    text: str
    role: Role
    phase: Phase
    fen: str
    contract: Contract
    previous: str = ""


@dataclass
class Decision:
    ruling: Ruling
    evidence: list = field(default_factory=list)


# ---------- text understanding ----------

NUMBER_WORDS = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8"}
SOUNDALIKES = {"night": "knight", "nite": "knight", "horse": "knight", "rock": "rook", "castle": "rook",
               "bish": "bishop", "porn": "pawn", "prawn": "pawn", "queeen": "queen"}
PIECE_WORDS = {"knight": "N", "bishop": "B", "rook": "R", "queen": "Q", "king": "K", "pawn": "P"}

ABUSE = ("idiot", "stupid", "moron", "trash", "garbage", "loser", "pathetic", "dumb", "useless", "clown")
THREATS = ("know where you live", "find you", "hurt you", "kill you", "come for you", "make you pay")
FIRST_PERSON = re.compile(r"\b(my|mine|i|i'm|im|me)\b")
ADDRESSED = re.compile(r"\b(you|your|you're|youre)\b")


def normalise(text: str) -> str:
    t = text.lower()
    t = re.sub(r"[^a-z0-9#+=' ]", " ", t)
    words = []
    for w in t.split():
        words.append(SOUNDALIKES.get(w, NUMBER_WORDS.get(w, w)))
    t = " ".join(words)
    # "f 6" -> "f6" (speech often splits the square)
    return re.sub(r"\b([a-h]) ([1-8])\b", r"\1\2", t)


def mentions(text: str) -> list[tuple[str | None, str]]:
    """Move-like mentions as (piece letter or None, target square)."""
    t = normalise(text)
    found = []
    for m in re.finditer(r"\b(?:([nbrqk])x?([a-h][1-8]))\b", t):          # SAN-ish: nf6, bxe5
        found.append((m.group(1).upper(), m.group(2)))
    for m in re.finditer(r"\b(knight|bishop|rook|queen|king|pawn)(?: (?:to|on|takes|x|on to|into))?(?: on)? ([a-h][1-8])\b", t):
        found.append((PIECE_WORDS[m.group(1)], m.group(2)))
    for m in re.finditer(r"\b(?:take|takes|capture|captures|push|go|play|move) (?:on |to )?([a-h][1-8])\b", t):
        found.append((None, m.group(1)))
    for m in re.finditer(r"(?<![a-z])([a-h][1-8])(?![a-z0-9])", t):
        if not any(m.group(1) == sq for _, sq in found):
            found.append((None, m.group(1)))
    return found


def resolve(board: Board, found) -> list:
    """Legal moves for the side to move that a mention could mean."""
    moves = board.legal_moves()
    out = []
    for piece, target in found:
        to = square(target)
        for m in moves:
            p = board.squares[m.frm].upper()
            if m.to == to and (piece is None or piece == p):
                out.append(m)
    return out


def _has(text, words):
    t = normalise(text)
    return any(re.search(r"\b" + re.escape(w) + r"\b", t) for w in words)


# ---------- B0: keyword list ----------

def b0_keywords(u: Utterance) -> Decision:
    if _has(u.text, THREATS):
        return Decision(Ruling.ESCALATE, ["threat phrase"])
    if _has(u.text, ABUSE):
        return Decision(Ruling.CONDUCT_WARNING, ["abusive word"])
    if mentions(u.text):
        return Decision(Ruling.HIGH_CONFIDENCE_VIOLATION, ["names a square or move"])
    return Decision(Ruling.NO_VIOLATION)


# ---------- B1/B2: text classifiers ----------

class NaiveBayes:
    """Multinomial naive Bayes over words of the normalised text, with add-one smoothing."""

    def __init__(self, with_history=False):
        self.with_history = with_history
        self.counts, self.totals, self.priors, self.vocab = {}, {}, Counter(), set()

    def _words(self, u):
        text = (u.previous + " || " if self.with_history else "") + u.text
        return normalise(text).split()

    def fit(self, examples):
        for u, ruling in examples:
            words = self._words(u)
            self.priors[ruling] += 1
            self.counts.setdefault(ruling, Counter()).update(words)
            self.vocab.update(words)
        self.totals = {r: sum(c.values()) for r, c in self.counts.items()}
        return self

    def __call__(self, u: Utterance) -> Decision:
        words = self._words(u)
        n = sum(self.priors.values())
        best, best_score = None, -math.inf
        for r, prior in self.priors.items():
            score = math.log(prior / n)
            denom = self.totals[r] + len(self.vocab) + 1
            for w in words:
                score += math.log((self.counts[r][w] + 1) / denom)
            if score > best_score:
                best, best_score = r, score
        return Decision(best, ["text classifier"])


# ---------- B3: keywords + board ----------

def b3_board(u: Utterance) -> Decision:
    if _has(u.text, THREATS):
        return Decision(Ruling.ESCALATE, ["threat phrase"])
    if _has(u.text, ABUSE):
        return Decision(Ruling.CONDUCT_WARNING, ["abusive word"])
    moves = resolve(Board(u.fen), mentions(u.text))
    if moves:
        return Decision(Ruling.HIGH_CONFIDENCE_VIOLATION, [f"names a legal move for the side to move ({moves[0].uci()})"])
    return Decision(Ruling.NO_VIOLATION)


# ---------- B4: board + role + phase + contract + abstention ----------

def b4_contextual(u: Utterance) -> Decision:
    when = {Phase.PRE: "before the game", Phase.DURING: "during play", Phase.POST: "after the game"}[u.phase]
    observed = f"{u.role.value.lower()} spoke {when}; match rules: {u.contract.value.lower()}"
    if _has(u.text, THREATS):
        return Decision(Ruling.ESCALATE, [observed, "threat phrase: a person must review this"])
    if _has(u.text, ABUSE):
        return Decision(Ruling.CONDUCT_WARNING, [observed, "abusive language"])
    found = mentions(u.text)
    if not found:
        return Decision(Ruling.NO_VIOLATION, [observed])
    if u.phase is not Phase.DURING:
        return Decision(Ruling.NO_VIOLATION, [observed, "chess talk outside play is allowed"])
    if u.contract in (Contract.OPEN, Contract.TRAINING):
        return Decision(Ruling.NO_VIOLATION, [observed, "this match allows assistance"])

    board = Board(u.fen)
    moves = resolve(board, found)
    side = "White" if board.white else "Black"
    if u.role is Role.PLAYER:
        t = normalise(u.text)
        if FIRST_PERSON.search(t) and not ADDRESSED.search(t):
            return Decision(Ruling.NO_VIOLATION, [observed, "a player describing their own position"])
        if moves and ADDRESSED.search(t) and u.contract is Contract.STRICT:
            return Decision(Ruling.POSSIBLE_RULE_VIOLATION,
                            [observed, f"suggests a legal move to the player on move ({moves[0].uci()})",
                             "strict matches do not allow position talk aimed at the opponent"])
        return Decision(Ruling.NO_VIOLATION, [observed, "player chat allowed in this match"])
    if not moves:
        return Decision(Ruling.INSUFFICIENT_EVIDENCE,
                        [observed, "names a square, but no legal move for the side to move matches it"])
    if u.role is Role.UNKNOWN:
        return Decision(Ruling.INSUFFICIENT_EVIDENCE,
                        [observed, f"names a legal move for {side} ({moves[0].uci()})", "speaker not identified"])
    return Decision(Ruling.HIGH_CONFIDENCE_VIOLATION,
                    [observed, f"a spectator named a legal move for {side} ({moves[0].uci()}) during play",
                     "outside assistance is not allowed in this match", "a person must confirm before any sanction"])


def engines(training):
    """All methods; B1 and B2 are trained on `training` [(Utterance, Ruling)]."""
    return {"B0": b0_keywords, "B1": NaiveBayes().fit(training), "B2": NaiveBayes(with_history=True).fit(training),
            "B3": b3_board, "B4": b4_contextual}


__all__ = ["Ruling", "Contract", "Role", "Phase", "Utterance", "Decision", "engines", "b4_contextual",
           "mentions", "resolve", "normalise", "FILES"]
