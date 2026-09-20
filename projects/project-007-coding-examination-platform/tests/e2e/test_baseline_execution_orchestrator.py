from datetime import datetime, timezone
import pytest

from app.domain.enums import ClaimApplicability, EvidenceType
from app.domain.models import CaseClaim, CompetenceClaim, EvidenceItem, ProgrammingCase
from app.persistence.database import Database
from app.persistence.experiment_observation_repository import ExperimentObservationRepository
from app.persistence.experiment_run_repository import ExperimentRunRepository
from app.persistence.repositories import P001Repository
from app.services.experiment_orchestrator import ExperimentOrchestrator
from app.services.verification_burden import VerificationBurden


def setup(tmp_path):
    db=Database(tmp_path/"baseline-exec.db"); db.initialize()
    d=P001Repository(db)
    d.add_case(ProgrammingCase("CASE-DEV-003","Case","Task","python"))
    d.add_claim(CompetenceClaim("CC3","Test Design","Design useful tests."))
    d.add_case_claim(CaseClaim("CASE-DEV-003","CC3",ClaimApplicability.REQUIRED))
    svc=ExperimentOrchestrator(ExperimentRunRepository(db),ExperimentObservationRepository(db))
    svc.start(
        experiment_run_id="EXP-1",case_id="CASE-DEV-003",claim_id="CC3",
        corpus_version="DEV-v1",assessor_rubric_version="AR-v1",
        method_versions={m:(f"{m}-v1",f"{m}-CFG-v1") for m in ("B0","B1","B2","B3","B4")},
        started_at=datetime.now(timezone.utc),
    )
    return svc


def ev(i,t,source):
    return EvidenceItem(i,"CASE-DEV-003",t,i,source,datetime.now(timezone.utc))


def test_executes_b0_b3_from_same_collection_and_persists_boundaries(tmp_path):
    svc=setup(tmp_path); now=datetime.now(timezone.utc)
    evidence=[
        ev("A",EvidenceType.ARTIFACT,"submission"),
        ev("P",EvidenceType.PROCESS,"process_log"),
        ev("FV",EvidenceType.VERIFICATION,"fixed_viva"),
        ev("TV",EvidenceType.VERIFICATION,"targeted_verification"),
    ]
    rows=svc.execute_b0_b3(
        experiment_run_id="EXP-1",case_id="CASE-DEV-003",claim_id="CC3",
        evidence=evidence,recorded_at=now,
        b2_burden=VerificationBurden(4,120.0,("MEDIUM",)*4),
    )
    by={r.method:r for r in rows}
    assert by["B0"].evidence_ids==("A",)
    assert by["B1"].evidence_ids==("A","P")
    assert by["B2"].evidence_ids==("A","P","FV")
    assert by["B3"].evidence_ids==("A","P")
    assert "TV" not in by["B2"].evidence_ids
    assert by["B2"].burden.question_count==4
    assert len(svc.observations.observations("EXP-1"))==4


def test_b2_verification_cannot_be_recorded_with_invented_zero_burden(tmp_path):
    svc=setup(tmp_path)
    with pytest.raises(ValueError,match="requires measured burden"):
        svc.execute_b0_b3(
            experiment_run_id="EXP-1",case_id="CASE-DEV-003",claim_id="CC3",
            evidence=[ev("FV",EvidenceType.VERIFICATION,"fixed_viva")],
            recorded_at=datetime.now(timezone.utc),
        )


def test_execution_rejects_case_claim_mismatch(tmp_path):
    svc=setup(tmp_path)
    with pytest.raises(ValueError,match="frozen experiment"):
        svc.execute_b0_b3(
            experiment_run_id="EXP-1",case_id="CASE-OTHER",claim_id="CC3",
            evidence=[],recorded_at=datetime.now(timezone.utc),
        )
