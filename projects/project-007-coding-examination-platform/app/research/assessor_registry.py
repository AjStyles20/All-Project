"""In-memory dry-run registry for preserving independent assessor responses.

Persistence is deliberately separate from experiment reference judgment:
multiple assessor responses must survive until the research protocol decides
how, if at all, a reference judgment is derived.
"""
from dataclasses import dataclass

from app.research.assessor_judgment import (
    AssessorComparison, AssessorJudgment, compare_independent_judgments,
)


@dataclass(frozen=True)
class CaseAssessmentSummary:
    case_id: str
    judgments: tuple[AssessorJudgment, ...]
    comparison: AssessorComparison | None


class AssessorJudgmentRegistry:
    def __init__(self) -> None:
        self._records: dict[tuple[str, str], AssessorJudgment] = {}

    def add(self, judgment: AssessorJudgment) -> None:
        judgment.validate()
        key = (judgment.case_id, judgment.assessor_code)
        if key in self._records:
            raise ValueError("assessor judgment already exists; preserve original record")
        self._records[key] = judgment

    def for_case(self, case_id: str) -> tuple[AssessorJudgment, ...]:
        return tuple(
            record for (record_case, _), record in sorted(self._records.items())
            if record_case == case_id
        )

    def summarize_two_assessor_case(self, case_id: str) -> CaseAssessmentSummary:
        records = self.for_case(case_id)
        if len(records) > 2:
            raise ValueError("two-assessor dry-run summary received more than two judgments")
        comparison = None
        if len(records) == 2:
            comparison = compare_independent_judgments(records[0], records[1])
        return CaseAssessmentSummary(case_id, records, comparison)
