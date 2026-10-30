"""Audit helpers for recording the B4 decision path without hiding rationale."""
from datetime import datetime

from app.domain.audit import AuditEvent, AuditEventType
from app.domain.enums import EvidenceState
from app.services.gap_detector import EvidenceGapCandidate
from app.services.probe_selector import ProbeSelection
from app.services.verification_workflow import VerificationUpdate


class AuditTrailRecorder:
    def __init__(self, audit_repository, *, method_version: str = "B4-v1.0-development"):
        self.audit_repository = audit_repository
        self.method_version = method_version

    def record_initial_state(
        self, *, event_id: str, case_id: str, claim_id: str,
        state: EvidenceState, rationale: str, recorded_at: datetime
    ) -> None:
        self.audit_repository.append(AuditEvent(
            event_id=event_id, case_id=case_id,
            event_type=AuditEventType.EVIDENCE_STATE_RECORDED,
            recorded_at=recorded_at, actor_type="B4_ENGINE",
            rationale=rationale, claim_id=claim_id,
            to_state=state.value, method_version=self.method_version,
        ))

    def record_gap(
        self, *, event_id: str, case_id: str,
        gap: EvidenceGapCandidate, recorded_at: datetime
    ) -> None:
        self.audit_repository.append(AuditEvent(
            event_id=event_id, case_id=case_id,
            event_type=AuditEventType.GAP_DETECTED,
            recorded_at=recorded_at, actor_type="B4_ENGINE",
            rationale=gap.description, claim_id=gap.claim_id,
            gap_type=gap.gap_type, method_version=self.method_version,
        ))

    def record_selection(
        self, *, event_id: str, case_id: str,
        selection: ProbeSelection, recorded_at: datetime
    ) -> None:
        self.audit_repository.append(AuditEvent(
            event_id=event_id, case_id=case_id,
            event_type=AuditEventType.PROBE_SELECTION,
            recorded_at=recorded_at, actor_type="B4_ENGINE",
            rationale=selection.rationale, claim_id=selection.claim_id,
            gap_type=selection.gap_type,
            probe_id=(selection.selected_probe.probe_id if selection.selected_probe else None),
            decision=selection.decision, method_version=self.method_version,
        ))

    def record_verification_update(
        self, *, result_event_id: str, state_event_id: str,
        control_event_id: str, case_id: str, claim_id: str,
        gap_type: str, probe_id: str, from_state: EvidenceState,
        update: VerificationUpdate, recorded_at: datetime
    ) -> None:
        self.audit_repository.append(AuditEvent(
            event_id=result_event_id, case_id=case_id,
            event_type=AuditEventType.PROBE_RESULT_RECORDED,
            recorded_at=recorded_at, actor_type="B4_ENGINE",
            rationale="Targeted verification result recorded as new evidence.",
            claim_id=claim_id, gap_type=gap_type, probe_id=probe_id,
            evidence_id=update.evidence.evidence_id,
            method_version=self.method_version,
        ))
        self.audit_repository.append(AuditEvent(
            event_id=state_event_id, case_id=case_id,
            event_type=AuditEventType.EVIDENCE_STATE_RECORDED,
            recorded_at=recorded_at, actor_type="B4_ENGINE",
            rationale=update.state_record.rationale, claim_id=claim_id,
            gap_type=gap_type, probe_id=probe_id,
            evidence_id=update.evidence.evidence_id,
            from_state=from_state.value, to_state=update.state_record.state.value,
            method_version=self.method_version,
        ))
        self.audit_repository.append(AuditEvent(
            event_id=control_event_id, case_id=case_id,
            event_type=AuditEventType.CONTROL_DECISION,
            recorded_at=recorded_at, actor_type="B4_ENGINE",
            rationale=(
                "Target claim is supported under the current development rule."
                if update.control_state == "VERIFICATION_COMPLETE"
                else "Further admissible verification or human review may be required."
            ),
            claim_id=claim_id, gap_type=gap_type, probe_id=probe_id,
            evidence_id=update.evidence.evidence_id,
            decision=update.control_state, method_version=self.method_version,
        ))
