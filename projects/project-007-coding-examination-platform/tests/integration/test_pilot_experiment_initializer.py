from datetime import datetime, timezone

from app.persistence.database import Database
from app.persistence.experiment_observation_repository import ExperimentObservationRepository
from app.persistence.experiment_run_repository import ExperimentRunRepository
from app.research.pilot_cases import case_pilot_001
from app.research.pilot_experiment import (
    PILOT_ASSESSOR_RUBRIC_VERSION, PILOT_METHOD_VERSIONS,
    initialize_constructed_experiment,
)


def test_constructed_pilot_initializer_freezes_identity_without_results(tmp_path):
    db = Database(tmp_path / "pilot-exp.db")
    db.initialize()
    started = datetime(2026, 9, 20, 13, 0, tzinfo=timezone.utc)
    initialized = initialize_constructed_experiment(
        db, case_pilot_001(), "EXP-PILOT-001-DRY-001", started
    )

    run = ExperimentRunRepository(db).get(initialized.experiment_run_id)
    assert run.case_id == "CASE-PILOT-001"
    assert run.corpus_version == "PILOT-CC3-v1-candidate"
    assert run.assessor_rubric_version == PILOT_ASSESSOR_RUBRIC_VERSION
    frozen = ExperimentRunRepository(db).method_configurations(run.experiment_run_id)
    assert {c.method for c in frozen} == set(PILOT_METHOD_VERSIONS)
    assert len(ExperimentObservationRepository(db).observations(run.experiment_run_id)) == 0
    assert ExperimentObservationRepository(db).reference(run.experiment_run_id) is None
