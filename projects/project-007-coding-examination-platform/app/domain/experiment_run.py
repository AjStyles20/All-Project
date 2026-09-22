"""Persistent experiment-run identity for B0-B4 comparative evaluation."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ExperimentRunStatus(str, Enum):
    ACTIVE = "ACTIVE"
    COMPLETE = "COMPLETE"
    INVALID = "INVALID"


@dataclass(frozen=True)
class ExperimentRun:
    experiment_run_id: str
    case_id: str
    claim_id: str
    corpus_version: str
    assessor_rubric_version: str
    status: ExperimentRunStatus
    started_at: datetime
    ended_at: datetime | None = None


@dataclass(frozen=True)
class FrozenMethodConfiguration:
    experiment_run_id: str
    method: str
    method_version: str
    configuration_version: str
