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
from app.services.baseline_experiment_runner import BaselineExperimentRunner
from app.services.verification_burden import VerificationBurden
from app.domain.models import EvidenceItem


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

    def execute_b0_b3(
        self, *, experiment_run_id: str, case_id: str, claim_id: str,
        evidence: list[EvidenceItem], recorded_at: datetime,
        b2_burden: VerificationBurden | None = None,
    ) -> tuple[PersistedMethodObservation, ...]:
        """Execute B0-B3 from one evidence collection under frozen boundaries.

        B0, B1 and B3 have zero verification burden here. B2 burden must be
        supplied from the actual fixed-viva administration when B2 verification
        evidence is present; it is never guessed.
        """
        run = self.runs.get(experiment_run_id)
        if run is None or run.status is not ExperimentRunStatus.ACTIVE:
            raise ValueError("Baseline execution requires an ACTIVE experiment run.")
        if run.case_id != case_id or run.claim_id != claim_id:
            raise ValueError("Execution case/claim must match the frozen experiment.")

        result = BaselineExperimentRunner().run(
            case_id=case_id, claim_id=claim_id, evidence=evidence,
        )
        observations = []
        for baseline in result.results:
            if baseline.method == "B2":
                has_fixed_viva = any(
                    item.evidence_id in baseline.evidence_ids
                    and item.evidence_type.value == "VERIFICATION"
                    and item.source_type == "fixed_viva"
                    for item in evidence
                )
                if has_fixed_viva and b2_burden is None:
                    raise ValueError(
                        "B2 fixed-viva evidence requires measured burden; it cannot be guessed."
                    )
                burden = b2_burden or VerificationBurden(0, 0.0, ())
            else:
                burden = VerificationBurden(0, 0.0, ())

            observation = PersistedMethodObservation(
                experiment_run_id=experiment_run_id,
                method=baseline.method,
                system_state=baseline.state,
                evidence_ids=baseline.evidence_ids,
                burden=burden,
                recorded_at=recorded_at,
            )
            self.record_method(observation)
            observations.append(observation)
        return tuple(observations)

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
