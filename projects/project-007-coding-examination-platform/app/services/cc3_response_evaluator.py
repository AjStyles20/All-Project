"""Structured development rubric for CC3 Test Design verification.

This is a frozen development rule for CASE-DEV-003, not a validated final
scientific rubric. It evaluates explicit structured fields rather than trying
to infer competence from arbitrary free text.
"""
from dataclasses import dataclass

from app.domain.enums import EvidenceState


@dataclass(frozen=True)
class CC3ProbeResponse:
    test_input: str
    expected_result: str
    usefulness_reason: str
    input_relevant: bool
    expected_result_correct: bool
    reason_defensible: bool


@dataclass(frozen=True)
class CC3ResponseEvaluation:
    state: EvidenceState
    rationale: str


class CC3ResponseEvaluator:
    def evaluate(self, response: CC3ProbeResponse) -> CC3ResponseEvaluation:
        components = (
            response.input_relevant,
            response.expected_result_correct,
            response.reason_defensible,
        )
        satisfied = sum(components)

        if satisfied == 3:
            return CC3ResponseEvaluation(
                state=EvidenceState.SUPPORTED,
                rationale=(
                    "The structured verification response contains a relevant "
                    "independent test, the correct expected result, and a "
                    "defensible explanation of why the test is useful."
                ),
            )

        if satisfied > 0:
            return CC3ResponseEvaluation(
                state=EvidenceState.PARTIAL,
                rationale=(
                    "The response supplies some relevant test-design evidence "
                    "but does not satisfy every frozen CC3 development component."
                ),
            )

        return CC3ResponseEvaluation(
            state=EvidenceState.UNRESOLVED,
            rationale=(
                "The response does not yet supply sufficient relevant evidence "
                "for any frozen CC3 development component."
            ),
        )
