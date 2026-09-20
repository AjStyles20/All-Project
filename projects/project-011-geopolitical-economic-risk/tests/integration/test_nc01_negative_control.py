from app.domain.enums import OutputClass, TransitionClass
from app.fixtures.nc01_urea_negative_control import nc01_baselines


def test_nc01_b3_stops_at_direct_exposure_edge():
    _, decision = nc01_baselines()
    assert decision.output_class == OutputClass.VERIFIED_EVENT_ONLY
    assert decision.stopping_transition == TransitionClass.T2_EXPOSURE
    assert OutputClass.EXPOSURE_IDENTIFIED in decision.prohibited_outputs
    assert OutputClass.MECHANISM_SUPPORTED_SCENARIO in decision.prohibited_outputs


def test_nc01_b1_does_not_release_exposure_when_direct_exposure_is_negligible():
    results, _ = nc01_baselines()
    b1 = results[1]
    assert b1.output_class == OutputClass.VERIFIED_EVENT_ONLY


def test_nc01_placeholder_b2_is_explicitly_not_ground_truth():
    results, _ = nc01_baselines()
    b2 = results[2]
    assert b2.output_class == OutputClass.MECHANISM_SUPPORTED_SCENARIO
    assert b2.structurally_gated is False
