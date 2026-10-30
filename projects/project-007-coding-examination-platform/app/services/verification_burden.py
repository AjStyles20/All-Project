"""Transparent verification-burden measurements for P001 experiments.

Burden dimensions remain separate; no arbitrary weighted composite score is used.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class VerificationBurden:
    question_count: int
    verification_seconds: float
    complexity: tuple[str, ...]

    def __post_init__(self):
        if self.question_count < 0:
            raise ValueError("question_count cannot be negative")
        if self.verification_seconds < 0:
            raise ValueError("verification_seconds cannot be negative")
        if len(self.complexity) != self.question_count:
            raise ValueError("complexity must contain one entry per administered question")
        allowed = {"LOW", "MEDIUM", "HIGH"}
        if any(level not in allowed for level in self.complexity):
            raise ValueError("complexity entries must be LOW, MEDIUM, or HIGH")


@dataclass(frozen=True)
class BurdenComparison:
    b2: VerificationBurden
    b4: VerificationBurden

    @property
    def question_difference(self) -> int:
        return self.b2.question_count - self.b4.question_count

    @property
    def time_difference_seconds(self) -> float:
        return self.b2.verification_seconds - self.b4.verification_seconds
