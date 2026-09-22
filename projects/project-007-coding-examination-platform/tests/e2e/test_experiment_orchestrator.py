from datetime import datetime, timezone
import pytest

from app.domain.enums import ClaimApplicability, EvidenceState
from app.domain.models import CaseClaim, CompetenceClaim, ProgrammingCase
from app.persistence.database import Database
from app.persistence.experiment_observation_repository import (
    ExperimentObservationRepository, PersistedMethodObservation,
)
from app.persistence.experiment_run_repository import ExperimentRunRepository
from app.persistence.repositories import P001Repository
from app.services.experiment_orchestrator import ExperimentOrchestrator
from app.services.experiment_record import IndependentReferenceJudgment
from app.services.verification_burden import VerificationBurden


def setup(tmp_path):
    db=Database(tmp_path/"orchestrator.db"); db.initialize()
    domain=P001Repository(db)
    domain.add_case(ProgrammingCase("CASE-DEV-003","Case","Task","python"))
    domain.add_claim(CompetenceClaim("CC3","Test Design","Design useful tests."))
    domain.add_case_claim(CaseClaim("CASE-DEV-003","CC3",ClaimApplicability.REQUIRED))
    return ExperimentOrchestrator(
        ExperimentRunRepository(db), ExperimentObservationRepository(db)
    )


def versions():
    return {m:(f"{m}-v1.0-development",f"{m}-CFG-v1.0") for m in ("B0","B1","B2","B3","B4")}


def test_requires_exact_b0_b4_freeze(tmp_path):
    svc=setup(tmp_path); bad=versions(); bad.pop("B3")
    with pytest.raises(ValueError,match="exactly B0-B4"):
        svc.start(
            experiment_run_id="EXP-1",case_id="CASE-DEV-003",claim_id="CC3",
            corpus_version="DEV-v1",assessor_rubric_version="AR-v1",
            method_versions=bad,started_at=datetime.now(timezone.utc),
        )


def test_refuses_completion_until_all_methods_and_reference_exist(tmp_path):
    svc=setup(tmp_path); now=datetime.now(timezone.utc)
    svc.start(
        experiment_run_id="EXP-1",case_id="CASE-DEV-003",claim_id="CC3",
        corpus_version="DEV-v1",assessor_rubric_version="AR-v1",
        method_versions=versions(),started_at=now,
    )
    svc.record_method(PersistedMethodObservation(
        "EXP-1","B0",EvidenceState.UNRESOLVED,("EV-A",),
        VerificationBurden(0,0.0,()),now,
    ))
    ready,missing=svc.completion_readiness("EXP-1")
    assert ready is False
    assert "method:B1" in missing and "independent_reference" in missing
    with pytest.raises(ValueError,match="Experiment incomplete"):
        svc.complete("EXP-1",now)


def test_complete_experiment_requires_b0_b4_and_independent_reference(tmp_path):
    svc=setup(tmp_path); now=datetime.now(timezone.utc)
    svc.start(
        experiment_run_id="EXP-1",case_id="CASE-DEV-003",claim_id="CC3",
        corpus_version="DEV-v1",assessor_rubric_version="AR-v1",
        method_versions=versions(),started_at=now,
    )
    for method in ("B0","B1","B2","B3","B4"):
        q=4 if method=="B2" else (1 if method=="B4" else 0)
        complexity=("MEDIUM",)*q
        svc.record_method(PersistedMethodObservation(
            "EXP-1",method,EvidenceState.SUPPORTED if method in ("B2","B4") else EvidenceState.UNRESOLVED,
            ("EV-A",),VerificationBurden(q,float(q*30),complexity),now,
        ))
    svc.record_reference("EXP-1",IndependentReferenceJudgment(
        "ASSESSOR-01","CC3",EvidenceState.SUPPORTED,"Independent rubric judgment.","AR-v1",
    ),now)
    ready,missing=svc.completion_readiness("EXP-1")
    assert ready is True and missing==()
    svc.complete("EXP-1",now)
    assert svc.runs.get("EXP-1").status.value=="COMPLETE"


def test_completed_experiment_rejects_late_observation(tmp_path):
    svc=setup(tmp_path); now=datetime.now(timezone.utc)
    svc.start(
        experiment_run_id="EXP-1",case_id="CASE-DEV-003",claim_id="CC3",
        corpus_version="DEV-v1",assessor_rubric_version="AR-v1",
        method_versions=versions(),started_at=now,
    )
    for method in ("B0","B1","B2","B3","B4"):
        svc.record_method(PersistedMethodObservation(
            "EXP-1",method,EvidenceState.UNRESOLVED,(),
            VerificationBurden(0,0.0,()),now,
        ))
    svc.record_reference("EXP-1",IndependentReferenceJudgment(
        "A","CC3",EvidenceState.UNRESOLVED,"Independent judgment.","AR-v1",
    ),now)
    svc.complete("EXP-1",now)
    with pytest.raises(ValueError,match="ACTIVE"):
        svc.record_method(PersistedMethodObservation(
            "EXP-1","B0",EvidenceState.SUPPORTED,(),
            VerificationBurden(0,0.0,()),now,
        ))
