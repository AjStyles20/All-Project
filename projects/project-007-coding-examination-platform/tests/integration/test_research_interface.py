from datetime import datetime, timezone

from app.domain.enums import EvidenceState\nfrom app.domain.models import ProgrammingCase, CompetenceClaim\nfrom app.persistence.repositories import P001Repository
from app.domain.experiment_run import ExperimentRun, ExperimentRunStatus, FrozenMethodConfiguration
from app.persistence.database import Database
from app.persistence.experiment_observation_repository import (
    ExperimentObservationRepository, PersistedMethodObservation,
)
from app.persistence.experiment_run_repository import ExperimentRunRepository
from app.services.experiment_record import IndependentReferenceJudgment
from app.services.research_interface import ResearchInterface
from app.services.verification_burden import VerificationBurden


def setup_run(tmp_path):
    db=Database(tmp_path/"interface.db"); db.initialize()
    core=P001Repository(db); runs=ExperimentRunRepository(db); obs=ExperimentObservationRepository(db)\n    core.add_case(ProgrammingCase(\"CASE-I\",\"Interface case\",\"Development fixture\",\"Python\"))\n    core.add_claim(CompetenceClaim(\"CC3\",\"Test Design\",\"Design appropriate tests.\"))
    now=datetime.now(timezone.utc)
    runs.create(ExperimentRun(
        "EXP-I","CASE-I","CC3","DEV-v1","AR-v1",ExperimentRunStatus.ACTIVE,
        started_at=now,
    ))
    for method in ("B0","B1","B2","B3","B4"):
        runs.freeze_method(FrozenMethodConfiguration(
            "EXP-I",method,f"{method}-v1",f"{method}-CFG-v1"
        ))
    return runs,obs,now


def test_inspection_reports_missing_components_without_inventing_data(tmp_path):
    runs,obs,now=setup_run(tmp_path)
    obs.add_method_observation(PersistedMethodObservation(
        "EXP-I","B0",EvidenceState.UNRESOLVED,("EV-A",),
        VerificationBurden(0,0.0,()),now,
    ))
    view=ResearchInterface(runs,obs).inspect_experiment("EXP-I")
    assert view.complete is False
    assert view.missing==("B1","B2","B3","B4","INDEPENDENT_REFERENCE")
    assert view.reference_state is None
    assert view.methods[0].evidence_ids==("EV-A",)


def test_inspection_exposes_b0_b4_burden_and_independent_reference(tmp_path):
    runs,obs,now=setup_run(tmp_path)
    for method in ("B0","B1","B2","B3","B4"):
        burden=VerificationBurden(1,30.0,("MEDIUM",)) if method=="B4" else VerificationBurden(0,0.0,())
        obs.add_method_observation(PersistedMethodObservation(
            "EXP-I",method,EvidenceState.SUPPORTED,(f"EV-{method}",),burden,now,
        ))
    obs.add_reference("EXP-I",IndependentReferenceJudgment(
        "ASSESSOR-01","CC3",EvidenceState.SUPPORTED,"Independent judgment.","AR-v1"
    ),now)
    view=ResearchInterface(runs,obs).inspect_experiment("EXP-I")
    assert view.complete is True and view.missing==()
    assert view.reference_assessor_id=="ASSESSOR-01"
    assert view.reference_state is EvidenceState.SUPPORTED
    b4=next(m for m in view.methods if m.method=="B4")
    assert b4.question_count==1
    assert b4.verification_seconds==30.0
    assert b4.complexity==("MEDIUM",)
