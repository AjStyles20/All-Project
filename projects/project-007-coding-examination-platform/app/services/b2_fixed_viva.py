"""Non-adaptive B2 fixed-viva procedure for P001 development experiments."""
from dataclasses import dataclass
from datetime import datetime

from app.domain.enums import EvidenceState
from app.services.cc3_response_evaluator import CC3ProbeResponse, CC3ResponseEvaluator


@dataclass(frozen=True)
class FixedVivaQuestion:
    family: str
    prompt: str
    version: str = "B2-FIXED-VIVA-v1.0-development"


@dataclass(frozen=True)
class FixedVivaAdministration:
    case_id: str
    questions: tuple[FixedVivaQuestion, ...]


@dataclass(frozen=True)
class FixedVivaCC3Result:
    state: EvidenceState
    rationale: str


class B2FixedViva:
    """Returns the same question-family battery for every eligible case."""

    def administer(self, case_id: str) -> FixedVivaAdministration:
        return FixedVivaAdministration(case_id=case_id, questions=(
            FixedVivaQuestion(
                "EXPLAIN",
                "Explain the purpose of the frozen important code region and how it contributes to the result.",
            ),
            FixedVivaQuestion(
                "PREDICT_TRACE",
                "For the frozen bounded input, predict or trace the relevant execution and expected result.",
            ),
            FixedVivaQuestion(
                "TEST_DESIGN",
                "Give one additional useful test, its expected result, and why the test is useful.",
            ),
            FixedVivaQuestion(
                "MODIFY",
                "Make or describe the frozen bounded change and explain its consequence.",
            ),
        ))

    def evaluate_cc3(self, response: CC3ProbeResponse) -> FixedVivaCC3Result:
        result = CC3ResponseEvaluator().evaluate(response)
        return FixedVivaCC3Result(
            state=result.state,
            rationale=(
                "B2 fixed Test Design response evaluated with the shared CC3 "
                "development dimensions; question allocation remains non-adaptive. "
                + result.rationale
            ),
        )
