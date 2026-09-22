"""Enforceable M8 constructed dry-run readiness gate."""
from dataclasses import dataclass

from app.persistence.experiment_run_repository import ExperimentRunRepository
from app.research.pilot_cases import PilotCaseBundle
from app.research.pilot_experiment import (
    PILOT_ASSESSOR_RUBRIC_VERSION, PILOT_METHOD_VERSIONS,
)


@dataclass(frozen=True)
class DryRunReadiness:
    ready: bool
    missing_or_invalid: tuple[str, ...]


class DryRunReadinessValidator:
    def __init__(self, runs: ExperimentRunRepository):
        self.runs = runs

    def validate(
        self, *, experiment_run_id: str, bundle: PilotCaseBundle,
        timing_procedure_version: str | None,
    ) -> DryRunReadiness:
        issues: list[str] = []
        run = self.runs.get(experiment_run_id)
        if run is None:
            return DryRunReadiness(False, ("experiment_run",))

        if run.case_id != bundle.case.case_id:
            issues.append("case_identity")
        if run.claim_id != bundle.claim.claim_id:
            issues.append("claim_identity")
        if run.corpus_version != bundle.corpus_version:
            issues.append("corpus_version")
        if run.assessor_rubric_version != PILOT_ASSESSOR_RUBRIC_VERSION:
            issues.append("assessor_rubric_version")
        if not bundle.case.version:
            issues.append("case_version")
            issues.append("task_version")
        # Bounded M8 rule: task_version is explicitly aliased to case.version.
        task_version = bundle.case.version
        if task_version != bundle.case.version:
            issues.append("task_version")
        if not bundle.evidence:
            issues.append("evidence_bundle")
        if any(not item.source_type for item in bundle.evidence):
            issues.append("evidence_provenance")
        if not timing_procedure_version:
            issues.append("timing_procedure_version")

        frozen = {c.method: c for c in self.runs.method_configurations(experiment_run_id)}
        if set(frozen) != set(PILOT_METHOD_VERSIONS):
            issues.append("b0_b4_method_set")
        else:
            for method, (method_version, configuration_version) in PILOT_METHOD_VERSIONS.items():
                current = frozen[method]
                if (
                    current.method_version != method_version
                    or current.configuration_version != configuration_version
                ):
                    issues.append(f"{method.lower()}_configuration")

        return DryRunReadiness(not issues, tuple(issues))
