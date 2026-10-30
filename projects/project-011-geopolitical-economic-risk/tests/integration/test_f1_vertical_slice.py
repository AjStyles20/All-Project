from datetime import datetime, timezone

from app.domain.audit import build_audit_trace
from app.domain.enums import EdgeState, OutputClass, TransitionClass
from app.fixtures.f1_missing_link import CASE_F1_001, F1_ASSESSMENTS, F1_EVIDENCE


def test_f1_end_to_end_stops_at_exposure_and_records_audit_trace():
    decision, trace = build_audit_trace(
        CASE_F1_001,
        F1_EVIDENCE,
        F1_ASSESSMENTS,
        generated_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )

    assert decision.output_class is OutputClass.EXPOSURE_IDENTIFIED
    assert trace.released_output is OutputClass.EXPOSURE_IDENTIFIED
    assert trace.passed_transitions == (
        TransitionClass.T1_EVENT_VERIFICATION,
        TransitionClass.T2_EXPOSURE,
    )
    assert trace.stopping_transition is TransitionClass.T3_DOMESTIC_TRANSMISSION
    assert trace.stopping_state is EdgeState.INSUFFICIENT
    assert trace.stopping_reason == "No admissible product-to-sector mapping is present."
    assert trace.evidence_ids == ("EV-F1-EVENT", "EV-F1-EXPOSURE")
    assert OutputClass.MECHANISM_SUPPORTED_SCENARIO in trace.prohibited_outputs
    assert OutputClass.MODEL_ESTIMATE in trace.prohibited_outputs
    assert OutputClass.CALIBRATED_FORECAST in trace.prohibited_outputs
