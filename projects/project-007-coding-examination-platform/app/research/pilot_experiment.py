"""Constructed M8 experiment initialization.

Creates reproducible ACTIVE experiment runs only. It does not create assessor
judgments, method outcomes, timings, or claims that a pilot occurred.
"""
from dataclasses import dataclass
from datetime import datetime, timezone

from app.persistence.database import Database
from app.persistence.experiment_observation_repository import ExperimentObservationRepository
from app.persistence.experiment_run_repository import ExperimentRunRepository
from app.persistence.repositories import P001Repository
from app.research.pilot_cases import PilotCaseBundle, load_bundle
from app.services.experiment_orchestrator import ExperimentOrchestrator


PILOT_ASSESSOR_RUBRIC_VERSION = "CC3-ASSESSOR-v1-candidate"
PILOT_METHOD_VERSIONS = {
    "B0": ("B0-v1-development", "PILOT-CC3-v1-candidate"),
    "B1": ("B1-v1-development", "PILOT-CC3-v1-candidate"),
    "B2": ("B2-FIXED-VIVA-v1.0-development", "PILOT-CC3-v1-candidate"),
    "B3": ("B3-v1-development", "PILOT-CC3-v1-candidate"),
    "B4": ("B4-EGPCV-v1-development", "PILOT-CC3-v1-candidate"),
}


@dataclass(frozen=True)
class InitializedPilotExperiment:
    experiment_run_id: str
    case_id: str
    claim_id: str
    corpus_version: str
    assessor_rubric_version: str


def initialize_constructed_experiment(
    database: Database, bundle: PilotCaseBundle, experiment_run_id: str,
    started_at: datetime | None = None,
) -> InitializedPilotExperiment:
    """Load a constructed case and freeze a B0-B4 experiment identity."""
    core = P001Repository(database)
    load_bundle(core, bundle)
    runs = ExperimentRunRepository(database)
    observations = ExperimentObservationRepository(database)
    orchestrator = ExperimentOrchestrator(runs, observations)
    start_time = started_at or datetime.now(timezone.utc)
    run = orchestrator.start(
        experiment_run_id=experiment_run_id,
        case_id=bundle.case.case_id,
        claim_id=bundle.claim.claim_id,
        corpus_version=bundle.corpus_version,
        assessor_rubric_version=PILOT_ASSESSOR_RUBRIC_VERSION,
        method_versions=PILOT_METHOD_VERSIONS,
        started_at=start_time,
    )
    return InitializedPilotExperiment(
        run.experiment_run_id, run.case_id, run.claim_id,
        run.corpus_version, run.assessor_rubric_version,
    )
