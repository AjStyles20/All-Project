"""Games in memory: two seats with secret tokens, moves, resignation, chat with arbiter notices.

Games live only while the server runs (first version). The arbiter (B4) annotates chat; it
never changes the game. Only a person may act on a notice.
"""
import secrets
import threading
import time
import uuid
from dataclasses import dataclass, field

from p010.arbiter import Contract, Phase, Role, Ruling, Utterance, b4_contextual
from p010.chess import Board, IllegalMove

MAX_GAMES = 1000
MAX_MESSAGES = 500


class GameError(Exception):
    def __init__(self, message, status=409):
        super().__init__(message)
        self.status = status


@dataclass
class Message:
    n: int
    at: float
    author: str
    role: str
    text: str
    ruling: str
    evidence: list


@dataclass
class Game:
    game_id: str
    contract: Contract
    tokens: dict                     # "white"/"black" -> token
    board: Board = field(default_factory=Board)
    sans: list = field(default_factory=list)
    messages: list = field(default_factory=list)
    result: str | None = None
    reason: str | None = None
    created: float = field(default_factory=time.time)

    @property
    def phase(self) -> Phase:
        if self.result:
            return Phase.POST
        return Phase.DURING if self.sans else Phase.PRE

    def seat_of(self, token: str | None) -> str | None:
        if not token:
            return None
        for seat, secret in self.tokens.items():
            if secrets.compare_digest(secret.encode(), token.encode()):
                return seat
        return None

    def view(self, since: int = 0) -> dict:
        return {"game_id": self.game_id, "contract": self.contract.value, "fen": self.board.fen(),
                "turn": "white" if self.board.white else "black", "moves": list(self.sans),
                "in_check": self.board.in_check(), "result": self.result, "reason": self.reason,
                "phase": self.phase.value,
                "legal": [m.uci() for m in self.board.legal_moves()] if not self.result else [],
                "messages": [m.__dict__ for m in self.messages if m.n > since]}


class Games:
    def __init__(self):
        self.games: dict[str, Game] = {}
        self.lock = threading.Lock()

    def create(self, contract: Contract) -> tuple[Game, dict]:
        with self.lock:
            if len(self.games) >= MAX_GAMES:
                oldest = min(self.games.values(), key=lambda g: g.created)
                del self.games[oldest.game_id]
            tokens = {"white": secrets.token_urlsafe(16), "black": secrets.token_urlsafe(16)}
            game = Game(uuid.uuid4().hex, contract, tokens)
            self.games[game.game_id] = game
            return game, tokens

    def get(self, game_id: str) -> Game:
        game = self.games.get(game_id)
        if game is None:
            raise GameError("No such game.", 404)
        return game

    def move(self, game_id: str, token: str, uci: str) -> Game:
        with self.lock:
            game = self.get(game_id)
            seat = game.seat_of(token)
            if seat is None:
                raise GameError("Only the two players can move.", 403)
            if game.result:
                raise GameError("The game is over.")
            if seat != ("white" if game.board.white else "black"):
                raise GameError("It is not your turn.")
            try:
                m = game.board.parse_uci(uci)
            except IllegalMove as exc:
                raise GameError(str(exc), 400) from exc
            game.sans.append(game.board.san(m))
            game.board.push(m)
            reason = game.board.outcome()
            if reason:
                game.reason = reason
                if reason == "checkmate":
                    game.result = "0-1" if game.board.white else "1-0"
                else:
                    game.result = "1/2-1/2"
            return game

    def resign(self, game_id: str, token: str) -> Game:
        with self.lock:
            game = self.get(game_id)
            seat = game.seat_of(token)
            if seat is None:
                raise GameError("Only the two players can resign.", 403)
            if game.result:
                raise GameError("The game is over.")
            game.result, game.reason = ("0-1" if seat == "white" else "1-0"), f"{seat} resigned"
            return game

    def chat(self, game_id: str, token: str | None, author: str, text: str) -> Message:
        with self.lock:
            game = self.get(game_id)
            if len(game.messages) >= MAX_MESSAGES:
                raise GameError("This game's chat is full.")
            seat = game.seat_of(token)
            role = Role.PLAYER if seat else Role.SPECTATOR
            previous = game.messages[-1].text if game.messages else ""
            decision = b4_contextual(Utterance(text, role, game.phase, game.board.fen(), game.contract, previous))
            message = Message(len(game.messages) + 1, time.time(), seat or author or "spectator", role.value,
                              text, decision.ruling.value,
                              decision.evidence if decision.ruling is not Ruling.NO_VIOLATION else [])
            game.messages.append(message)
            return message
