"""B0-B3 comparison engines for the P001 research experiment.

These engines enforce information boundaries. They are comparison methods,
not final grading systems and not scientific validation of EGPCV.
"""
from dataclasses import dataclass
from typing import Iterable

from app.domain.enums import EvidenceState, EvidenceType
from app.domain.models import EvidenceItem
from app.services.evidence_evaluator import EvidenceEvaluator


@dataclass(frozen=True)
class BaselineResult:
    method: str
    claim_id: str
    state: EvidenceState
    rationale: str
    evidence_ids: tuple[str, ...]


class _EvidenceBoundary:
    @staticmethod
    def include(evidence: Iterable[EvidenceItem], allowed: frozenset[EvidenceType]):
        return [item for item in evidence if item.evidence_type in allowed]

    @staticmethod
    def include_b2(evidence: Iterable[EvidenceItem], allowed: frozenset[EvidenceType]):
        """B2 may consume only explicitly provenance-marked fixed-viva verification."""
        return [
            item for item in evidence
            if item.evidence_type in allowed
            and (
                item.evidence_type is not EvidenceType.VERIFICATION
                or item.source_type == "fixed_viva"
            )
        ]


class B0Engine:
    """Final submission + ordinary tests/rubric only."""
    method = "B0"
    allowed = frozenset({
        EvidenceType.ARTIFACT, EvidenceType.EXECUTION, EvidenceType.RUBRIC,
    })

    def evaluate(self, claim_id: str, evidence: list[EvidenceItem]) -> BaselineResult:
        bounded = _EvidenceBoundary.include(evidence, self.allowed)
        result = EvidenceEvaluator().evaluate(claim_id, bounded)
        return BaselineResult(
            self.method, claim_id, result.state,
            f"B0 information boundary: {result.rationale}",
            tuple(item.evidence_id for item in bounded),
        )


class B1Engine(B0Engine):
    """B0 + controlled programming-process/event evidence."""
    method = "B1"
    allowed = B0Engine.allowed | frozenset({EvidenceType.PROCESS})


class B2Engine(B1Engine):
    """B1 + generic fixed viva evidence; no gap-driven selection."""
    method = "B2"
    allowed = B1Engine.allowed | frozenset({EvidenceType.VERIFICATION})

    def evaluate(self, claim_id: str, evidence: list[EvidenceItem]) -> BaselineResult:
        # The evidence boundary is implemented now; the fixed-viva response
        # rubric remains a separate method-freeze item. No targeted probe
        # selection is permitted here.
        bounded = _EvidenceBoundary.include_b2(evidence, self.allowed)
        result = EvidenceEvaluator().evaluate(claim_id, bounded)
        return BaselineResult(
            self.method, claim_id, result.state,
            f"B2 fixed-viva boundary (no targeted selection; targeted-verification evidence excluded): {result.rationale}",
            tuple(item.evidence_id for item in bounded),
        )


class B3Engine(B1Engine):
    """Evidence-centered competence model without targeted verification."""
    method = "B3"

    def evaluate(self, claim_id: str, evidence: list[EvidenceItem]) -> BaselineResult:
        # B3 deliberately excludes VERIFICATION evidence. It structures the
        # available evidence around competence claims but asks no follow-up.
        bounded = _EvidenceBoundary.include(evidence, self.allowed)
        result = EvidenceEvaluator().evaluate(claim_id, bounded)
        return BaselineResult(
            self.method, claim_id, result.state,
            f"B3 evidence-centered model; targeted verification prohibited: {result.rationale}",
            tuple(item.evidence_id for item in bounded),
        )
