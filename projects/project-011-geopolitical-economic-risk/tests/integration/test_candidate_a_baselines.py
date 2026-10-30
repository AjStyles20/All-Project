from app.domain.comparison import comparison_rows
from app.domain.enums import OutputClass
from app.fixtures.candidate_a_baselines import candidate_a_baselines


def test_candidate_a_same_information_baseline_outputs_are_recorded():
    results, decision = candidate_a_baselines()
    rows = comparison_rows(results)
    assert [r.baseline_id for r in rows] == ["B0", "B1", "B2", "B3"]
    assert [r.output_class for r in rows] == [
        OutputClass.VERIFIED_EVENT_ONLY,
        OutputClass.EXPOSURE_IDENTIFIED,
        OutputClass.MECHANISM_SUPPORTED_SCENARIO,
        OutputClass.MECHANISM_SUPPORTED_SCENARIO,
    ]
    assert decision.stopping_transition.value == "T5_MODEL_ESTIMATE_ELIGIBILITY"


def test_candidate_a_b3_prohibits_model_and_calibrated_outputs():
    _, decision = candidate_a_baselines()
    assert OutputClass.MODEL_ESTIMATE in decision.prohibited_outputs
    assert OutputClass.CALIBRATED_FORECAST in decision.prohibited_outputs
