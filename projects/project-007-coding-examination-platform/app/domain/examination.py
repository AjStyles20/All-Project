"""Operational examination/question domain model for P001 FD-02."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ExaminationStatus(str, Enum):
    DRAFT = "DRAFT"
    SCHEDULED = "SCHEDULED"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    ARCHIVED = "ARCHIVED"


@dataclass(frozen=True)
class Examination:
    examination_id: str
    title: str
    description: str
    owner_user_id: str
    status: ExaminationStatus
    starts_at: datetime | None = None
    ends_at: datetime | None = None

    def validate(self) -> None:
        if not self.title.strip():
            raise ValueError("Examination title is required.")
        if self.starts_at and self.ends_at and self.ends_at <= self.starts_at:
            raise ValueError("Examination end time must be after start time.")


@dataclass(frozen=True)
class ProgrammingQuestion:
    question_id: str
    title: str
    prompt: str
    language: str
    max_score: int
    version: int = 1

    def validate(self) -> None:
        if not self.title.strip() or not self.prompt.strip():
            raise ValueError("Question title and prompt are required.")
        if self.max_score <= 0:
            raise ValueError("Question max_score must be positive.")
        if self.version <= 0:
            raise ValueError("Question version must be positive.")
