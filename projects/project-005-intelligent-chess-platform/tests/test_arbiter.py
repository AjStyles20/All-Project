import pytest
from fastapi.testclient import TestClient

from p010.api import create_app
from p010.arbiter import Contract, Phase, Role, Ruling, Utterance, b4_contextual, mentions, normalise
from p010.benchmark import TRUTH, generate
from p010.chess import START_FEN
from p010.evaluation import rule

AFTER_E4 = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"


def ruling(text, role=Role.SPECTATOR, phase=Phase.DURING, contract=Contract.STRICT, fen=AFTER_E4):
    return b4_contextual(Utterance(text, role, phase, fen, contract)).ruling


def test_speech_recognition_errors_are_absorbed():
    assert normalise("Night F six!") == "knight f6"
    assert ("N", "f6") in mentions("night to f six")


def test_same_words_different_rulings_by_context():
    text = "knight f6"   # a legal move for Black after 1.e4
    assert ruling(text) is Ruling.HIGH_CONFIDENCE_VIOLATION
    assert ruling(text, contract=Contract.TRAINING) is Ruling.NO_VIOLATION
    assert ruling(text, phase=Phase.POST) is Ruling.NO_VIOLATION
    assert ruling(text, role=Role.UNKNOWN) is Ruling.INSUFFICIENT_EVIDENCE


def test_board_decides_whether_a_mention_is_a_move():
    # No black knight can reach f3 now: not identifiable assistance.
    assert ruling("knight f3") is Ruling.INSUFFICIENT_EVIDENCE


def test_players_describing_their_own_position_are_fine():
    assert ruling("my knight on g8 is doing nothing", role=Role.PLAYER) is Ruling.NO_VIOLATION


def test_suggesting_a_move_to_the_opponent_depends_on_the_contract():
    assert ruling("you should play knight f6", role=Role.PLAYER) is Ruling.POSSIBLE_RULE_VIOLATION
    assert ruling("you should play knight f6", role=Role.PLAYER, contract=Contract.SOCIAL) is Ruling.NO_VIOLATION


def test_conduct_is_judged_in_every_contract():
    for contract in Contract:
        assert ruling("you are an idiot", contract=contract) is Ruling.CONDUCT_WARNING
        assert ruling("i know where you live", contract=contract) is Ruling.ESCALATE


def test_every_ruling_carries_evidence():
    d = b4_contextual(Utterance("knight f6", Role.SPECTATOR, Phase.DURING, AFTER_E4, Contract.STRICT))
    assert any("g8f6" in e for e in d.evidence) and any("person must confirm" in e for e in d.evidence)


def test_benchmark_labels_come_from_the_policy_table():
    cases = generate("dev", range(1))
    assert all(c.expected is TRUTH[c.cls][c.utterance.contract] for c in cases)
    assert len({c.utterance.contract for c in cases}) == 4


def test_rule_rejects_recall_bought_with_false_penalties():
    good = {"macro_f1": 0.9, "false_penalty_rate": 0.0, "missed_severe_rate": 0.0}
    noisy_b4 = {"macro_f1": 0.99, "false_penalty_rate": 0.3, "missed_severe_rate": 0.0}
    assert rule({"dev": {"B0": good, "B4": noisy_b4}})["overall"] == "NOT SUPPORTED"


# ---------- games through the API ----------

def setup(contract="STRICT"):
    c = TestClient(create_app())
    g = c.post("/api/games", json={"contract": contract}).json()
    return c, g


def test_only_the_player_on_move_can_move():
    c, g = setup()
    gid = g["game_id"]
    assert c.post(f"/api/games/{gid}/move", json={"token": g["black_token"], "uci": "e7e5"}).status_code == 409
    assert c.post(f"/api/games/{gid}/move", json={"token": "nope", "uci": "e2e4"}).status_code == 403
    assert c.post(f"/api/games/{gid}/move", json={"token": g["white_token"], "uci": "e2e5"}).status_code == 400
    state = c.post(f"/api/games/{gid}/move", json={"token": g["white_token"], "uci": "e2e4"}).json()
    assert state["moves"] == ["e4"] and state["turn"] == "black"


def test_spectator_move_hint_gets_an_arbiter_notice_but_changes_nothing():
    c, g = setup()
    gid = g["game_id"]
    c.post(f"/api/games/{gid}/move", json={"token": g["white_token"], "uci": "e2e4"})
    msg = c.post(f"/api/games/{gid}/chat", json={"name": "sam", "text": "knight f6!"}).json()
    assert msg["role"] == "SPECTATOR" and msg["ruling"] == "HIGH-CONFIDENCE VIOLATION"
    state = c.get(f"/api/games/{gid}").json()
    assert state["result"] is None and state["turn"] == "black"


def test_player_chat_is_identified_by_seat_token():
    c, g = setup("SOCIAL")
    msg = c.post(f"/api/games/{g['game_id']}/chat", json={"token": g["white_token"], "text": "good luck"}).json()
    assert msg["role"] == "PLAYER" and msg["author"] == "white" and msg["ruling"] == "NO VIOLATION"


def test_fools_mate_ends_the_game_and_chat_is_then_post_game():
    c, g = setup()
    gid = g["game_id"]
    for seat, uci in (("white", "f2f3"), ("black", "e7e5"), ("white", "g2g4"), ("black", "d8h4")):
        c.post(f"/api/games/{gid}/move", json={"token": g[f"{seat}_token"], "uci": uci})
    state = c.get(f"/api/games/{gid}").json()
    assert state["result"] == "0-1" and state["reason"] == "checkmate" and state["phase"] == "POST"
    msg = c.post(f"/api/games/{gid}/chat", json={"text": "g3 would have held"}).json()
    assert msg["ruling"] == "NO VIOLATION"


def test_resign_and_validation():
    c, g = setup()
    gid = g["game_id"]
    assert c.post(f"/api/games/{gid}/chat", json={"text": "x" * 301}).status_code == 422
    assert c.post(f"/api/games/{gid}/resign", json={"token": "nope"}).status_code == 403
    assert c.post(f"/api/games/{gid}/resign", json={"token": g["black_token"]}).json()["result"] == "1-0"
    assert c.get("/api/games/unknown").status_code == 404


def test_page_has_strict_csp():
    r = TestClient(create_app()).get("/")
    assert r.status_code == 200 and "default-src 'self'" in r.headers["content-security-policy"]
