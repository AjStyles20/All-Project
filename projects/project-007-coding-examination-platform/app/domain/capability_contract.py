"""Examination Capability Contract (ECC) domain model for P001 FD-05.

Implements the approved ECC v1.0 specification
(specification/EXAMINATION_CAPABILITY_CONTRACT_SPECIFICATION.md, DR-013).
The contract is declarative: it states what a candidate may use. It does not
enforce anything and never produces integrity verdicts.
"""
import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from app.domain.examination import ExaminationConflictError

SCHEMA_VERSION = "1.0"
# Spec §3: until runtime enforcement exists, every contract carries this label.
ENFORCEMENT = "DECLARED_NOT_ENFORCED"

# Spec §4.2: each key takes exactly one of these values.
CAPABILITY_VALUES: dict[str, frozenset[str]] = {
    "compiler": frozenset({"ALLOW", "DENY"}),
    "debugger": frozenset({"ALLOW", "DENY"}),
    "visible_tests": frozenset({"ALLOW", "DENY"}),
    "terminal": frozenset({"ALLOW", "LIMITED", "DENY"}),
    "documentation": frozenset({"ALLOW", "ALLOWLIST", "DENY"}),
    "internet": frozenset({"ALLOW", "ALLOWLIST", "DENY"}),
    "clipboard": frozenset({"ALLOW", "INTERNAL_ONLY", "DENY"}),
    "ai_assistance": frozenset({"DENY", "DECLARE", "ALLOW_BOUNDED", "ALLOW"}),
    "external_ide": frozenset({"ALLOW", "DENY"}),
}
# Values that need extra detail, and the field that carries it.
DETAIL_FIELDS = {"LIMITED": "allowlist", "ALLOWLIST": "sources", "ALLOW_BOUNDED": "limits"}


class ContractStatus(str, Enum):
    DRAFT = "DRAFT"
    BOUND = "BOUND"
    SUPERSEDED = "SUPERSEDED"


class IntegrityMode(str, Enum):
    LAB_CONTROLLED = "LAB_CONTROLLED"  # default (DR-013 Q5)
    RESTRICTED_BROWSER = "RESTRICTED_BROWSER"
    REMOTE_PROCTORED = "REMOTE_PROCTORED"
    OPEN_TOOL_DECLARED = "OPEN_TOOL_DECLARED"


class AssistanceConstruct(str, Enum):
    INDEPENDENT = "INDEPENDENT"
    ASSISTANCE_INCLUSIVE = "ASSISTANCE_INCLUSIVE"


class ExceptionReason(str, Enum):
    # Category only: detailed reasons are deliberately not stored (NFR-10).
    ACCESSIBILITY = "ACCESSIBILITY"
    TECHNICAL = "TECHNICAL"
    OTHER_APPROVED = "OTHER_APPROVED"


class ContractRequiredError(ExaminationConflictError):
    """Scheduling needs a capability contract (spec §5.2)."""


def contract_id_for(examination_id: str) -> str:
    return "ecc-" + examination_id


def normalise_capabilities(raw: dict) -> dict:
    """Validate capabilities and return them in canonical form.

    A plain value stays a string; a value needing detail becomes {"value": ..., <field>: ...}.
    """
    if set(raw) != set(CAPABILITY_VALUES):
        missing = sorted(set(CAPABILITY_VALUES) - set(raw))
        unknown = sorted(set(raw) - set(CAPABILITY_VALUES))
        raise ValueError(f"Capabilities must list every key exactly once (missing {missing}, unknown {unknown}).")
    return {key: normalise_capability(key, raw[key]) for key in sorted(raw)}


