"""Types for the two research kernels (Pass 017 §7).

Authority and status are separate: authority says how trustworthy a claim's origin is,
status says whether it is still usable now.
"""
from enum import Enum, IntEnum


class Authority(IntEnum):
    """Ordered: a derived claim may never rank above what it came from (APLDG-R02)."""
    UNVERIFIED = 0
    COMMUNITY_ASSERTION = 1
    AI_DERIVED = 2
    HUMAN_ASSERTION = 3
    TRUSTED_REFERENCE = 4
    CANONICAL_APPROVED = 5


TRUSTED = {Authority.TRUSTED_REFERENCE, Authority.CANONICAL_APPROVED}


class ClaimStatus(str, Enum):
    CURRENT = "CURRENT"
    UNVERIFIED = "UNVERIFIED"
    CONFLICTED = "CONFLICTED"
    STALE = "STALE"
    SUPERSEDED = "SUPERSEDED"
    REJECTED = "REJECTED"


class Relation(str, Enum):
    SUPPORTS = "SUPPORTS"
    CONTRADICTS = "CONTRADICTS"
    QUALIFIES = "QUALIFIES"


class EdgeType(str, Enum):
    PARAPHRASE = "PARAPHRASE"
    SUMMARY = "SUMMARY"
    INFERENCE = "INFERENCE"
    AGGREGATION = "AGGREGATION"
    CORRECTION = "CORRECTION"
    REUSE = "REUSE"


class ArtifactStatus(str, Enum):
    CURRENT = "CURRENT"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    STALE = "STALE"
    CONFLICTED = "CONFLICTED"
    INVALID = "INVALID"


class Assistance(IntEnum):
    """Cognitive assistance ladder (Pass 017 §7). Accessibility support is recorded separately."""
    L0_NONE = 0
    L1_METACOGNITIVE = 1
    L2_CONCEPTUAL_CUE = 2
    L3_TARGETED_HINT = 3
    L4_PARTIAL_PROCEDURE = 4
    L5_WORKED_SCAFFOLD = 5
    L6_DIRECT_ANSWER = 6


class Mastery(str, Enum):
    UNKNOWN = "UNKNOWN"
    ASSISTED_SUCCESS = "ASSISTED_SUCCESS"
    PROVISIONAL = "PROVISIONAL"
    VERIFYING = "VERIFYING"
    INDEPENDENT = "INDEPENDENT"
    REOPENED = "REOPENED"


class IssueState(str, Enum):
    OPEN = "OPEN"
    WORKING = "WORKING"
    VERIFYING = "VERIFYING"
    RESOLVED = "RESOLVED"
    REOPENED = "REOPENED"


class PolicyError(Exception):
    """A request the deterministic policy refuses. The message says why."""
