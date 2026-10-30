from datetime import datetime, timezone
import pytest

from app.domain.enums import ClaimApplicability, EvidenceState
from app.domain.experiment_run import ExperimentRun, ExperimentRunStatus, FrozenMethodConfiguration
from app.domain.models import CaseClaim, CompetenceClaim, ProgrammingCase
from app.persistence.database import Database
from app.persistence.experiment_observation_repository import (
    ExperimentObservationRepository, PersistedMethodObservation,
)
from app.persistence.experiment_run_repository import ExperimentRunRepository
from app.persistence.repositories import P001Repository
from app.services.experiment_record import IndependentReferenceJudgment
from app.services.verification_burden import VerificationBurden


def setup(tmp_path):
    db=Database(tmp_path/"observations.db"); db.initialize()
    domain=P001Repository(db)
    domain.add_case(ProgrammingCase("CASE-DEV-003","Case","Task","python"))
    domain.add_claim(CompetenceClaim("CC3","Test Design","Design tests."))
    domain.add_case_claim(CaseClaim("CASE-DEV-003","CC3",ClaimApplicability.REQUIRED))
    runs=ExperimentRunRepository(db)
    runs.create(ExperimentRun(
        "EXP-1","CASE-DEV-003","CC3","DEV-CORPUS-v1.0","ASSESSOR-RUBRIC-v1.0",
        ExperimentRunStatus.ACTIVE,datetime.now(timezone.utc),
    ))
    for method in ("B0","B1","B2","B3","B4"):
        runs.freeze_method(FrozenMethodConfiguration("EXP-1",method,f"{method}-v1","CFG-v1"))
    return ExperimentObservationRepository(db)


def test_persists_method_state_evidence_and_separate_burden_dimensions(tmp_path):
    repo=setup(tmp_path); now=datetime.now(timezone.utc)
    repo.add_method_observation(PersistedMethodObservation(
        "EXP-1","B2",EvidenceState.SUPPORTED,("EV-A","EV-V"),
        VerificationBurden(4,123.5,("MEDIUM",)*4),now,
    ))
    row=repo.observations("EXP-1")[0]
    assert row.method=="B2" and row.system_state is EvidenceState.SUPPORTED
    assert row.evidence_ids==("EV-A","EV-V")
    assert row.burden.question_count==4
    assert row.burden.verification_seconds==123.5


def test_observation_requires_method_to_be_frozen_for_run(tmp_path):
    repo=setup(tmp_path)
    with pytest.raises(Exception):
        repo.add_method_observation(PersistedMethodObservation(
            "EXP-1","B9",EvidenceState.UNRESOLVED,(),
            VerificationBurden(0,0.0,()),datetime.now(timezone.utc),
        ))


def test_reference_must_match_frozen_claim_and_rubric(tmp_path):
    repo=setup(tmp_path); now=datetime.now(timezone.utc)
    good=IndependentReferenceJudgment(
        "ASSESSOR-01","CC3",EvidenceState.SUPPORTED,"Independent judgment.",
        "ASSESSOR-RUBRIC-v1.0",
    )
    repo.add_reference("EXP-1",good,now)
    bad=IndependentReferenceJudgment(
        "ASSESSOR-02","CC3",EvidenceState.SUPPORTED,"Wrong rubric.","OTHER-RUBRIC",
    )
    with pytest.raises(ValueError,match="frozen experiment rubric"):
        repo.add_reference("EXP-1",bad,now)


def test_same_method_observation_cannot_be_silently_overwritten(tmp_path):
    repo=setup(tmp_path); now=datetime.now(timezone.utc)
    observation=PersistedMethodObservation(
        "EXP-1","B0",EvidenceState.UNRESOLVED,("EV-A",),
        VerificationBurden(0,0.0,()),now,
    )
    repo.add_method_observation(observation)
    with pytest.raises(Exception):
        repo.add_method_observation(observation)
