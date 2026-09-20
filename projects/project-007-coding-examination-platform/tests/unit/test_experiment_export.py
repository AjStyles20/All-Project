import json
from datetime import datetime, timezone

from app.domain.enums import EvidenceState
from app.domain.experiment_run import ExperimentRun
from app.persistence.database import Database
from app.persistence.experiment_observation_repository import ExperimentObservationRepository
from app.persistence.experiment_run_repository import ExperimentRunRepository
from app.services.experiment_export import ExperimentExporter
from app.services.research_interface import ResearchInterface


def test_export_is_machine_readable_and_preserves_missing_components(tmp_path):
    db=Database(tmp_path/"export.db"); db.initialize()
    runs=ExperimentRunRepository(db); observations=ExperimentObservationRepository(db)
    runs.create(ExperimentRun(
        "EXP-X","CASE-X","CC3","DEV-v1","AR-v1",
        started_at=datetime.now(timezone.utc),
    ))
    exporter=ExperimentExporter(ResearchInterface(runs,observations))
    payload=json.loads(exporter.as_json("EXP-X"))
    assert payload["experiment_run_id"]=="EXP-X"
    assert payload["methods"]==[]
    assert payload["reference_state"] is None
    assert payload["complete"] is False
    assert payload["missing"]==["B0","B1","B2","B3","B4","INDEPENDENT_REFERENCE"]
