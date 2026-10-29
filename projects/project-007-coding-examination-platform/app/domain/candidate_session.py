"""Candidate assignment, examination session and response model for P001 FD-03."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# Upper bound on one saved response. Keeps a single request from storing
# arbitrarily large payloads (resource limit, PROJECT_RULES section 22).
MAX_RESPONSE_CHARS = 100_000


class SessionStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    SUBMITTED = "SUBMITTED"


class SubmissionMode(str, Enum):
    CANDIDATE = "CANDIDATE"
    # Finalised because the examiner closed the examination (DR-011 (6)).
    AUTO_ON_CLOSE = "AUTO_ON_CLOSE"


@dataclass(frozen=True)
class CandidateAssignment:
    assignment_id: str
    examination_id: str
    candidate_user_id: str
    assigned_by_user_id: str


@dataclass(frozen=True)
class ExaminationSession:
    session_id: str
    assignment_id: str
    status: SessionStatus
    started_at: datetime
    submitted_at: datetime | None = None
    submission_mode: SubmissionMode | None = None


@dataclass(frozen=True)
class SavedResponse:
    session_id: str
    question_id: str
    content: str
    revision: int
    saved_at: datetime

    def validate(self) -> None:
        if len(self.content) > MAX_RESPONSE_CHARS:
            raise ValueError(f"Response exceeds {MAX_RESPONSE_CHARS} characters.")
        if self.revision <= 0:
            raise ValueError("Response revision must be positive.")


class SessionConflictError(ValueError):
    """The request conflicts with the session's current state or a newer save."""
