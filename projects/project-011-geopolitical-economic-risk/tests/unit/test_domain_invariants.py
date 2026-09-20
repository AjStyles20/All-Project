from datetime import datetime, timezone

import pytest

from app.domain.enums import EdgeState, OutputClass, SourceAuthorityTier, TransitionClass
from app.domain.invariants import validate_evidence, weakest_link_output
from app.domain.models import EconomicCase, EvidenceItem, TransitionAssessment


CUT = datetime(2026, 1, 1, tzinfo=timezone.utc)
CASE = EconomicCase("CASE-F1-001", "Nigeria", "export_restriction", CUT, "1.0")


def assessment(t, state):
    return TransitionAssessment(CASE.case_id, t, state, ("EV-1",), "Frozen fixture.")


def test_f1_missing_domestic_transmission_caps_output_at_exposure():
    result = weakest_link_output((
        assessment(TransitionClass.T1_EVENT_VERIFICATION, EdgeState.VERIFIED),
        assessment(TransitionClass.T2_EXPOSURE, EdgeState.VERIFIED),
        assessment(TransitionClass.T3_DOMESTIC_TRANSMISSION, EdgeState.INSUFFICIENT),
    ))
    assert result is OutputClass.EXPOSURE_IDENTIFIED


def test_transition_cannot_be_skipped_to_release_stronger_claim():
    result = weakest_link_output((
        assessment(TransitionClass.T1_EVENT_VERIFICATION, EdgeState.VERIFIED),
        assessment(TransitionClass.T2_EXPOSURE, EdgeState.VERIFIED),
        assessment(TransitionClass.T4_LOCAL_SCENARIO, EdgeState.SUPPORTED),
    ))
    assert result is OutputClass.EXPOSURE_IDENTIFIED


def test_contested_required_edge_stops_progression():
    result = weakest_link_output((
        assessment(TransitionClass.T1_EVENT_VERIFICATION, EdgeState.VERIFIED),
        assessment(TransitionClass.T2_EXPOSURE, EdgeState.CONTESTED),
    ))
    assert result is OutputClass.VERIFIED_EVENT_ONLY


def test_no_model_eligibility_means_no_numeric_model_output():
    result = weakest_link_output((
        assessment(TransitionClass.T1_EVENT_VERIFICATION, EdgeState.VERIFIED),
        assessment(TransitionClass.T2_EXPOSURE, EdgeState.VERIFIED),
        assessment(TransitionClass.T3_DOMESTIC_TRANSMISSION, EdgeState.SUPPORTED),
        assessment(TransitionClass.T4_LOCAL_SCENARIO, EdgeState.SUPPORTED),
        assessment(TransitionClass.T5_MODEL_ESTIMATE_ELIGIBILITY, EdgeState.INSUFFICIENT),
        assessment(TransitionClass.T6_CALIBRATED_FORECAST, EdgeState.VERIFIED),
    ))
    assert result is OutputClass.MECHANISM_SUPPORTED_SCENARIO


def test_future_evidence_is_rejected_by_information_cutoff():
    ev = EvidenceItem(
        "EV-FUTURE", CASE.case_id, TransitionClass.T1_EVENT_VERIFICATION,
        SourceAuthorityTier.OFFICIAL_PRIMARY, "official-source",
        datetime(2026, 1, 2, tzinfo=timezone.utc), "v1", "Nigeria",
    )
    with pytest.raises(ValueError, match="information cutoff"):
        validate_evidence(CASE, ev)
