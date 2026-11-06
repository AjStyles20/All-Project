from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

from p008.app import create_app
from p008.matching import DISCLAIMER, Deal, Investor, Startup, match, rank, says_vs_does

TODAY = date(2026, 11, 6)
H = {"X-Requested-With": "fetch"}


def startup(**kw):
    base = dict(id=1, name="S", sector="fintech", stage="seed", country="NG", raising=500_000, updated=TODAY)
    return Startup(**{**base, **kw})


def investor(**kw):
    base = dict(id=1, name="I", sectors=("fintech",), stages=("seed",), countries=("NG",), check_min=50_000,
                check_max=200_000, deals=(), updated=TODAY)
    return Investor(**{**base, **kw})


def deal(sector="fintech", stage="seed", days=100, verified=True):
    return Deal("c", sector, stage, TODAY - timedelta(days=days), "src", TODAY - timedelta(days=10) if verified else None)


# ---------- matching ----------

def test_every_criterion_has_a_reason_and_full_fit_scores_one():
    m = match(startup(), investor(deals=(deal(), deal())), TODAY)
    assert m.score == 1.0 and all(c.reason for c in m.components)
    assert {c.name for c in m.components} == {"sector", "stage", "region", "cheque size", "recent deals"}


def test_unknown_is_not_zero():
    m = match(startup(country=None, raising=None), investor(), TODAY)
    unknown = {c.name for c in m.components if c.score is None}
    assert {"region", "cheque size", "recent deals"} <= unknown
    assert m.score == 1.0          # unknowns are left out, not counted as misses
    assert m.confidence == "low"   # ... but they lower confidence


def test_adjacent_stage_partly_fits_and_far_stage_does_not():
    assert next(c for c in match(startup(stage="series-a"), investor(), TODAY).components if c.name == "stage").score == 0.5
    assert next(c for c in match(startup(stage="growth"), investor(), TODAY).components if c.name == "stage").score == 0.0


def test_says_vs_does_needs_evidence_and_flags_disagreement():
    assert says_vs_does(investor(deals=(deal("health", "series-a"),) * 3), TODAY) == []     # too few deals
    notes = says_vs_does(investor(deals=(deal("health", "series-a"),) * 5), TODAY)
    assert any("series-a" in n for n in notes) and any("health" in n for n in notes)
    old = says_vs_does(investor(deals=(deal("health", "series-a", days=2000),) * 5), TODAY)
    assert old == []                 # deals older than three years do not count


def test_stale_and_unverified_data_warn():
    m = match(startup(), investor(updated=TODAY - timedelta(days=400), deals=(deal(verified=False), deal())), TODAY)
    assert any("may be out of date" in w for w in m.warnings)
    assert any("not been verified" in w for w in m.warnings)
    assert m.confidence != "high"


def test_ranking_is_stable_and_puts_unknown_last():
    invs = [investor(id=1, name="B", sectors=("health",)), investor(id=2, name="A"),
            investor(id=3, name="C", sectors=(), stages=(), countries=(), check_min=None, check_max=None)]
    order = [m.investor_id for m in rank(startup(country=None, raising=None), invs, TODAY)]
    assert order == [2, 1, 3]


def test_disclaimer_says_it_is_not_a_prediction():
    assert "do not predict" in DISCLAIMER


# ---------- app ----------

def app(tmp_path):
    return TestClient(create_app(tmp_path / "m.sqlite3", today=TODAY), base_url="http://127.0.0.1")


def signup(c, role, email, name="X"):
    r = c.post("/api/register", headers=H, json={"email": email, "password": "correct horse 1", "role": role, "name": name})
    assert r.status_code == 201, r.text
    return c


def test_state_changes_need_the_header(tmp_path):
    c = app(tmp_path)
    assert c.post("/api/register", json={"email": "a@b.co", "password": "x" * 12, "role": "founder", "name": "n"}).status_code == 403


def test_accounts_passwords_and_throttling(tmp_path):
    c = signup(app(tmp_path), "founder", "f@demo.test")
    assert c.post("/api/register", headers=H, json={"email": "F@demo.test", "password": "x" * 12, "role": "founder", "name": "n"}).status_code == 409
    c.post("/api/logout", headers=H)
    assert c.get("/api/me").json() == {"role": None}
    assert c.get("/api/matches").status_code == 401
    for _ in range(5):
        assert c.post("/api/login", headers=H, json={"email": "f@demo.test", "password": "wrong-password"}).status_code == 401
    assert c.post("/api/login", headers=H, json={"email": "f@demo.test", "password": "correct horse 1"}).status_code == 429
    other = TestClient(create_app(tmp_path / "other.sqlite3", today=TODAY), base_url="http://127.0.0.1")
    cookie = signup(other, "investor", "i@demo.test").cookies
    assert "sm_session" in cookie


