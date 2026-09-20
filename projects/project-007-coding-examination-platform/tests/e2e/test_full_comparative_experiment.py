from datetime import datetime, timezone

from app.domain.enums import ClaimApplicability, EvidenceState, EvidenceType
from app.domain.models import CaseClaim, ClaimEvidenceLink, CompetenceClaim, EvidenceItem, ProgrammingCase
from app.persistence.audit_repository import AuditRepository
from app.persistence.database import Database
from app.persistence.experiment_observation_repository import ExperimentObservationRepository
from app.persistence.experiment_run_repository import ExperimentRunRepository
from app.persistence.probe_audit_repository import ProbeAuditRepository
from app.persistence.repositories import P001Repository
from app.persistence.verification_run_repository import VerificationRunRepository
from app.services.b4_orchestrator import B4Orchestrator
from app.services.cc3_response_evaluator import CC3ProbeResponse
from app.services.experiment_orchestrator import ExperimentOrchestrator
from app.services.experiment_record import IndependentReferenceJudgment
from app.services.verification_burden import VerificationBurden


def test_one_experiment_persists_b0_b4_and_independent_reference(tmp_path):
    db=Database(tmp_path/"full-experiment.db"); db.initialize()
    domain=P001Repository(db)
    domain.add_case(ProgrammingCase("CASE-DEV-003","Find even numbers","Return evens.","python"))
    domain.add_claim(CompetenceClaim("CC3","Test Design","Design useful tests."))
    domain.add_case_claim(CaseClaim("CASE-DEV-003","CC3",ClaimApplicability.REQUIRED))
    supplied=EvidenceItem(
        "EV-EXEC","CASE-DEV-003",EvidenceType.EXECUTION,"Supplied tests passed.",
        "automated_test",datetime.now(timezone.utc),
    )
    domain.add_evidence(supplied)
    domain.link_evidence(ClaimEvidenceLink(
        "CASE-DEV-003","CC3","EV-EXEC","Relevant but insufficient.",
    ))

    experiments=ExperimentOrchestrator(
        ExperimentRunRepository(db),ExperimentObservationRepository(db)
    )
    now=datetime.now(timezone.utc)
    experiments.start(
        experiment_run_id="EXP-1",case_id="CASE-DEV-003",claim_id="CC3",
        corpus_version="DEV-v1",assessor_rubric_version="AR-v1",
        method_versions={m:(f"{m}-v1",f"{m}-CFG-v1") for m in ("B0","B1","B2","B3","B4")},
        started_at=now,
    )
    experiments.execute_b0_b3(
        experiment_run_id="EXP-1",case_id="CASE-DEV-003",claim_id="CC3",
        evidence=[supplied],recorded_at=now,
    )

    b4=B4Orchestrator(
        domain,VerificationRunRepository(db),AuditRepository(db),ProbeAuditRepository(db)
    )
    b4obs=experiments.execute_b4_cc3(
        experiment_run_id="EXP-1",b4=b4,verification_run_id="VR-1",
        response=CC3ProbeResponse(
            "[1,3,5]","[]","Checks no-even boundary.",True,True,True,
        ),
        evidence_id="EV-B4-1",started_at=now,recorded_at=now,
        burden=VerificationBurden(1,30.0,("MEDIUM",)),
    )
    assert b4obs.system_state is EvidenceState.SUPPORTED
    assert b4obs.evidence_ids==("EV-B4-1",)

    observations=experiments.observations.observations("EXP-1")
    assert tuple(o.method for o in observations)==("B0","B1","B2","B3","B4")
    assert next(o for o in observations if o.method=="B4").burden.question_count==1

    experiments.record_reference("EXP-1",IndependentReferenceJudgment(
        "ASSESSOR-01","CC3",EvidenceState.SUPPORTED,"Independent judgment.","AR-v1",
    ),now)
    ready,missing=experiments.completion_readiness("EXP-1")
    assert ready is True and missing==()
    experiments.complete("EXP-1",now)
    assert experiments.runs.get("EXP-1").status.value=="COMPLETE"
