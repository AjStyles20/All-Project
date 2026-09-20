"""Cohesive M6 skeleton for reproducible P001 comparative experiments.

This service freezes B0-B4 configuration identity, records method observations,
and refuses completion until all five methods plus an independent reference
judgment are present. It does not claim comparative superiority.
"""
from datetime import datetime
import sqlite3

from app.domain.experiment_run import (
    ExperimentRun, ExperimentRunStatus, FrozenMethodConfiguration,
)
from app.persistence.experiment_observation_repository import (
    ExperimentObservationRepository, PersistedMethodObservation,
)
from app.persistence.experiment_run_repository import ExperimentRunRepository
from app.services.experiment_record import IndependentReferenceJudgment


REQUIRED_METHODS = ("B0", "B1", "B2", "B3", "B4")


class ExperimentOrchestrator:
    def __init__(self, runs: ExperimentRunRepository, observations: ExperimentObservationRepository):
        self.runs = runs
        self.observations = observations

    def start(
        self, *, experiment_run_id: str, case_id: str, claim_id: str,
        corpus_version: str, assessor_rubric_version: str,
        method_versions: dict[str, tuple[str, str]], started_at: datetime,
    ) -> ExperimentRun:
        if tuple(sorted(method_versions)) != REQUIRED_METHODS:
            raise ValueError("Experiment must freeze exactly B0-B4 before execution.")
        run = ExperimentRun(
            experiment_run_id, case_id, claim_id, corpus_version,
            assessor_rubric_version, ExperimentRunStatus.ACTIVE, started_at,
        )
        self.runs.create(run)
        for method in REQUIRED_METHODS:
            method_version, configuration_version = method_versions[method]
            self.runs.freeze_method(FrozenMethodConfiguration(
                experiment_run_id, method, method_version, configuration_version,
            ))
        return run

    def record_method(self, observation: PersistedMethodObservation) -> None:
        run = self.runs.get(observation.experiment_run_id)
        if run is None or run.status is not ExperimentRunStatus.ACTIVE:
            raise ValueError("Method observations require an ACTIVE experiment run.")
        self.observations.add_method_observation(observation)

    def record_reference(
        self, experiment_run_id: str, reference: IndependentReferenceJudgment,
        recorded_at: datetime,
    ) -> None:
        run = self.runs.get(experiment_run_id)
        if run is None or run.status is not ExperimentRunStatus.ACTIVE:
            raise ValueError("Reference judgments require an ACTIVE experiment run.")
        self.observations.add_reference(experiment_run_id, reference, recorded_at)

    def completion_readiness(self, experiment_run_id: str) -> tuple[bool, tuple[str, ...]]:
        run = self.runs.get(experiment_run_id)
        if run is None:
            raise ValueError("Unknown experiment run.")
        observed = {o.method for o in self.observations.observations(experiment_run_id)}
        missing = [f"method:{m}" for m in REQUIRED_METHODS if m not in observed]
        with self.observations.database.connect() as connection:
            reference = connection.execute(
                "SELECT 1 FROM experiment_reference_judgments WHERE experiment_run_id = ?",
                (experiment_run_id,),
            ).fetchone()
        if reference is None:
            missing.append("independent_reference")
        return (not missing, tuple(missing))

    def complete(self, experiment_run_id: str, ended_at: datetime) -> None:
        ready, missing = self.completion_readiness(experiment_run_id)
        if not ready:
            raise ValueError("Experiment incomplete: " + ", ".join(missing))
        self.runs.finish(experiment_run_id, ended_at)
