"""Examiner marking model for P001 FD-04.

Marks are human examiner judgments on operational submissions. They are not
EGPCV evidence states, competence verdicts or misconduct findings.
"""
from dataclasses import dataclass
from datetime import datetime

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


class MarkingConflictError(ValueError):
    """The session or examination is not in a state that allows marking."""
