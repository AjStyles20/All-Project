"""Labelled chess-speech benchmark (Pass 003 classes C0–C9, C7 not modelled).

Each case is rendered under all four match contracts; the expected ruling comes from the
TRUTH table below, which states the policy, not from any arbiter method.

Two template pools: DEV (used while building the methods) and HELD_OUT (paraphrases,
not used while building B4; also run through a speech-recognition noise pass).
"""
import random
from dataclasses import dataclass

from p010.arbiter import Contract, Phase, Role, Ruling, Utterance
from p010.chess import Board, name

POSITIONS = [
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3",
    "r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
    "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2",
    "rnbqkbnr/ppp2ppp/4p3/3p4/2PP4/8/PP2PPPP/RNBQKBNR w KQkq - 0 3",
    "r2q1rk1/pp2bppp/2n1bn2/3p4/3P4/2NBBN2/PP3PPP/R2Q1RK1 w - - 4 11",
    "r1bq1rk1/ppp2ppp/2np1n2/2b1p3/2B1P3/2NP1N2/PPP2PPP/R1BQ1RK1 b - - 0 7",
]

N, W, P, H, I, E = (Ruling.NO_VIOLATION, Ruling.CONDUCT_WARNING, Ruling.POSSIBLE_RULE_VIOLATION,
                    Ruling.HIGH_CONFIDENCE_VIOLATION, Ruling.INSUFFICIENT_EVIDENCE, Ruling.ESCALATE)

# Policy: expected ruling per class and contract.
TRUTH = {
    "C0": dict.fromkeys(Contract, N),
    "C1": dict.fromkeys(Contract, N),
    "C2": dict.fromkeys(Contract, W),
    "C3": dict.fromkeys(Contract, E),
    "C4": dict.fromkeys(Contract, N),
    "C5": {Contract.STRICT: P, Contract.SOCIAL: N, Contract.OPEN: N, Contract.TRAINING: N},
    "C6": {Contract.STRICT: H, Contract.SOCIAL: H, Contract.OPEN: N, Contract.TRAINING: N},
    "C8": dict.fromkeys(Contract, N),
    "C9": {Contract.STRICT: I, Contract.SOCIAL: I, Contract.OPEN: N, Contract.TRAINING: N},
}
CLASSES = tuple(TRUTH)

DEV = {
    "C0": ["good luck have fun", "how was your day", "is the sound ok on your side", "nice to meet you",
           "thanks for the game invite"],
    "C1": ["you're going down", "lucky move", "nice try", "this one is mine", "bring it on"],
    "C2": ["you are an idiot", "what a loser", "you play like garbage", "pathetic", "stupid move you clown"],
    "C3": ["i know where you live", "i will find you", "i will hurt you after this", "i will make you pay"],
    "C4": ["my {piece} on {own} is doing nothing", "ugh my {piece} on {own} is stuck", "i hate my {piece} on {own}"],
    "C5": ["you should really play {move}", "{move} is your best move", "why not {move} you'd be winning"],
    "C6": ["play {move}", "{move} wins", "go {move} quick", "{move} {move}"],
    "C8": ["{move} would have won", "you missed {move} earlier", "{move} was the move there"],
    "C9": ["{bad} looks interesting", "what about {bad}", "{bad} maybe"],
}
HELD_OUT = {
    "C0": ["can you hear me alright", "hope you're having a good weekend", "ready when you are"],
    "C1": ["prepare to lose", "you got lucky there", "not today my friend"],
    "C2": ["you absolute moron", "useless player", "you dumb muppet", "you are such a donkey"],
    "C3": ["i'm coming for you", "watch your back i will hurt you", "i'll find you after this"],
    "C4": ["this {piece} of mine on {own} is so weak", "honestly my {piece} on {own} has no squares"],
    "C5": ["honestly your only move is {move}", "if i were you i'd go {move}"],
    "C6": ["psst {move}", "{move} is crushing do it", "come on just {move}"],
    "C8": ["the engine says {move} was best", "after the game i think {move} was stronger"],
    "C9": ["isn't {bad} possible", "i'd look at {bad}"],
}
PIECE_NAMES = {"N": "knight", "B": "bishop", "R": "rook", "Q": "queen", "K": "king", "P": "pawn"}


@dataclass(frozen=True)
class Case:
    cls: str
    utterance: Utterance
    expected: Ruling
    group: int     # same text and context under different contracts share a group


def speak_move(board, m, rng):
    p = board.squares[m.frm].upper()
    to = name(m.to)
    capture = board.squares[m.to] is not None
    options = [f"{PIECE_NAMES[p]} {to}", f"{PIECE_NAMES[p]} to {to}", board.san(m).rstrip("+#")]
    if capture:
        options.append(f"take on {to}")
    if p == "P":
        options.append(f"push {to}")
    return rng.choice(options)


def _bad_mention(board, rng):
    """A piece and square that match no legal move for the side to move."""
    legal = {(board.squares[m.frm].upper(), m.to) for m in board.legal_moves()}
    for _ in range(200):
        piece, sq = rng.choice("NBRQ"), rng.randrange(64)
        if (piece, sq) not in legal:
            return f"{PIECE_NAMES[piece]} {name(sq)}"
    return "bishop a1"


def _own_piece(board, rng):
    side_upper = board.white
    own = [(sq, p) for sq, p in enumerate(board.squares) if p and p.isupper() == side_upper and p.upper() in "NBRQ"]
    sq, p = rng.choice(own)
    return PIECE_NAMES[p.upper()], name(sq)


def noisy(text, rng):
    """Speech-recognition style errors: digits as words, sound-alikes, dropped little words."""
    words = {"1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight"}
    out = []
    for w in text.split():
        if len(w) == 2 and w[0] in "abcdefgh" and w[1] in words and rng.random() < 0.7:
            w = f"{w[0]} {words[w[1]]}"
        elif w == "knight" and rng.random() < 0.5:
            w = "night"
        elif w in ("to", "on") and rng.random() < 0.3:
            continue
        out.append(w)
    return " ".join(out)


def generate(pool: str, seeds, noise=False) -> list[Case]:
    templates = {"dev": DEV, "held_out": HELD_OUT}[pool]
    cases, group = [], 0
    for seed in seeds:
        rng = random.Random(f"{pool}:{seed}:{noise}")
        for cls in CLASSES:
            for template in templates[cls]:
                fen = rng.choice(POSITIONS)
                board = Board(fen)
                move = rng.choice(board.legal_moves())
                piece, own = _own_piece(board, rng)
                text = template.format(move=speak_move(board, move, rng), bad=_bad_mention(board, rng),
                                       piece=piece, own=own)
                if noise:
                    text = noisy(text, rng)
                role, phase = _context(cls, rng)
                previous = rng.choice(["", "good game so far", "hmm", "what a position"])
                group += 1
                for contract in Contract:
                    u = Utterance(text, role, phase, fen, contract, previous)
                    cases.append(Case(cls, u, TRUTH[cls][contract], group))
    return cases


def _context(cls, rng):
    if cls in ("C4", "C5"):
        return Role.PLAYER, Phase.DURING
    if cls == "C6":
        return Role.SPECTATOR, Phase.DURING
    if cls == "C8":
        return rng.choice([Role.PLAYER, Role.SPECTATOR]), Phase.POST
    if cls == "C9":
        # A mention that matches no legal move, by a spectator or an unidentified speaker.
        return rng.choice([Role.SPECTATOR, Role.UNKNOWN]), Phase.DURING
    return rng.choice(list(Role)), rng.choice(list(Phase))
