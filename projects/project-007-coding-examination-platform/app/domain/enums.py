"""Core P001 domain enumerations.

These values implement the pre-implementation research specification.
They do not represent experimental findings.
"""
from enum import Enum


class ClaimApplicability(str, Enum):
    REQUIRED = "REQUIRED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class EvidenceState(str, Enum):
    SUPPORTED = "SUPPORTED"
    PARTIAL = "PARTIAL"
    UNRESOLVED = "UNRESOLVED"
    CONTRADICTED = "CONTRADICTED"


class EvidenceType(str, Enum):
    ARTIFACT = "ARTIFACT"
    PROCESS = "PROCESS"
    EXECUTION = "EXECUTION"
    RUBRIC = "RUBRIC"
    VERIFICATION = "VERIFICATION"
    POLICY_CONTEXT = "POLICY_CONTEXT"
