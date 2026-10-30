"""Operational -> EGPCV evidence bridge model for P001 FD-06.

Governed by ECC v1.0 §6 (evidence labelling), DR-013 (Q3 ARTIFACT/POLICY_CONTEXT
only; Q4 explicit question -> case link) and DR-015 (ethics reference + opt-in,
random research codes, administrator-only links, one case per candidate per question).
"""
import json
import secrets
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from app.domain.capability_contract import CapabilityContract, ContractException

# Capabilities that bear on how much assistance an answer may reflect (spec §6).
ASSISTANCE_KEYS = ("ai_assistance", "documentation", "internet", "clipboard")
SOURCE_TYPE = "OPERATIONAL_SUBMISSION:FD-06"


class ConsentStatus(str, Enum):
    OPTED_IN = "OPTED_IN"
    WITHDRAWN = "WITHDRAWN"


class BridgeOutcome(str, Enum):
    BRIDGED = "BRIDGED"
    NO_RESPONSE = "NO_RESPONSE"   # nothing saved: missing evidence is not invented
    NO_CONTRACT = "NO_CONTRACT"   # no contract in force when saved: spec R5, not assumed


class ResearchBridgeError(ValueError):
    """The bridge cannot run in the current state (wrong exam state, invalid link)."""


class ResearchStoreNotConfigured(ResearchBridgeError):
    """No research store path is configured; nothing is copied (reported as 503)."""


@dataclass(frozen=True)
class ResearchLink:
    link_id: str
    examination_id: str
    question_id: str
    template_case_id: str
    claim_ids: tuple[str, ...]
    ethics_reference: str
    created_by_user_id: str
    created_at: datetime

    def validate(self) -> None:
        if not self.ethics_reference.strip():
            raise ValueError("A research link requires an institutional ethics approval reference.")
        if not self.claim_ids or any(not c.strip() for c in self.claim_ids):
            raise ValueError("A research link must name at least one claim.")
        if len(set(self.claim_ids)) != len(self.claim_ids):
            raise ValueError("Claim ids must be unique.")


@dataclass(frozen=True)
class BridgeRecord:
    session_id: str
    question_id: str
    link_id: str
    outcome: BridgeOutcome
    research_case_id: str | None
    response_revision: int | None
    policy_version: str | None
    bridged_at: datetime


def new_research_code() -> str:
    # Random, so the code reveals nothing about the student (DR-015 (2)).
    return "R-" + secrets.token_hex(6).upper()


def research_case_id(research_code: str, question_id: str) -> str:
    return f"op-{research_code}-{question_id}"


# Contract fields that identify a person; removed before the contract enters the research store.
REDACTED_CONTRACT_FIELDS = ("bound_by_user_id",)


def research_policy_document(contract: CapabilityContract) -> str:
    """POLICY_CONTEXT evidence content (DR-013 Q3) without personal identifiers (DR-015 (2)).

    The full content hash is kept, so the exact bound contract can still be verified
    against the operational database by someone authorised to read it.
    """
    document = {k: v for k, v in contract.hashed_document().items() if k not in REDACTED_CONTRACT_FIELDS}
    return json.dumps({"contract": document, "content_hash": contract.content_hash or contract.compute_hash(),
                       "redacted_fields": list(REDACTED_CONTRACT_FIELDS)},
                      sort_keys=True, separators=(",", ":"))


def assistance_context(contract: CapabilityContract, exceptions: list[ContractException],
                       claim_ids: tuple[str, ...], at: datetime) -> str:
    """Canonical JSON for EvidenceItem.assistance_context (ECC v1.0 §6).

    Only exceptions approved at or before the event apply (spec §5.4). Reason
    categories are omitted: the research store needs what was permitted, not why.
    """
    contract_doc = contract.hashed_document()
    construct = contract_doc["assistance_construct"]
    active = [e for e in exceptions if e.approved_at <= at]
    document = {
        "capabilities": {key: contract_doc["capabilities"][key] for key in ASSISTANCE_KEYS},
        "assistance_construct": {claim: construct["per_claim"].get(claim, construct["default"])
                                 for claim in claim_ids},
        "exceptions": [{"capability_overrides": e.capability_overrides,
                        "extra_time_minutes": e.extra_time_minutes} for e in active],
        "enforcement": contract_doc["enforcement"],
    }
    return json.dumps(document, sort_keys=True, separators=(",", ":"))
