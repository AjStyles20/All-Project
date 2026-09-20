from datetime import datetime, timezone

from app.domain.audit import AuditEventType
from app.domain.enums import ClaimApplicability, EvidenceState, EvidenceType
from app.domain.models import (
    CaseClaim, ClaimEvidenceLink, CompetenceClaim, EvidenceItem, ProgrammingCase,
)
from app.domain.verification_run import VerificationRunStatus
from app.persistence.audit_repository import AuditRepository
from app.persistence.database import Database
from app.persistence.probe_audit_repository import ProbeAuditRepository
from app.persistence.repositories import P001Repository
from app.persistence.verification_run_repository import VerificationRunRepository
from app.services.b4_orchestrator import B4Orchestrator
from app.services.cc3_response_evaluator import CC3ProbeResponse


def test_b4_orchestrator_runs_persistent_cc3_path_end_to_end(tmp_path):
    db = Database(tmp_path / "b4.db")
    db.initialize()
    repo = P001Repository(db)
    runs = VerificationRunRepository(db)
    audits = AuditRepository(db)
    probe_audits = ProbeAuditRepository(db)
    engine = B4Orchestrator(repo, runs, audits, probe_audits)

    repo.add_case(ProgrammingCase(
        case_id="CASE-DEV-003", title="Find even numbers",
        task_description="Return even numbers in a list.", language="python",
    ))
    repo.add_claim(CompetenceClaim(
        claim_id="CC3", name="Test Design",
        definition="Independently design relevant tests and justify them.",
    ))
    repo.add_case_claim(CaseClaim(
        case_id="CASE-DEV-003", claim_id="CC3",
        applicability=ClaimApplicability.REQUIRED,
    ))
    supplied = EvidenceItem(
        evidence_id="EV-EXEC-003", case_id="CASE-DEV-003",
        evidence_type=EvidenceType.EXECUTION,
        content="Examiner-supplied tests passed.", source_type="automated_test",
        created_at=datetime(2026, 9, 20, 10, 0, tzinfo=timezone.utc),
    )
    repo.add_evidence(supplied)
    repo.link_evidence(ClaimEvidenceLink(
        case_id="CASE-DEV-003", claim_id="CC3", evidence_id=supplied.evidence_id,
        rationale="Relevant but insufficient for independent test design.",
    ))

    start = engine.start_cc3(
        run_id="RUN-003-01", case_id="CASE-DEV-003",
        started_at=datetime(2026, 9, 20, 10, 1, tzinfo=timezone.utc),
    )
    assert start.state is EvidenceState.UNRESOLVED
    assert start.selection is not None
    assert start.selection.selected_probe is not None
    assert start.selection.selected_probe.probe_id == "VP-CC3-02"
    assert start.control_decision == "CONTINUE_VERIFICATION"

    update = engine.submit_cc3_response(
        run_id="RUN-003-01",
        response=CC3ProbeResponse(
            test_input="[1, 3, 5]", expected_result="[]",
            usefulness_reason="Checks the no-even-values boundary.",
            input_relevant=True, expected_result_correct=True, reason_defensible=True,
        ),
        evidence_id="EV-VERIFY-003-01",
        recorded_at=datetime(2026, 9, 20, 10, 5, tzinfo=timezone.utc),
    )
    assert update.state_record.state is EvidenceState.SUPPORTED
    assert update.control_state == "VERIFICATION_COMPLETE"

    stored_run = runs.get("RUN-003-01")
    assert stored_run is not None
    assert stored_run.status is VerificationRunStatus.VERIFICATION_COMPLETE
    assert runs.used_probe_ids("RUN-003-01") == frozenset({"VP-CC3-02"})

    states = repo.list_evidence_states("CASE-DEV-003", "CC3")
    assert [s.state for s in states] == [EvidenceState.UNRESOLVED, EvidenceState.SUPPORTED]

    trace = audits.list_for_case("CASE-DEV-003")
    assert [e.event_type for e in trace] == [
        AuditEventType.EVIDENCE_STATE_RECORDED,
        AuditEventType.GAP_DETECTED,
        AuditEventType.PROBE_SELECTION,
        AuditEventType.PROBE_RESULT_RECORDED,
        AuditEventType.EVIDENCE_STATE_RECORDED,
        AuditEventType.CONTROL_DECISION,
    ]

    candidates = probe_audits.list_for_event("RUN-003-01-SELECT-01")
    dispositions = {c.disposition.probe_id: c.disposition.disposition for c in candidates}
    assert dispositions == {
        "VP-CC3-01": "REJECTED_INSUFFICIENT",
        "VP-CC3-02": "SELECTED",
        "VP-CC3-03": "REJECTED_HIGHER_BURDEN",
    }
