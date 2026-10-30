from app.domain.baselines import (
    run_b0_news_signal,
    run_b1_event_exposure,
    run_b2_narrative,
    run_b3_etec,
)
from app.domain.comparison import comparison_rows
from app.domain.enums import OutputClass
from app.fixtures.f1_missing_link import F1_ASSESSMENTS


def test_b0_cannot_claim_more_than_event_signal_in_bounded_adapter():
    assert run_b0_news_signal(True).output_class is OutputClass.VERIFIED_EVENT_ONLY


def test_b1_caps_at_direct_exposure():
    assert run_b1_event_exposure(True, True).output_class is OutputClass.EXPOSURE_IDENTIFIED


def test_b2_can_record_ungated_downstream_narrative_for_later_scoring():
    r = run_b2_narrative(
        OutputClass.MECHANISM_SUPPORTED_SCENARIO,
        "Constructed persuasive downstream narrative.",
    )
    assert r.output_class is OutputClass.MECHANISM_SUPPORTED_SCENARIO
    assert r.structurally_gated is False


def test_b3_f1_stops_at_missing_t3():
    r, decision = run_b3_etec(F1_ASSESSMENTS)
    assert r.output_class is OutputClass.EXPOSURE_IDENTIFIED
    assert r.structurally_gated is True
    assert decision.stopping_transition.value == "T3_DOMESTIC_TRANSMISSION"


def test_comparison_preserves_outputs_without_declaring_a_winner():
    b0 = run_b0_news_signal(True)
    b1 = run_b1_event_exposure(True, True)
    b2 = run_b2_narrative(
        OutputClass.MECHANISM_SUPPORTED_SCENARIO, "Constructed narrative."
    )
    b3, _ = run_b3_etec(F1_ASSESSMENTS)
    rows = comparison_rows((b0, b1, b2, b3))
    assert [r.baseline_id for r in rows] == ["B0", "B1", "B2", "B3"]
    assert [r.claim_strength for r in rows] == [1, 2, 4, 2]
