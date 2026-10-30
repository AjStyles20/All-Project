"""Persistent B4 verification-run model for P001 EGPCV."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class VerificationRunStatus(str, Enum):
    ACTIVE = "ACTIVE"
    VERIFICATION_COMPLETE = "VERIFICATION_COMPLETE"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"


@dataclass(frozen=True)
class VerificationRun:
    run_id: str
    case_id: str
    method_version: str
    configuration_version: str
    status: VerificationRunStatus
    started_at: datetime
    ended_at: datetime | None = None
    final_decision: str | None = None
    final_rationale: str | None = None


@dataclass(frozen=True)
class UsedProbe:
    run_id: str
    probe_id: str
    claim_id: str
    gap_type: str
    used_at: datetime
