"""Research-critical domain models for P001.

M1 intentionally contains no UI, authentication, proctoring, or automatic
misconduct logic. It models cases, bounded competence claims, evidence,
claim-evidence links, and append-only evidence-state history.
"""
from dataclasses import dataclass
from datetime import datetime, timezone

from .enums import ClaimApplicability, EvidenceState, EvidenceType


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class ProgrammingCase:
    case_id: str
    title: str
    task_description: str
    language: str
    version: str = "1.0"


@dataclass(frozen=True)
class CompetenceClaim:
    claim_id: str
    name: str
    definition: str
    version: str = "1.0"


@dataclass(frozen=True)
class CaseClaim:
    case_id: str
    claim_id: str
    applicability: ClaimApplicability


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    case_id: str
    evidence_type: EvidenceType
    content: str
    source_type: str
    created_at: datetime
    policy_version: str | None = None
    assistance_context: str | None = None


@dataclass(frozen=True)
class ClaimEvidenceLink:
    case_id: str
    claim_id: str
    evidence_id: str
    rationale: str


@dataclass(frozen=True)
class EvidenceStateRecord:
    case_id: str
    claim_id: str
    state: EvidenceState
    rationale: str
    recorded_at: datetime
    source: str
