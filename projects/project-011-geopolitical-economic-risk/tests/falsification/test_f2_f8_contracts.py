"""F2-F8 deterministic falsification-contract tests.

These fixtures test software invariants only. They are not historical validation.
"""
from datetime import datetime, timezone

import pytest

from app.domain.enums import EdgeState, OutputClass, SourceAuthorityTier, TransitionClass
from app.domain.invariants import validate_evidence
from app.domain.models import EconomicCase, EvidenceItem, TransitionAssessment
from app.domain.progression import evaluate_progression
from app.domain.recompute import revise_and_recompute

CASE_ID = "CASE-FALSIFICATION"


def a(t, s, reason="Frozen fixture."):
    return TransitionAssessment(CASE_ID, t, s, ("EV",), reason)


def test_f2_counterevidence_reversal_reduces_claim_strength():
    base = (
        a(TransitionClass.T1_EVENT_VERIFICATION, EdgeState.VERIFIED),
        a(TransitionClass.T2_EXPOSURE, EdgeState.VERIFIED),
        a(TransitionClass.T3_DOMESTIC_TRANSMISSION, EdgeState.SUPPORTED),
        a(TransitionClass.T4_LOCAL_SCENARIO, EdgeState.SUPPORTED),
    )
    r = revise_and_recompute(
        base, TransitionClass.T3_DOMESTIC_TRANSMISSION, EdgeState.CONTESTED,
        "Mitigation evidence contests the domestic transmission mechanism.",
    )
    assert r.before.output_class is OutputClass.MECHANISM_SUPPORTED_SCENARIO
    assert r.after.output_class is OutputClass.EXPOSURE_IDENTIFIED


def test_f3_contradictory_event_evidence_forces_abstention():
    decision = evaluate_progression((
        a(TransitionClass.T1_EVENT_VERIFICATION, EdgeState.CONTRADICTED,
          "Authoritative sources contradict the asserted event scope."),
        a(TransitionClass.T2_EXPOSURE, EdgeState.VERIFIED),
    ))
    assert decision.output_class is OutputClass.ABSTAIN_INSUFFICIENT_EVIDENCE
    assert decision.stopping_state is EdgeState.CONTRADICTED


def test_f4_stale_evidence_blocks_progression():
    decision = evaluate_progression((
        a(TransitionClass.T1_EVENT_VERIFICATION, EdgeState.VERIFIED),
        a(TransitionClass.T2_EXPOSURE, EdgeState.STALE, "Exposure evidence expired."),
    ))
    assert decision.output_class is OutputClass.VERIFIED_EVENT_ONLY
    assert decision.stopping_state is EdgeState.STALE


def test_f5_persuasive_narrative_cannot_replace_missing_required_edge():
    decision = evaluate_progression((
        a(TransitionClass.T1_EVENT_VERIFICATION, EdgeState.VERIFIED),
        a(TransitionClass.T2_EXPOSURE, EdgeState.VERIFIED),
        # No T3. A later narrative/scenario assessment must not bypass it.
        a(TransitionClass.T4_LOCAL_SCENARIO, EdgeState.SUPPORTED,
          "Constructed persuasive narrative predicts a local consequence."),
    ))
    assert decision.output_class is OutputClass.EXPOSURE_IDENTIFIED
    assert decision.stopping_transition is TransitionClass.T3_DOMESTIC_TRANSMISSION


def test_f6_negative_control_with_insufficient_nigeria_exposure_has_no_local_warning():
    decision = evaluate_progression((
        a(TransitionClass.T1_EVENT_VERIFICATION, EdgeState.VERIFIED),
        a(TransitionClass.T2_EXPOSURE, EdgeState.INSUFFICIENT,
          "No material Nigeria exposure is established in this negative control."),
    ))
    assert decision.output_class is OutputClass.VERIFIED_EVENT_ONLY
    assert OutputClass.TRANSMISSION_SUPPORTED in decision.prohibited_outputs
    assert OutputClass.MECHANISM_SUPPORTED_SCENARIO in decision.prohibited_outputs


def test_f7_scenario_without_validated_model_cannot_emit_number_or_forecast():
    decision = evaluate_progression((
        a(TransitionClass.T1_EVENT_VERIFICATION, EdgeState.VERIFIED),
        a(TransitionClass.T2_EXPOSURE, EdgeState.VERIFIED),
        a(TransitionClass.T3_DOMESTIC_TRANSMISSION, EdgeState.SUPPORTED),
        a(TransitionClass.T4_LOCAL_SCENARIO, EdgeState.SUPPORTED),
        a(TransitionClass.T5_MODEL_ESTIMATE_ELIGIBILITY, EdgeState.INSUFFICIENT,
          "No independently validated quantitative model is eligible."),
        a(TransitionClass.T6_CALIBRATED_FORECAST, EdgeState.SUPPORTED),
    ))
    assert decision.output_class is OutputClass.MECHANISM_SUPPORTED_SCENARIO
    assert OutputClass.MODEL_ESTIMATE in decision.prohibited_outputs
    assert OutputClass.CALIBRATED_FORECAST in decision.prohibited_outputs


def test_f8_later_data_revision_is_rejected_by_historical_information_cutoff():
    case = EconomicCase(
        CASE_ID, "Nigeria", "constructed_event",
        datetime(2025, 1, 1, tzinfo=timezone.utc), "historical-v1",
    )
    revised_later = EvidenceItem(
        "EV-REVISION", CASE_ID, TransitionClass.T2_EXPOSURE,
        SourceAuthorityTier.STATISTICAL_INSTITUTION,
        "constructed://later-revision",
        datetime(2025, 2, 1, tzinfo=timezone.utc),
        "revised-v2", "Nigeria",
    )
    with pytest.raises(ValueError, match="information cutoff"):
        validate_evidence(case, revised_later)
