from datetime import datetime, timezone

from app.persistence.database import Database
from app.persistence.experiment_run_repository import ExperimentRunRepository
from app.research.pilot_cases import case_pilot_001
from app.research.pilot_experiment import initialize_constructed_experiment
from app.research.pilot_readiness import DryRunReadinessValidator


def _initialized(tmp_path):
    db = Database(tmp_path / "ready.db")
    db.initialize()
    bundle = case_pilot_001()
    initialize_constructed_experiment(
        db, bundle, "EXP-PILOT-001-DRY-READY",
        datetime(2026, 9, 20, 14, 0, tzinfo=timezone.utc),
    )
    return db, bundle


def test_ready_only_when_frozen_identity_and_timing_procedure_exist(tmp_path):
    db, bundle = _initialized(tmp_path)
    result = DryRunReadinessValidator(ExperimentRunRepository(db)).validate(
        experiment_run_id="EXP-PILOT-001-DRY-READY",
        bundle=bundle,
        timing_procedure_version="TIMER-v1",
    )
    assert result.ready is True
    assert result.missing_or_invalid == ()


def test_missing_timing_procedure_blocks_readiness(tmp_path):
    db, bundle = _initialized(tmp_path)
    result = DryRunReadinessValidator(ExperimentRunRepository(db)).validate(
        experiment_run_id="EXP-PILOT-001-DRY-READY",
        bundle=bundle,
        timing_procedure_version=None,
    )
    assert result.ready is False
    assert "timing_procedure_version" in result.missing_or_invalid


def test_unknown_experiment_cannot_be_declared_ready(tmp_path):
    db = Database(tmp_path / "ready.db")
    db.initialize()
    result = DryRunReadinessValidator(ExperimentRunRepository(db)).validate(
        experiment_run_id="MISSING", bundle=case_pilot_001(),
        timing_procedure_version="TIMER-v1",
    )
    assert result == type(result)(False, ("experiment_run",))
