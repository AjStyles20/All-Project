from datetime import datetime, timezone

from app.domain.enums import ClaimApplicability, EvidenceState, EvidenceType
from app.domain.models import EvidenceItem
from app.services.cc3_response_evaluator import CC3ProbeResponse
from app.services.evidence_evaluator import EvidenceEvaluator
from app.services.gap_detector import GapDetector
from app.services.probe_catalog import cc3_development_probes
from app.services.probe_selector import ProbeSelector
from app.services.verification_workflow import VerificationWorkflow


def test_case_dev_003_b4_vertical_slice():
    initial_evidence = [
        EvidenceItem(
            evidence_id="EV-EXEC-003",
            case_id="CASE-DEV-003",
            evidence_type=EvidenceType.EXECUTION,
            content="Examiner-supplied tests passed.",
            source_type="automated_test",
            created_at=datetime(2026, 9, 20, 9, 0, tzinfo=timezone.utc),
        )
    ]

    initial = EvidenceEvaluator().evaluate("CC3", initial_evidence)
    assert initial.state is EvidenceState.UNRESOLVED

    gap = GapDetector().detect(
        claim_id="CC3",
        applicability=ClaimApplicability.REQUIRED,
        state=initial.state,
    )
    assert gap is not None
    assert gap.gap_type == "EG-T3"

    selection = ProbeSelector().select(
        gap_type=gap.gap_type,
        claim_id=gap.claim_id,
        probes=cc3_development_probes(),
    )
    assert selection.selected_probe is not None
    assert selection.selected_probe.probe_id == "VP-CC3-02"

    update = VerificationWorkflow().apply_cc3_response(
        case_id="CASE-DEV-003",
        selection=selection,
        response=CC3ProbeResponse(
            test_input="[1, 3, 5]",
            expected_result="[]",
            usefulness_reason="Checks behavior when there are no even values.",
            input_relevant=True,
            expected_result_correct=True,
            reason_defensible=True,
        ),
        evidence_id="EV-VERIFY-003-01",
        recorded_at=datetime(2026, 9, 20, 9, 10, tzinfo=timezone.utc),
    )

    assert update.state_record.state is EvidenceState.SUPPORTED
    assert update.control_state == "VERIFICATION_COMPLETE"
