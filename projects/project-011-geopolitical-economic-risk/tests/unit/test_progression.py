from app.domain.enums import EdgeState, OutputClass, TransitionClass
from app.domain.models import TransitionAssessment
from app.domain.progression import evaluate_progression

CASE_ID = "CASE-M2-001"


def a(transition, state, rationale="Frozen assessment rationale."):
    return TransitionAssessment(CASE_ID, transition, state, ("EV-1",), rationale)


def test_explains_missing_t3_as_exact_weakest_link():
    decision = evaluate_progression((
        a(TransitionClass.T1_EVENT_VERIFICATION, EdgeState.VERIFIED),
        a(TransitionClass.T2_EXPOSURE, EdgeState.VERIFIED),
    ))
    assert decision.output_class is OutputClass.EXPOSURE_IDENTIFIED
    assert decision.stopping_transition is TransitionClass.T3_DOMESTIC_TRANSMISSION
    assert decision.stopping_state is None
    assert "no assessment" in decision.stopping_reason
    assert OutputClass.TRANSMISSION_SUPPORTED in decision.prohibited_outputs
    assert OutputClass.CALIBRATED_FORECAST in decision.prohibited_outputs


def test_preserves_reason_for_insufficient_edge():
    decision = evaluate_progression((
        a(TransitionClass.T1_EVENT_VERIFICATION, EdgeState.VERIFIED),
        a(TransitionClass.T2_EXPOSURE, EdgeState.VERIFIED),
        a(
            TransitionClass.T3_DOMESTIC_TRANSMISSION,
            EdgeState.INSUFFICIENT,
            "No admissible product-to-sector mapping is present.",
        ),
    ))
    assert decision.output_class is OutputClass.EXPOSURE_IDENTIFIED
    assert decision.stopping_state is EdgeState.INSUFFICIENT
    assert decision.stopping_reason == "No admissible product-to-sector mapping is present."


def test_later_supported_edge_cannot_hide_earlier_contested_edge():
    decision = evaluate_progression((
        a(TransitionClass.T1_EVENT_VERIFICATION, EdgeState.VERIFIED),
        a(TransitionClass.T2_EXPOSURE, EdgeState.CONTESTED, "Exposure sources conflict."),
        a(TransitionClass.T3_DOMESTIC_TRANSMISSION, EdgeState.SUPPORTED),
        a(TransitionClass.T4_LOCAL_SCENARIO, EdgeState.SUPPORTED),
    ))
    assert decision.output_class is OutputClass.VERIFIED_EVENT_ONLY
    assert decision.stopping_transition is TransitionClass.T2_EXPOSURE
    assert decision.stopping_state is EdgeState.CONTESTED


def test_duplicate_transition_assessments_are_rejected():
    try:
        evaluate_progression((
            a(TransitionClass.T1_EVENT_VERIFICATION, EdgeState.VERIFIED),
            a(TransitionClass.T1_EVENT_VERIFICATION, EdgeState.SUPPORTED),
        ))
    except ValueError as exc:
        assert "duplicate assessment" in str(exc)
    else:
        raise AssertionError("duplicate transition assessment was accepted")


def test_full_chain_has_no_prohibited_output():
    decision = evaluate_progression((
        a(TransitionClass.T1_EVENT_VERIFICATION, EdgeState.VERIFIED),
        a(TransitionClass.T2_EXPOSURE, EdgeState.VERIFIED),
        a(TransitionClass.T3_DOMESTIC_TRANSMISSION, EdgeState.SUPPORTED),
        a(TransitionClass.T4_LOCAL_SCENARIO, EdgeState.SUPPORTED),
        a(TransitionClass.T5_MODEL_ESTIMATE_ELIGIBILITY, EdgeState.SUPPORTED),
        a(TransitionClass.T6_CALIBRATED_FORECAST, EdgeState.SUPPORTED),
    ))
    assert decision.output_class is OutputClass.CALIBRATED_FORECAST
    assert decision.stopping_transition is None
    assert decision.prohibited_outputs == ()
