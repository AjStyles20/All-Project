"""M8 pilot measurement records.

Raw timing and deviations remain separate from method outcomes. Missing timing
is represented as None, never silently converted to zero.
"""
from dataclasses import dataclass
from enum import Enum


class DeviationType(str, Enum):
    MISSING_TIMING = "MISSING_TIMING"
    MISSING_EVIDENCE = "MISSING_EVIDENCE"
    EVALUATOR_UNAVAILABLE = "EVALUATOR_UNAVAILABLE"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
    ASSESSOR_DISAGREEMENT = "ASSESSOR_DISAGREEMENT"
    PROTOCOL_DEVIATION = "PROTOCOL_DEVIATION"


@dataclass(frozen=True)
class PilotTimingRecord:
    experiment_run_id: str
    method: str
    question_count: int
    verification_seconds: float | None
    complexity: tuple[str, ...]

    def __post_init__(self):
        if self.question_count < 0:
            raise ValueError("question_count cannot be negative.")
        if self.verification_seconds is not None and self.verification_seconds < 0:
            raise ValueError("verification_seconds cannot be negative.")
        if len(self.complexity) != self.question_count:
            raise ValueError("complexity must contain one entry per administered question.")
        allowed = {"LOW", "MEDIUM", "HIGH"}
        if any(value not in allowed for value in self.complexity):
            raise ValueError("complexity values must be LOW, MEDIUM or HIGH.")
        if self.question_count > 0 and self.verification_seconds == 0:
            raise ValueError("Administered verification cannot use zero seconds as missing timing.")


@dataclass(frozen=True)
class PilotDeviation:
    deviation_id: str
    experiment_run_id: str
    deviation_type: DeviationType
    description: str
    invalidates_analysis: tuple[str, ...] = ()