def normalise_capability(key: str, item):
    if key not in CAPABILITY_VALUES:
        raise ValueError(f"Unknown capability '{key}'.")
    value = item.get("value") if isinstance(item, dict) else item
    if value not in CAPABILITY_VALUES[key]:
        raise ValueError(f"{key} must be one of {sorted(CAPABILITY_VALUES[key])}.")
    detail_field = DETAIL_FIELDS.get(value)
    if detail_field is None:
        if isinstance(item, dict) and set(item) - {"value"}:
            raise ValueError(f"{key}={value} takes no extra detail.")
        return value
    detail = item.get(detail_field) if isinstance(item, dict) else None
    if detail_field == "limits":
        if not isinstance(detail, str) or not detail.strip():
            raise ValueError(f"{key}={value} requires a non-empty '{detail_field}' description.")
    elif not isinstance(detail, list) or not detail or not all(isinstance(d, str) and d.strip() for d in detail):
        raise ValueError(f"{key}={value} requires a non-empty '{detail_field}' list.")
    return {"value": value, detail_field: detail}


@dataclass(frozen=True)
class CapabilityContract:
    examination_id: str
    version: int
    status: ContractStatus
    integrity_mode: IntegrityMode
    capabilities: dict
    assistance_default: AssistanceConstruct = AssistanceConstruct.INDEPENDENT
    assistance_per_claim: dict = field(default_factory=dict)
    remote_proctoring_justification: str | None = None
    bound_by_user_id: str | None = None
    supersedes_version: int | None = None
    amendment_reason: str | None = None
    bound_at: datetime | None = None
    content_hash: str | None = None

    @property
    def contract_id(self) -> str:
        return contract_id_for(self.examination_id)

    def validate(self) -> None:
        if self.version <= 0:
            raise ValueError("Contract version must be positive.")
        normalise_capabilities(self.capabilities)
        if self.integrity_mode is IntegrityMode.REMOTE_PROCTORED and not (self.remote_proctoring_justification or "").strip():
            raise ValueError("REMOTE_PROCTORED requires a recorded justification (spec §4.3).")
        for claim_id, construct in self.assistance_per_claim.items():
            if not str(claim_id).strip():
                raise ValueError("Assistance construct claim ids must be non-empty.")
            AssistanceConstruct(construct)
        if self.supersedes_version is not None and not (self.amendment_reason or "").strip():
            raise ValueError("A new version of a bound contract requires an amendment reason (spec §5.3).")

    def hashed_document(self) -> dict:
        """Spec §8: everything except status, bound_at and content_hash, canonically ordered."""
        return {
            "schema_version": SCHEMA_VERSION,
            "contract_id": self.contract_id,
            "examination_id": self.examination_id,
            "version": self.version,
            "enforcement": ENFORCEMENT,
            "integrity_mode": self.integrity_mode.value,
            "capabilities": normalise_capabilities(self.capabilities),
            "assistance_construct": {"default": self.assistance_default.value,
                                     "per_claim": {k: AssistanceConstruct(v).value
                                                   for k, v in sorted(self.assistance_per_claim.items())}},
            "remote_proctoring_justification": self.remote_proctoring_justification,
            "bound_by_user_id": self.bound_by_user_id,
            "supersedes_version": self.supersedes_version,
            "amendment_reason": self.amendment_reason,
        }

    def compute_hash(self) -> str:
        canonical = json.dumps(self.hashed_document(), sort_keys=True, separators=(",", ":"))
        return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def policy_version_label(self) -> str:
        """Spec §6: the value later written to EvidenceItem.policy_version."""
        return f"ecc:{self.examination_id}@v{self.version}#{(self.content_hash or self.compute_hash())[7:19]}"


@dataclass(frozen=True)
class ContractException:
    exception_id: str
    examination_id: str
    contract_version: int
    candidate_user_id: str
    reason_category: ExceptionReason
    approved_by_user_id: str
    approved_at: datetime
    capability_overrides: dict = field(default_factory=dict)
    extra_time_minutes: int = 0

    def validate(self) -> None:
        if not self.capability_overrides and self.extra_time_minutes <= 0:
            raise ValueError("An exception must change at least one capability or add time.")
        if self.extra_time_minutes < 0 or self.extra_time_minutes > 24 * 60:
            raise ValueError("Extra time must be between 0 and 1440 minutes.")
        for key, item in self.capability_overrides.items():
            # Same rules as a full contract entry, including required detail.
            normalise_capability(key, item)
