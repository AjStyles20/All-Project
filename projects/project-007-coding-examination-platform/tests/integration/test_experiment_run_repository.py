from datetime import datetime, timezone

import pytest

from app.domain.enums import ClaimApplicability
from app.domain.experiment_run import (
    ExperimentRun, ExperimentRunStatus, FrozenMethodConfiguration,
)
from app.domain.models import CaseClaim, CompetenceClaim, ProgrammingCase
from app.persistence.database import Database
from app.persistence.experiment_run_repository import ExperimentRunRepository
from app.persistence.repositories import P001Repository


def setup_repo(tmp_path):
    db = Database(tmp_path / "experiment.db")
    db.initialize()
    domain = P001Repository(db)
    domain.add_case(ProgrammingCase(
        case_id="CASE-DEV-003", title="Find even numbers",
        task_description="Return even numbers.", language="python",
    ))
    domain.add_claim(CompetenceClaim(
        claim_id="CC3", name="Test Design", definition="Design useful tests.",
    ))
    domain.add_case_claim(CaseClaim(
        case_id="CASE-DEV-003", claim_id="CC3",
        applicability=ClaimApplicability.REQUIRED,
    ))
    return ExperimentRunRepository(db)


def test_experiment_run_persists_identity_and_frozen_b0_b4_versions(tmp_path):
    repo = setup_repo(tmp_path)
    started = datetime(2026, 9, 20, 13, 0, tzinfo=timezone.utc)
    repo.create(ExperimentRun(
        experiment_run_id="EXP-003-01", case_id="CASE-DEV-003", claim_id="CC3",
        corpus_version="DEV-CORPUS-v1.0",
        assessor_rubric_version="ASSESSOR-RUBRIC-v1.0",
        status=ExperimentRunStatus.ACTIVE, started_at=started,
    ))
    for method in ("B0", "B1", "B2", "B3", "B4"):
        repo.freeze_method(FrozenMethodConfiguration(
            experiment_run_id="EXP-003-01", method=method,
            method_version=f"{method}-v1.0-development",
            configuration_version=f"{method}-CONFIG-v1.0",
        ))

    stored = repo.get("EXP-003-01")
    assert stored is not None
    assert stored.status is ExperimentRunStatus.ACTIVE
    configs = repo.method_configurations("EXP-003-01")
    assert tuple(c.method for c in configs) == ("B0", "B1", "B2", "B3", "B4")


def test_same_method_cannot_be_refrozen_inside_one_experiment(tmp_path):
    repo = setup_repo(tmp_path)
    repo.create(ExperimentRun(
        experiment_run_id="EXP-003-01", case_id="CASE-DEV-003", claim_id="CC3",
        corpus_version="DEV-CORPUS-v1.0",
        assessor_rubric_version="ASSESSOR-RUBRIC-v1.0",
        status=ExperimentRunStatus.ACTIVE,
        started_at=datetime.now(timezone.utc),
    ))
    config = FrozenMethodConfiguration("EXP-003-01", "B2", "B2-v1", "CFG-1")
    repo.freeze_method(config)
    with pytest.raises(Exception):
        repo.freeze_method(config)


def test_experiment_run_can_finish_only_once(tmp_path):
    repo = setup_repo(tmp_path)
    repo.create(ExperimentRun(
        experiment_run_id="EXP-003-01", case_id="CASE-DEV-003", claim_id="CC3",
        corpus_version="DEV-CORPUS-v1.0",
        assessor_rubric_version="ASSESSOR-RUBRIC-v1.0",
        status=ExperimentRunStatus.ACTIVE,
        started_at=datetime.now(timezone.utc),
    ))
    ended = datetime.now(timezone.utc)
    repo.finish("EXP-003-01", ended)
    assert repo.get("EXP-003-01").status is ExperimentRunStatus.COMPLETE
    with pytest.raises(ValueError, match="not ACTIVE"):
        repo.finish("EXP-003-01", ended)
