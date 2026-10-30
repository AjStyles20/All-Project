"""Structured ingestion for independent M8 assessor dry-run judgments.

This module records human judgments supplied after blinded administration. It
does not generate, infer, reconcile, or overwrite assessor judgments.
"""
from dataclasses import dataclass
from enum import Enum

from app.domain.enums import EvidenceState


class DimensionJudgment(str, Enum):
    YES = "YES"
    NO = "NO"
    CANNOT_DETERMINE = "CANNOT_DETERMINE"


@dataclass(frozen=True)
class AssessorJudgment:
    assessor_code: str
    case_id: str
    state: EvidenceState
    relevant_input: DimensionJudgment
    correct_expected_outcome: DimensionJudgment
    defensible_reason: DimensionJudgment
    rationale: str
    boundary_confident: bool
    ambiguous_boundary: str | None
    additional_evidence_needed: bool
    additional_evidence_description: str | None
    human_review_concern: bool
    human_review_reason: str | None
    independence_confirmed: bool

    def validate(self) -> None:
        if not self.assessor_code.strip():
            raise ValueError("assessor_code is required")
        if not self.case_id.strip():
            raise ValueError("case_id is required")
        if not self.rationale.strip():
            raise ValueError("rationale is required")
        if not self.independence_confirmed:
            raise ValueError("independence declaration must be confirmed")
        if not self.boundary_confident and not (self.ambiguous_boundary or "").strip():
            raise ValueError("ambiguous boundary is required when confidence is false")
        if self.additional_evidence_needed and not (self.additional_evidence_description or "").strip():
            raise ValueError("additional evidence description is required")
        if self.human_review_concern and not (self.human_review_reason or "").strip():
            raise ValueError("human review reason is required")


@dataclass(frozen=True)
class AssessorComparison:
    case_id: str
    assessor_a: str
    assessor_b: str
    state_agreement: bool
    dimension_agreement_count: int
    dimension_count: int = 3


def compare_independent_judgments(a: AssessorJudgment, b: AssessorJudgment) -> AssessorComparison:
    a.validate()
    b.validate()
    if a.case_id != b.case_id:
        raise ValueError("judgments must refer to the same case")
    if a.assessor_code == b.assessor_code:
        raise ValueError("comparison requires distinct assessor codes")
    dimensions = (
        a.relevant_input == b.relevant_input,
        a.correct_expected_outcome == b.correct_expected_outcome,
        a.defensible_reason == b.defensible_reason,
    )
    return AssessorComparison(
        case_id=a.case_id,
        assessor_a=a.assessor_code,
        assessor_b=b.assessor_code,
        state_agreement=a.state == b.state,
        dimension_agreement_count=sum(dimensions),
    )