def test_full_flow_with_contact_privacy(tmp_path):
    db = tmp_path / "flow.sqlite3"
    founder = TestClient(create_app(db, today=TODAY), base_url="http://127.0.0.1")
    inv = TestClient(create_app(db, today=TODAY), base_url="http://127.0.0.1")
    signup(founder, "founder", "f@demo.test", "Lumen")
    signup(inv, "investor", "i@demo.test", "Harbour")
    assert founder.put("/api/startup", headers=H, json={"name": "Lumen", "sector": "fintech", "stage": "seed", "country": "NG",
                                                         "raising": 500000, "contact": "secret-founder@x.test"}).status_code == 200
    assert inv.put("/api/investor", headers=H, json={"name": "Harbour", "sectors": ["fintech"], "stages": ["seed"], "countries": ["NG"],
                                                      "check_min": 50000, "check_max": 200000, "contact": "secret-investor@x.test"}).status_code == 200
    assert inv.post("/api/deals", headers=H, json={"company": "K", "sector": "fintech", "stage": "seed", "on_date": "2026-05-01",
                                                    "source": "press release"}).status_code == 201
    m = founder.get("/api/matches").json()
    assert m["matches"][0]["name"] == "Harbour" and m["matches"][0]["score"] > 0.9 and "do not predict" in m["disclaimer"]
    iid = m["matches"][0]["investor_id"]
    intro = founder.post("/api/intros", headers=H, json={"investor_id": iid, "message": "We fit your seed fintech focus."}).json()["id"]
    assert founder.post("/api/intros", headers=H, json={"investor_id": iid, "message": "Second request please"}).status_code == 409
    seen = inv.get("/api/intros").json()[0]
    assert seen["their_contact"] is None and "secret" not in str(seen)          # hidden before acceptance
    assert inv.post(f"/api/intros/{intro}/messages", headers=H, json={"text": "hi"}).status_code == 409
    assert founder.post(f"/api/intros/{intro}/status", headers=H, json={"status": "accepted"}).status_code == 403
    assert inv.post(f"/api/intros/{intro}/status", headers=H, json={"status": "accepted"}).json()["their_contact"] == "secret-founder@x.test"
    assert founder.get("/api/intros").json()[0]["their_contact"] == "secret-investor@x.test"
    assert inv.post(f"/api/intros/{intro}/messages", headers=H, json={"text": "Let's talk Tuesday"}).status_code == 201
    assert founder.get(f"/api/intros/{intro}/messages").json()[0]["text"] == "Let's talk Tuesday"


def test_outsiders_cannot_see_or_touch_an_intro(tmp_path):
    db = tmp_path / "o.sqlite3"
    f = TestClient(create_app(db, today=TODAY), base_url="http://127.0.0.1")
    i = TestClient(create_app(db, today=TODAY), base_url="http://127.0.0.1")
    other = TestClient(create_app(db, today=TODAY), base_url="http://127.0.0.1")
    signup(f, "founder", "f@demo.test"); signup(i, "investor", "i@demo.test"); signup(other, "investor", "o@demo.test")
    iid = i.get("/api/me").json()["profile"]["id"]
    intro = f.post("/api/intros", headers=H, json={"investor_id": iid, "message": "hello there investor"}).json()["id"]
    assert other.get(f"/api/intros/{intro}/messages").status_code == 404
    assert other.post(f"/api/intros/{intro}/status", headers=H, json={"status": "accepted"}).status_code == 404
    assert other.get("/api/intros").json() == []
    assert f.get("/api/startups").status_code == 403            # founders cannot list startups
    assert i.get("/api/matches").status_code == 403             # investors have no founder matches


def test_validation(tmp_path):
    c = signup(app(tmp_path), "investor", "i@demo.test")
    assert c.put("/api/investor", headers=H, json={"name": "x", "sectors": ["crypto-casino"]}).status_code == 422
    assert c.put("/api/investor", headers=H, json={"name": "x", "check_min": 10, "check_max": 5}).status_code == 422
    assert c.post("/api/deals", headers=H, json={"company": "x", "sector": "fintech", "stage": "seed", "on_date": "not-a-date",
                                                  "source": "s"}).status_code == 422


def test_daily_intro_limit(tmp_path):
    from p008.store import Store, StoreError
    s = Store(tmp_path / "l.sqlite3")
    uid = s.register("f@demo.test", "x" * 12, "founder"); s.save_startup(uid, {"name": "S"})
    st = s.startup_row(owner_id=uid)["id"]
    invs = []
    for n in range(11):
        u = s.register(f"i{n}@demo.test", "x" * 12, "investor"); s.save_investor(u, {"name": f"I{n}"})
        invs.append(s.investor_row(owner_id=u)["id"])
    for n in range(10):
        s.create_intro(st, invs[n], "hello there")
    with pytest.raises(StoreError):
        s.create_intro(st, invs[10], "hello there")
