import threading

import pytest

from p007.domain import IssuerContext, RewardItem, RewardPolicy
from p007.store import Ledger, LedgerError

READ = RewardPolicy("READ", 1, "Reading", "READING", "10 per book", "Read more", 10, "pages")
PART = RewardPolicy("PART", 1, "Participation", "PARTICIPATION", "2 per contribution", "Contribute", 2)


def ledger(tmp_path):
    led = Ledger(tmp_path / "l.sqlite3")
    led.add_policy(READ)
    led.add_policy(PART)
    led.add_student("s1", "A")
    led.add_student("s2", "B")
    led.add_issuer(IssuerContext("t1", "TEACHER", frozenset({"READ", "PART"})))
    led.add_issuer(IssuerContext("t2", "TEACHER", frozenset({"PART"})))
    led.add_reward(RewardItem("r1", "Pass", 15, 1))
    return led


def test_balance_is_the_sum_of_the_log(tmp_path):
    led = ledger(tmp_path)
    led.earn("t1", "s1", "READ", 1, measure=200)
    led.earn("t1", "s1", "PART", 2)
    assert led.balance("s1") == 12
    assert {r["student_id"]: r["balance"] for r in led.balances()} == {"s1": 12, "s2": 0}


def test_issuer_outside_its_scope_is_refused(tmp_path):
    led = ledger(tmp_path)
    with pytest.raises(LedgerError, match="may not award"):
        led.earn("t2", "s1", "READ", 1, measure=200)


def test_policy_with_an_objective_measure_requires_it(tmp_path):
    with pytest.raises(LedgerError, match="pages"):
        ledger(tmp_path).earn("t1", "s1", "READ", 1)


def test_redeem_checks_balance_and_stock(tmp_path):
    led = ledger(tmp_path)
    with pytest.raises(LedgerError, match="Not enough"):
        led.redeem("s1", "r1", 1)
    led.earn("t1", "s1", "READ", 1, measure=200)
    led.earn("t1", "s1", "READ", 2, measure=200)
    led.redeem("s1", "r1", 3)
    assert led.balance("s1") == 5
    led.earn("t1", "s2", "READ", 4, measure=200)
    led.earn("t1", "s2", "READ", 5, measure=200)
    with pytest.raises(LedgerError, match="out of stock"):
        led.redeem("s2", "r1", 6)


def test_parallel_redemptions_cannot_overspend(tmp_path):
    led = ledger(tmp_path)
    led.add_reward(RewardItem("r2", "Sticker", 10, 100))
    led.earn("t1", "s1", "READ", 1, measure=200)  # 10 points: exactly one sticker
    outcomes = []

    def attempt():
        try:
            led.redeem("s1", "r2", 2)
            outcomes.append("ok")
        except LedgerError:
            outcomes.append("refused")

    threads = [threading.Thread(target=attempt) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert outcomes.count("ok") == 1 and led.balance("s1") == 0


def test_reversal_rules(tmp_path):
    led = ledger(tmp_path)
    award = led.earn("t1", "s1", "PART", 1)
    with pytest.raises(LedgerError, match="Only the issuer"):
        led.reverse(award, "t2", 2)
    led.reverse(award, "t1", 2)
    assert led.balance("s1") == 0
    with pytest.raises(LedgerError, match="already reversed"):
        led.reverse(award, "t1", 3)


def test_spent_points_cannot_be_reversed_into_a_negative_balance(tmp_path):
    led = ledger(tmp_path)
    first = led.earn("t1", "s1", "READ", 1, measure=200)
    led.earn("t1", "s1", "READ", 2, measure=200)
    led.redeem("s1", "r1", 3)  # 20 - 15 = 5 left
    with pytest.raises(LedgerError, match="already spent"):
        led.reverse(first, "t1", 4)


def test_round_trip_to_dataset(tmp_path):
    led = ledger(tmp_path)
    led.set_opportunities("s1", "READ", "t1", 4)
    led.earn("t1", "s1", "READ", 1, measure=180)
    data = led.load_dataset()
    assert data.students[0].opportunities == {("READ", "t1"): 4}
    assert data.transactions[0].measure == 180 and data.policies["READ"].objective_measure == "pages"
