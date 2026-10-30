"""Minimal researcher-facing service layer for P001 M7.

This is deliberately not a student portal or production examination UI.
It exposes only the bounded experiment information needed to inspect a run.
"""
from dataclasses import dataclass

from app.domain.enums import EvidenceState


@dataclass(frozen=True)
class MethodView:
    method: str
    state: EvidenceState
    evidence_ids: tuple[str, ...]
    question_count: int
    verification_seconds: float
    complexity: tuple[str, ...]


@dataclass(frozen=True)
class ExperimentView:
    experiment_run_id: str
    case_id: str
    claim_id: str
    corpus_version: str
    assessor_rubric_version: str
    status: str
    methods: tuple[MethodView, ...]
    reference_state: EvidenceState | None
    reference_assessor_id: str | None
    complete: bool
    missing: tuple[str, ...]


class ResearchInterface:
    """Read model for assessor/research inspection of a comparative run."""

    def __init__(self, runs, observations):
        self.runs = runs
        self.observations = observations

    def inspect_experiment(self, experiment_run_id: str) -> ExperimentView:
        run = self.runs.get(experiment_run_id)
        if run is None:
            raise ValueError("Unknown experiment run.")

        rows = self.observations.observations(experiment_run_id)
        methods = tuple(
            MethodView(
                method=row.method,
                state=row.system_state,
                evidence_ids=row.evidence_ids,
                question_count=row.burden.question_count,
                verification_seconds=row.burden.verification_seconds,
                complexity=row.burden.complexity,
            )
            for row in rows
        )
        reference = self.observations.reference(experiment_run_id)
        present = {row.method for row in rows}
        missing = [m for m in ("B0", "B1", "B2", "B3", "B4") if m not in present]
        if reference is None:
            missing.append("INDEPENDENT_REFERENCE")

        return ExperimentView(
            experiment_run_id=run.experiment_run_id,
            case_id=run.case_id,
            claim_id=run.claim_id,
            corpus_version=run.corpus_version,
            assessor_rubric_version=run.assessor_rubric_version,
            status=run.status.value,
            methods=methods,
            reference_state=reference.state if reference else None,
            reference_assessor_id=reference.assessor_id if reference else None,
            complete=not missing,
            missing=tuple(missing),
        )
