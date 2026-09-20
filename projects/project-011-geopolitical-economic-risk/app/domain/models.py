"""Immutable domain records for Economic Transmission Evidence Contract (ETEC)."""
from dataclasses import dataclass
from datetime import datetime

from .enums import EdgeState, SourceAuthorityTier, TransitionClass


@dataclass(frozen=True)
class EconomicCase:
    case_id: str
    target_country: str
    event_type: str
    information_cutoff: datetime
    version: str


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    case_id: str
    transition: TransitionClass
    authority_tier: SourceAuthorityTier
    source_reference: str
    observed_at: datetime
    data_vintage: str
    geography: str
    economic_identifier: str | None = None
    classification_version: str | None = None
    valid_until: datetime | None = None
    content_hash: str | None = None


@dataclass(frozen=True)
class TransitionAssessment:
    case_id: str
    transition: TransitionClass
    state: EdgeState
    evidence_ids: tuple[str, ...]
    rationale: str
