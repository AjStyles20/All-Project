from datetime import datetime, timezone

from app.domain.audit import AuditEventType
from app.domain.enums import ClaimApplicability, EvidenceState, EvidenceType
from app.domain.models import (
    CaseClaim, ClaimEvidenceLink, CompetenceClaim, EvidenceItem,
    EvidenceStateRecord, ProgrammingCase,
)
from app.persistence.audit_repository import AuditRepository
from app.persistence.database import Database
from app.persistence.repositories import P001Repository
from app.services.audit_trail import AuditTrailRecorder
from app.services.cc3_response_evaluator import CC3ProbeResponse
from app.services.evidence_evaluator import EvidenceEvaluator
from app.services.gap_detector import GapDetector
from app.services.probe_catalog import cc3_development_probes
from app.services.probe_selector import ProbeSelector
from app.services.verification_workflow import VerificationWorkflow


def test_case_dev_003_produces_persistent_machine_readable_audit_trace(tmp_path):
    db = Database(tmp_path / "audit-e2e.db")
    db.initialize()
    repository = P001Repository(db)
    audits = AuditRepository(db)
    recorder = AuditTrailRecorder(audits)

    repository.add_case(ProgrammingCase(
        case_id="CASE-DEV-003", title="Find even numbers",
        task_description="Return even numbers in a list.", language="python",
    ))
    repository.add_claim(CompetenceClaim(
        claim_id="CC3", name="Test Design",
        definition="Independently design relevant tests and justify them.",
    ))
    repository.add_case_claim(CaseClaim(
        case_id="CASE-DEV-003", claim_id="CC3",
        applicability=ClaimApplicability.REQUIRED,
    ))
    supplied = EvidenceItem(
        evidence_id="EV-EXEC-003", case_id="CASE-DEV-003",
        evidence_type=EvidenceType.EXECUTION,
        content="Examiner-supplied tests passed.", source_type="automated_test",
        created_at=datetime(2026, 9, 20, 11, 0, tzinfo=timezone.utc),
    )
    repository.add_evidence(supplied)
    repository.link_evidence(ClaimEvidenceLink(
        case_id="CASE-DEV-003", claim_id="CC3", evidence_id=supplied.evidence_id,
        rationale="Relevant execution evidence; insufficient for independent test design.",
    ))

    initial = EvidenceEvaluator().evaluate(
        "CC3", repository.get_evidence_for_claim("CASE-DEV-003", "CC3")
    )
    repository.append_evidence_state(EvidenceStateRecord(
        case_id="CASE-DEV-003", claim_id="CC3", state=initial.state,
        rationale=initial.rationale,
        recorded_at=datetime(2026, 9, 20, 11, 1, tzinfo=timezone.utc),
        source="B4-v1.0-development",
    ))
    recorder.record_initial_state(
        event_id="AUD-003-01", case_id="CASE-DEV-003", claim_id="CC3",
        state=initial.state, rationale=initial.rationale,
        recorded_at=datetime(2026, 9, 20, 11, 1, tzinfo=timezone.utc),
    )

    gap = GapDetector().detect(
        claim_id="CC3", applicability=ClaimApplicability.REQUIRED, state=initial.state
    )
    assert gap is not None
    recorder.record_gap(
        event_id="AUD-003-02", case_id="CASE-DEV-003", gap=gap,
        recorded_at=datetime(2026, 9, 20, 11, 2, tzinfo=timezone.utc),
    )

    selection = ProbeSelector().select(
        gap_type=gap.gap_type, claim_id=gap.claim_id,
        probes=cc3_development_probes(),
    )
    recorder.record_selection(
        event_id="AUD-003-03", case_id="CASE-DEV-003", selection=selection,
        recorded_at=datetime(2026, 9, 20, 11, 3, tzinfo=timezone.utc),
    )
    assert selection.selected_probe is not None

    update = VerificationWorkflow().apply_cc3_response(
        case_id="CASE-DEV-003", selection=selection,
        response=CC3ProbeResponse(
            test_input="[1, 3, 5]", expected_result="[]",
            usefulness_reason="Checks behavior when no even values exist.",
            input_relevant=True, expected_result_correct=True, reason_defensible=True,
        ),
        evidence_id="EV-VERIFY-003-01",
        recorded_at=datetime(2026, 9, 20, 11, 10, tzinfo=timezone.utc),
    )
    repository.add_evidence(update.evidence)
    repository.link_evidence(ClaimEvidenceLink(
        case_id="CASE-DEV-003", claim_id="CC3",
        evidence_id=update.evidence.evidence_id,
        rationale="Targeted independent verification evidence for EG-T3.",
    ))
    repository.append_evidence_state(update.state_record)
    recorder.record_verification_update(
        result_event_id="AUD-003-04", state_event_id="AUD-003-05",
        control_event_id="AUD-003-06", case_id="CASE-DEV-003", claim_id="CC3",
        gap_type=gap.gap_type, probe_id=selection.selected_probe.probe_id,
        from_state=EvidenceState.UNRESOLVED, update=update,
        recorded_at=datetime(2026, 9, 20, 11, 10, tzinfo=timezone.utc),
    )

    trace = audits.list_for_case("CASE-DEV-003")
    assert [event.event_type for event in trace] == [
        AuditEventType.EVIDENCE_STATE_RECORDED,
        AuditEventType.GAP_DETECTED,
        AuditEventType.PROBE_SELECTION,
        AuditEventType.PROBE_RESULT_RECORDED,
        AuditEventType.EVIDENCE_STATE_RECORDED,
        AuditEventType.CONTROL_DECISION,
    ]
    assert trace[0].to_state == "UNRESOLVED"
    assert trace[1].gap_type == "EG-T3"
    assert trace[2].probe_id == "VP-CC3-02"
    assert trace[4].from_state == "UNRESOLVED"
    assert trace[4].to_state == "SUPPORTED"
    assert trace[5].decision == "VERIFICATION_COMPLETE"
