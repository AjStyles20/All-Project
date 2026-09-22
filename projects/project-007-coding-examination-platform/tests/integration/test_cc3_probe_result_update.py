from datetime import datetime, timezone

from app.domain.enums import EvidenceState, EvidenceType
from app.services.cc3_response_evaluator import CC3ProbeResponse
from app.services.probe_catalog import cc3_development_probes
from app.services.probe_selector import ProbeSelector
from app.services.verification_workflow import VerificationWorkflow


def test_case_dev_003_valid_probe_response_updates_cc3_to_supported():
    selection = ProbeSelector().select(
        gap_type="EG-T3",
        claim_id="CC3",
        probes=cc3_development_probes(),
    )
    update = VerificationWorkflow().apply_cc3_response(
        case_id="CASE-DEV-003",
        selection=selection,
        response=CC3ProbeResponse(
            test_input="[1, 3, 5]",
            expected_result="[]",
            usefulness_reason=(
                "It checks the boundary where the input contains no even values."
            ),
            input_relevant=True,
            expected_result_correct=True,
            reason_defensible=True,
        ),
        evidence_id="EV-VERIFY-003-01",
        recorded_at=datetime(2026, 9, 20, 9, 10, tzinfo=timezone.utc),
    )

    assert update.evidence.evidence_type is EvidenceType.VERIFICATION
    assert update.state_record.state is EvidenceState.SUPPORTED
    assert update.control_state == "VERIFICATION_COMPLETE"


def test_partial_response_does_not_stop_verification():
    selection = ProbeSelector().select(
        gap_type="EG-T3",
        claim_id="CC3",
        probes=cc3_development_probes(),
    )
    update = VerificationWorkflow().apply_cc3_response(
        case_id="CASE-DEV-003",
        selection=selection,
        response=CC3ProbeResponse(
            test_input="[1, 3, 5]",
            expected_result="[]",
            usefulness_reason="",
            input_relevant=True,
            expected_result_correct=True,
            reason_defensible=False,
        ),
        evidence_id="EV-VERIFY-003-02",
        recorded_at=datetime(2026, 9, 20, 9, 11, tzinfo=timezone.utc),
    )

    assert update.state_record.state is EvidenceState.PARTIAL
    assert update.control_state == "CONTINUE_VERIFICATION"
