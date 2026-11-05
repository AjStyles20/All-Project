import pytest

from p010.chess import START_FEN, Board, IllegalMove, perft

# Published perft counts (chessprogramming.org). Depths kept small so CI stays fast.
PERFT = [
    (START_FEN, [20, 400, 8902]),
    ("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1", [48, 2039]),
    ("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1", [14, 191, 2812]),
    ("r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1", [6, 264]),
    ("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8", [44, 1486]),
]


@pytest.mark.parametrize("fen,counts", PERFT)
def test_perft(fen, counts):
    board = Board(fen)
    assert [perft(board, d + 1) for d in range(len(counts))] == counts
    assert board.fen() == fen  # make/unmake restored everything


def play(board, *sans):
    for s in sans:
        board.push(board.parse_san(s))
    return board


def test_scholars_mate_is_checkmate_and_san_marks_it():
    b = play(Board(), "e4", "e5", "Bc4", "Nc6", "Qh5", "Nf6")
    assert b.san(b.parse_san("Qxf7")) == "Qxf7#"
    play(b, "Qxf7#")
    assert b.outcome() == "checkmate"


def test_stalemate():
    assert Board("7k/5Q2/6K1/8/8/8/8/8 b - - 0 1").outcome() == "stalemate"


def test_castling_rights_and_through_check():
    b = Board("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")
    assert {"O-O", "O-O-O"} <= {b.san(m) for m in b.legal_moves()}
    attacked = Board("r3k2r/8/8/8/8/8/5r2/R3K2R w KQkq - 0 1")  # f2 rook covers f1
    assert "O-O" not in {attacked.san(m) for m in attacked.legal_moves()}
    play(b, "Rb1")
    assert "Q" not in b.castling


def test_en_passant_only_immediately():
    b = play(Board(), "e4", "a6", "e5", "d5")
    assert b.san(b.parse_san("exd6")) == "exd6"
    play(b, "a3", "a5")
    with pytest.raises(IllegalMove):
        b.parse_san("exd6")


def test_promotion_and_disambiguation():
    b = Board("8/P7/8/8/8/8/8/k1K5 w - - 0 1")
    # Queen and rook promotions also mate the king on a1 along the a-file.
    assert {b.san(m) for m in b.legal_moves() if b.squares[m.frm] == "P"} == {"a8=Q#", "a8=R#", "a8=B", "a8=N"}
    knights = Board("k7/8/8/8/8/8/8/1N1N2K1 w - - 0 1")
    assert "Nbc3" in {knights.san(m) for m in knights.legal_moves()}


def test_threefold_repetition_and_insufficient_material():
    b = play(Board(), "Nf3", "Nf6", "Ng1", "Ng8", "Nf3", "Nf6", "Ng1", "Ng8")
    assert b.outcome() == "threefold repetition"
    assert Board("8/8/8/4k3/8/8/2B5/4K3 w - - 0 1").outcome() == "insufficient material"
    assert Board("8/8/8/4k3/8/8/2R5/4K3 w - - 0 1").outcome() is None


def test_pinned_piece_cannot_move():
    b = Board("4k3/4r3/8/8/8/8/4B3/4K3 w - - 0 1")
    assert not any(b.squares[m.frm] == "B" for m in b.legal_moves())


def test_bad_input_is_rejected():
    with pytest.raises(ValueError):
        Board("not a fen")
    with pytest.raises(IllegalMove):
        Board().parse_uci("e2e5")
    with pytest.raises(IllegalMove):
        Board().parse_uci("zz")
