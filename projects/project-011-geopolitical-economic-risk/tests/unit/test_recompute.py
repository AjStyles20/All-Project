from app.domain.enums import EdgeState, OutputClass, TransitionClass
from app.domain.models import TransitionAssessment
from app.domain.recompute import revise_and_recompute

CASE = "CASE-M4-001"


def a(t, s):
    return TransitionAssessment(CASE, t, s, ("EV",), "Initial admissible evidence.")


BASE = (
    a(TransitionClass.T1_EVENT_VERIFICATION, EdgeState.VERIFIED),
    a(TransitionClass.T2_EXPOSURE, EdgeState.VERIFIED),
    a(TransitionClass.T3_DOMESTIC_TRANSMISSION, EdgeState.SUPPORTED),
    a(TransitionClass.T4_LOCAL_SCENARIO, EdgeState.SUPPORTED),
)


def test_counterevidence_can_downgrade_exposure_and_recompute_dependents():
    r = revise_and_recompute(
        BASE,
        TransitionClass.T2_EXPOSURE,
        EdgeState.CONDITIONAL,
        "New diversification evidence makes measured exposure conditional.",
    )
    assert r.before.output_class is OutputClass.MECHANISM_SUPPORTED_SCENARIO
    assert r.after.output_class is OutputClass.VERIFIED_EVENT_ONLY
    assert r.after.stopping_transition is TransitionClass.T2_EXPOSURE
    assert r.revision.previous_state is EdgeState.VERIFIED
    assert r.revision.new_state is EdgeState.CONDITIONAL


def test_stale_transmission_edge_removes_downstream_scenario():
    r = revise_and_recompute(
        BASE,
        TransitionClass.T3_DOMESTIC_TRANSMISSION,
        EdgeState.STALE,
        "The mapping validity horizon expired.",
    )
    assert r.before.output_class is OutputClass.MECHANISM_SUPPORTED_SCENARIO
    assert r.after.output_class is OutputClass.EXPOSURE_IDENTIFIED
    assert r.after.stopping_state is EdgeState.STALE


def test_contradicted_event_collapses_entire_pathway():
    r = revise_and_recompute(
        BASE,
        TransitionClass.T1_EVENT_VERIFICATION,
        EdgeState.CONTRADICTED,
        "Authoritative reversal contradicts the original event scope.",
    )
    assert r.after.output_class is OutputClass.ABSTAIN_INSUFFICIENT_EVIDENCE
    assert r.after.stopping_transition is TransitionClass.T1_EVENT_VERIFICATION
    assert r.after.stopping_state is EdgeState.CONTRADICTED


def test_revision_requires_explanation():
    try:
        revise_and_recompute(BASE, TransitionClass.T2_EXPOSURE, EdgeState.CONTESTED, " ")
    except ValueError as exc:
        assert "reason is required" in str(exc)
    else:
        raise AssertionError("unexplained revision was accepted")
