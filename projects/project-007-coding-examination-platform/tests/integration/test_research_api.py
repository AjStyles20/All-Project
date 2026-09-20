from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.api.research_api import create_research_app
from app.domain.experiment_run import ExperimentRun, ExperimentRunStatus
from app.domain.audit import AuditEvent, AuditEventType
from app.persistence.audit_repository import AuditRepository
from app.domain.models import CompetenceClaim, ProgrammingCase
from app.persistence.database import Database
from app.persistence.experiment_run_repository import ExperimentRunRepository
from app.persistence.repositories import P001Repository


def seed(db_path):
    db = Database(db_path)
    db.initialize()
    core = P001Repository(db)
    core.add_case(ProgrammingCase("CASE-API", "API case", "Development fixture", "Python"))
    core.add_claim(CompetenceClaim("CC3", "Test Design", "Design appropriate tests."))
    ExperimentRunRepository(db).create(ExperimentRun(
        "EXP-API", "CASE-API", "CC3", "DEV-v1", "AR-v1",
        ExperimentRunStatus.ACTIVE, datetime.now(timezone.utc),
    ))


def test_health_is_bounded_to_research_interface(tmp_path):
    path = tmp_path / "api.db"
    client = TestClient(create_research_app(str(path)))
    assert client.get("/health").json() == {
        "status": "ok", "scope": "research-interface"
    }


def test_experiment_endpoint_returns_truthful_incomplete_record(tmp_path):
    path = tmp_path / "api.db"
    seed(path)
    client = TestClient(create_research_app(str(path)))
    response = client.get("/research/experiments/EXP-API")
    assert response.status_code == 200
    payload = response.json()
    assert payload["experiment_run_id"] == "EXP-API"
    assert payload["complete"] is False
    assert payload["missing"] == [
        "B0", "B1", "B2", "B3", "B4", "INDEPENDENT_REFERENCE"
    ]


def test_unknown_experiment_is_404(tmp_path):
    path = tmp_path / "api.db"
    client = TestClient(create_research_app(str(path)))
    response = client.get("/research/experiments/DOES-NOT-EXIST")
    assert response.status_code == 404
    assert response.json()["detail"] == "Unknown experiment run."


def test_audit_endpoint_is_bounded_to_experiment_case_and_claim(tmp_path):
    path = tmp_path / "api.db"
    seed(path)
    db = Database(path)
    audits = AuditRepository(db)
    now = datetime.now(timezone.utc)
    audits.append(AuditEvent(
        "AE-1", "CASE-API", AuditEventType.GAP_DETECTED, now,
        "SYSTEM", "CC3 gap detected.", claim_id="CC3", gap_type="EG-T3",
    ))
    audits.append(AuditEvent(
        "AE-2", "CASE-API", AuditEventType.CONTROL_DECISION, now,
        "SYSTEM", "Different claim event.", claim_id="CC5",
        decision="CONTINUE_VERIFICATION",
    ))
    client = TestClient(create_research_app(str(path)))
    response = client.get("/research/experiments/EXP-API/audit")
    assert response.status_code == 200
    payload = response.json()
    assert payload["case_id"] == "CASE-API"
    assert [event["event_id"] for event in payload["events"]] == ["AE-1"]
    assert payload["events"][0]["gap_type"] == "EG-T3"


def test_reference_endpoint_binds_claim_and_accepts_frozen_rubric(tmp_path):
    path = tmp_path / "api.db"
    seed(path)
    client = TestClient(create_research_app(str(path)))
    response = client.post("/research/experiments/EXP-API/reference", json={
        "assessor_id": "ASSESSOR-01",
        "state": "SUPPORTED",
        "rationale": "Independent rubric-based judgment.",
        "rubric_version": "AR-v1",
    })
    assert response.status_code == 201
    payload = response.json()
    assert payload["claim_id"] == "CC3"
    assert payload["assessor_id"] == "ASSESSOR-01"
    inspected = client.get("/research/experiments/EXP-API").json()
    assert inspected["reference_state"] == "SUPPORTED"
    assert inspected["reference_assessor_id"] == "ASSESSOR-01"


def test_reference_endpoint_rejects_wrong_rubric_and_overwrite(tmp_path):
    path = tmp_path / "api.db"
    seed(path)
    client = TestClient(create_research_app(str(path)))
    wrong = client.post("/research/experiments/EXP-API/reference", json={
        "assessor_id": "ASSESSOR-01",
        "state": "SUPPORTED",
        "rationale": "Wrong rubric attempt.",
        "rubric_version": "AR-WRONG",
    })
    assert wrong.status_code == 409
    assert "rubric" in wrong.json()["detail"].lower()

    first = client.post("/research/experiments/EXP-API/reference", json={
        "assessor_id": "ASSESSOR-01",
        "state": "SUPPORTED",
        "rationale": "First independent judgment.",
        "rubric_version": "AR-v1",
    })
    assert first.status_code == 201

    second = client.post("/research/experiments/EXP-API/reference", json={
        "assessor_id": "ASSESSOR-02",
        "state": "UNRESOLVED",
        "rationale": "Attempted overwrite.",
        "rubric_version": "AR-v1",
    })
    assert second.status_code == 409
    assert "already exists" in second.json()["detail"].lower()
