"""Machine-readable audit records for P001 research-critical decisions."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class AuditEventType(str, Enum):
    EVIDENCE_STATE_RECORDED = "EVIDENCE_STATE_RECORDED"
    GAP_DETECTED = "GAP_DETECTED"
    PROBE_SELECTION = "PROBE_SELECTION"
    PROBE_RESULT_RECORDED = "PROBE_RESULT_RECORDED"
    CONTROL_DECISION = "CONTROL_DECISION"


@dataclass(frozen=True)
class AuditEvent:
    event_id: str
    case_id: str
    event_type: AuditEventType
    recorded_at: datetime
    actor_type: str
    rationale: str
    claim_id: str | None = None
    gap_type: str | None = None
    probe_id: str | None = None
    evidence_id: str | None = None
    from_state: str | None = None
    to_state: str | None = None
    decision: str | None = None
    method_version: str | None = None
