from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.api.research_api import create_research_app
from app.domain.experiment_run import ExperimentRun, ExperimentRunStatus
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
