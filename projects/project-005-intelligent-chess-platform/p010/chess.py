"""Chess rules: legal moves, check, mate, stalemate, draws by the fifty-move rule, repetition
and insufficient material, SAN in and out, FEN in and out.

Written for this project instead of using python-chess (GPL-3.0). Correctness is checked
against published perft node counts in tests/test_chess.py.

Board: 0..63, a1 = 0, h8 = 63. Pieces are letters, uppercase for White.
"""
from dataclasses import dataclass

START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
FILES = "abcdefgh"

KNIGHT = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
KING = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
ROOK_DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
BISHOP_DIRS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]


def square(name: str) -> int:
    return FILES.index(name[0]) + 8 * (int(name[1]) - 1)


def name(sq: int) -> str:
    return FILES[sq % 8] + str(sq // 8 + 1)


def _step(sq, df, dr):
    f, r = sq % 8 + df, sq // 8 + dr
    return f + 8 * r if 0 <= f < 8 and 0 <= r < 8 else None


@dataclass(frozen=True)
class Move:
    frm: int
    to: int
    promotion: str | None = None

    def uci(self) -> str:
        return name(self.frm) + name(self.to) + (self.promotion.lower() if self.promotion else "")


class IllegalMove(ValueError):
    pass


class Board:
    def __init__(self, fen: str = START_FEN):
        parts = fen.split()
        if len(parts) != 6:
            raise ValueError("FEN must have six fields")
        rows = parts[0].split("/")
        if len(rows) != 8:
            raise ValueError("FEN board must have eight ranks")
        self.squares = [None] * 64
        for i, row in enumerate(rows):
            f = 0
            for c in row:
                if c.isdigit():
                    f += int(c)
                elif c in "pnbrqkPNBRQK" and f < 8:
                    self.squares[f + 8 * (7 - i)] = c
                    f += 1
                else:
                    raise ValueError("bad FEN board")
            if f != 8:
                raise ValueError("bad FEN rank length")
        self.white = parts[1] == "w"
        self.castling = "" if parts[2] == "-" else parts[2]
        self.ep = None if parts[3] == "-" else square(parts[3])
        self.halfmove = int(parts[4])
        self.fullmove = int(parts[5])
        self.history = [self._position_key()]

    # ---- FEN ----

    def fen(self) -> str:
        rows = []
        for r in range(7, -1, -1):
            row, empty = "", 0
            for f in range(8):
                p = self.squares[f + 8 * r]
                if p is None:
                    empty += 1
                else:
                    row += (str(empty) if empty else "") + p
                    empty = 0
            rows.append(row + (str(empty) if empty else ""))
        return " ".join(["/".join(rows), "w" if self.white else "b", self.castling or "-",
                         name(self.ep) if self.ep is not None else "-", str(self.halfmove), str(self.fullmove)])

    def _position_key(self):
        # En passant counts only when a capture is actually possible (FIDE 9.2.3).
        ep = self.ep if self.ep is not None and any(m.to == self.ep and self.squares[m.frm] in "Pp"
                                                     for m in self._pseudo()) else None
        return (tuple(self.squares), self.white, self.castling, ep)

    # ---- attacks ----

    def _own(self, p, white):
        return p is not None and p.isupper() == white

    def attacked(self, sq: int, by_white: bool) -> bool:
        pawn = "P" if by_white else "p"
        for df in (-1, 1):
            s = _step(sq, df, -1 if by_white else 1)
            if s is not None and self.squares[s] == pawn:
                return True
        for df, dr in KNIGHT:
            s = _step(sq, df, dr)
            if s is not None and self.squares[s] == ("N" if by_white else "n"):
                return True
        for df, dr in KING:
            s = _step(sq, df, dr)
            if s is not None and self.squares[s] == ("K" if by_white else "k"):
                return True
        for dirs, pieces in ((ROOK_DIRS, "RQ"), (BISHOP_DIRS, "BQ")):
            targets = pieces if by_white else pieces.lower()
            for df, dr in dirs:
                s = _step(sq, df, dr)
                while s is not None:
                    p = self.squares[s]
                    if p is not None:
                        if p in targets:
                            return True
                        break
                    s = _step(s, df, dr)
        return False

    def king(self, white: bool) -> int:
        return self.squares.index("K" if white else "k")

    def in_check(self) -> bool:
        return self.attacked(self.king(self.white), not self.white)

    # ---- move generation ----

    def _pseudo(self):
        white = self.white
        for sq, p in enumerate(self.squares):
            if p is None or p.isupper() != white:
                continue
            kind = p.upper()
            if kind == "P":
                yield from self._pawn_moves(sq, white)
            elif kind == "N":
                for df, dr in KNIGHT:
                    s = _step(sq, df, dr)
                    if s is not None and not self._own(self.squares[s], white):
                        yield Move(sq, s)
            elif kind == "K":
                for df, dr in KING:
                    s = _step(sq, df, dr)
                    if s is not None and not self._own(self.squares[s], white):
                        yield Move(sq, s)
                yield from self._castles(white)
            else:
                dirs = {"R": ROOK_DIRS, "B": BISHOP_DIRS, "Q": ROOK_DIRS + BISHOP_DIRS}[kind]
                for df, dr in dirs:
                    s = _step(sq, df, dr)
                    while s is not None:
                        if self._own(self.squares[s], white):
                            break
                        yield Move(sq, s)
                        if self.squares[s] is not None:
                            break
                        s = _step(s, df, dr)

    def _pawn_moves(self, sq, white):
        dr = 1 if white else -1
        start, last = (1, 7) if white else (6, 0)
        promos = "QRBN" if white else "qrbn"
        one = _step(sq, 0, dr)
        if one is not None and self.squares[one] is None:
            yield from self._pawn_to(sq, one, last, promos)
            two = _step(one, 0, dr)
            if sq // 8 == start and self.squares[two] is None:
                yield Move(sq, two)
        for df in (-1, 1):
            s = _step(sq, df, dr)
            if s is None:
                continue
            target = self.squares[s]
            if target is not None and target.isupper() != white:
                yield from self._pawn_to(sq, s, last, promos)
            elif s == self.ep:
                yield Move(sq, s)

    @staticmethod
    def _pawn_to(frm, to, last, promos):
        if to // 8 == last:
            for p in promos:
                yield Move(frm, to, p)
        else:
            yield Move(frm, to)

    def _castles(self, white):
        rank = 0 if white else 7
        king_sq = 4 + 8 * rank
        if self.squares[king_sq] != ("K" if white else "k") or self.attacked(king_sq, not white):
            return
        rook = "R" if white else "r"
        if ("K" if white else "k") in self.castling and self.squares[7 + 8 * rank] == rook and \
                all(self.squares[f + 8 * rank] is None for f in (5, 6)) and \
                not any(self.attacked(f + 8 * rank, not white) for f in (5, 6)):
            yield Move(king_sq, 6 + 8 * rank)
        if ("Q" if white else "q") in self.castling and self.squares[8 * rank] == rook and \
                all(self.squares[f + 8 * rank] is None for f in (1, 2, 3)) and \
                not any(self.attacked(f + 8 * rank, not white) for f in (2, 3)):
            yield Move(king_sq, 2 + 8 * rank)

    def legal_moves(self) -> list[Move]:
        moves = []
        # Materialise first: making a move mutates the board the generator walks.
        for m in list(self._pseudo()):
            undo = self._make(m)
            if not self.attacked(self.king(not self.white), self.white):
                moves.append(m)
            self._unmake(undo)
        return moves

    # ---- making moves ----

    def _make(self, m: Move):
        undo = (list(self.squares), self.white, self.castling, self.ep, self.halfmove, self.fullmove)
        p = self.squares[m.frm]
        captured = self.squares[m.to]
        self.squares[m.to] = m.promotion or p
        self.squares[m.frm] = None
        if p in "Pp" and m.to == self.ep:
            self.squares[m.to + (-8 if p == "P" else 8)] = None
            captured = "p"
        if p in "Kk" and abs(m.to - m.frm) == 2:
            rank = m.frm // 8
            if m.to % 8 == 6:
                self.squares[5 + 8 * rank], self.squares[7 + 8 * rank] = self.squares[7 + 8 * rank], None
            else:
                self.squares[3 + 8 * rank], self.squares[8 * rank] = self.squares[8 * rank], None
        rights = self.castling
        for sq, lose in ((4, "KQ"), (60, "kq"), (0, "Q"), (7, "K"), (56, "q"), (63, "k")):
            if m.frm == sq or m.to == sq:
                rights = "".join(c for c in rights if c not in lose)
        self.castling = rights
        self.ep = (m.frm + m.to) // 2 if p in "Pp" and abs(m.to - m.frm) == 16 else None
        self.halfmove = 0 if p in "Pp" or captured else self.halfmove + 1
        if not self.white:
            self.fullmove += 1
        self.white = not self.white
        return undo

    def _unmake(self, undo):
        squares, self.white, self.castling, self.ep, self.halfmove, self.fullmove = undo
        self.squares[:] = squares

    def push(self, m: Move) -> None:
        if m not in self.legal_moves():
            raise IllegalMove(f"{m.uci()} is not legal here")
        self._make(m)
        self.history.append(self._position_key())

    # ---- game end ----

    def outcome(self) -> str | None:
        """None while the game goes on, else a reason."""
        if not self.legal_moves():
            return "checkmate" if self.in_check() else "stalemate"
        if self.halfmove >= 100:
            return "fifty-move rule"
        if self.history.count(self.history[-1]) >= 3:
            return "threefold repetition"
        if self._insufficient():
            return "insufficient material"
        return None

    def _insufficient(self):
        pieces = [p for p in self.squares if p is not None and p not in "Kk"]
        if not pieces:
            return True
        if len(pieces) == 1 and pieces[0] in "NBnb":
            return True
        if all(p in "Bb" for p in pieces):
            colours = {(sq % 8 + sq // 8) % 2 for sq, p in enumerate(self.squares) if p in ("B", "b")}
            return len(colours) == 1
        return False

    # ---- SAN ----

    def san(self, m: Move) -> str:
        p = self.squares[m.frm]
        kind = p.upper()
        if kind == "K" and abs(m.to - m.frm) == 2:
            text = "O-O" if m.to % 8 == 6 else "O-O-O"
        else:
            capture = self.squares[m.to] is not None or (kind == "P" and m.to == self.ep)
            if kind == "P":
                text = (FILES[m.frm % 8] + "x" if capture else "") + name(m.to)
                if m.promotion:
                    text += "=" + m.promotion.upper()
            else:
                rivals = [o for o in self.legal_moves() if o.to == m.to and o.frm != m.frm
                          and self.squares[o.frm] == p]
                hint = ""
                if rivals:
                    if all(o.frm % 8 != m.frm % 8 for o in rivals):
                        hint = FILES[m.frm % 8]
                    elif all(o.frm // 8 != m.frm // 8 for o in rivals):
                        hint = str(m.frm // 8 + 1)
                    else:
                        hint = name(m.frm)
                text = kind + hint + ("x" if capture else "") + name(m.to)
        undo = self._make(m)
        if self.in_check():
            text += "#" if not self.legal_moves() else "+"
        self._unmake(undo)
        return text

    def parse_san(self, text: str) -> Move:
        cleaned = text.strip().replace("0-0-0", "O-O-O").replace("0-0", "O-O").rstrip("+#!?")
        for m in self.legal_moves():
            if self.san(m).rstrip("+#") == cleaned:
                return m
        raise IllegalMove(f"{text} is not a legal move here")

    def parse_uci(self, text: str) -> Move:
        text = text.strip().lower()
        if len(text) not in (4, 5) or text[0] not in FILES or text[2] not in FILES:
            raise IllegalMove("Use moves like e2e4 or e7e8q.")
        try:
            frm, to = square(text[:2]), square(text[2:4])
        except (ValueError, IndexError) as exc:
            raise IllegalMove("Use moves like e2e4 or e7e8q.") from exc
        promo = None
        if len(text) == 5:
            promo = text[4].upper() if self.white else text[4]
        m = Move(frm, to, promo)
        if m not in self.legal_moves():
            raise IllegalMove(f"{text} is not legal here")
        return m


def perft(board: Board, depth: int) -> int:
    if depth == 0:
        return 1
    total = 0
    moves = board.legal_moves()
    if depth == 1:
        return len(moves)
    for m in moves:
        undo = board._make(m)
        total += perft(board, depth - 1)
        board._unmake(undo)
    return total
