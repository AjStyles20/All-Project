"""Examiner marking model for P001 FD-04.

Marks are human examiner judgments on operational submissions. They are not
EGPCV evidence states, competence verdicts or misconduct findings.
"""
from dataclasses import dataclass
from datetime import datetime
from fractions import Fraction

from app.domain.examination import ExaminationQuestionEntry

MAX_COMMENT_CHARS = 5_000


@dataclass(frozen=True)
class ResponseMark:
    session_id: str
    question_id: str
    score: int
    comment: str
    response_revision: int | None
    marked_by_user_id: str
    marked_at: datetime

    def validate(self, max_score: int) -> None:
        if not 0 <= self.score <= max_score:
            raise ValueError(f"Score must be between 0 and {max_score}.")
        if len(self.comment) > MAX_COMMENT_CHARS:
            raise ValueError(f"Comment exceeds {MAX_COMMENT_CHARS} characters.")


@dataclass(frozen=True)
class ResultRelease:
    examination_id: str
    released_by_user_id: str
    released_at: datetime


def weighted_percent(entries: list[ExaminationQuestionEntry],
                     marks: dict[str, ResponseMark]) -> float | None:
    """DR-012 (1): sum(score / max_score * weight) / sum(weight) * 100, to 2 decimals.

    Returns None until every question is marked, so a partly marked session is
    never reported as a low percentage. Fractions keep the arithmetic exact
    before the single final rounding.
    """
    if not entries or any(e.question.question_id not in marks for e in entries):
        return None
    total_weight = sum(e.score_weight for e in entries)
    earned = sum(Fraction(marks[e.question.question_id].score, e.question.max_score) * e.score_weight
                 for e in entries)
    return round(float(earned / total_weight * 100), 2)


class MarkingConflictError(ValueError):
    """The session or examination is not in a state that allows marking."""
