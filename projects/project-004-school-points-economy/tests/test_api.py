from fastapi.testclient import TestClient

from p007.api import create_app


def client(tmp_path):
    return TestClient(create_app(tmp_path / "api.sqlite3"))


def test_demo_load_then_audit_shows_states_and_evidence(tmp_path):
    c = client(tmp_path)
    assert c.post("/api/demo", json={"scenario": "S6", "seed": 2}).status_code == 201
    report = c.get("/api/audit", params={"engine": "B4"}).json()
    assert report["state"] == "INSUFFICIENT CONTEXT"
    assert report["findings"][0]["missing_context"]
    # The audit response never names the scenario that generated the data.
    assert "S6" not in str(report)


def test_demo_refuses_a_ledger_that_holds_data(tmp_path):
    c = client(tmp_path)
    c.post("/api/demo", json={"scenario": "S0"})
    assert c.post("/api/demo", json={"scenario": "S1"}).status_code == 409


def test_earn_redeem_reverse_through_the_api(tmp_path):
    c = client(tmp_path)
    c.post("/api/demo", json={"scenario": "S0"})
    before = {r["student_id"]: r["balance"] for r in c.get("/api/students").json()}["A000"]
    award = c.post("/api/earn", json={"issuer_id": "T1", "student_id": "A000", "policy_id": "READ", "measure": 250})
    assert award.status_code == 201
    assert c.post("/api/earn", json={"issuer_id": "T3", "student_id": "A000", "policy_id": "READ",
                                     "measure": 250}).status_code == 409
    assert c.post("/api/reverse", json={"transaction_id": award.json()["transaction_id"],
                                        "issuer_id": "T1"}).status_code == 201
    after = {r["student_id"]: r["balance"] for r in c.get("/api/students").json()}["A000"]
    assert after == before


def test_input_is_validated(tmp_path):
    c = client(tmp_path)
    assert c.get("/api/audit", params={"engine": "B9"}).status_code == 422
    assert c.post("/api/demo", json={"scenario": "S9"}).status_code == 422
    assert c.post("/api/earn", json={"issuer_id": "", "student_id": "x", "policy_id": "y"}).status_code == 422


def test_dashboard_is_served_with_a_strict_csp(tmp_path):
    response = client(tmp_path).get("/")
    assert response.status_code == 200 and "School Points" in response.text
    assert "default-src 'self'" in response.headers["content-security-policy"]
