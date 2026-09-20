from app.domain.candidate_d_fixture import CANDIDATE_D, CANDIDATE_D_OUTCOME

def test_candidate_d_is_r2_and_stops_before_model_estimate():
    assert CANDIDATE_D.replay_mode == "R2"
    assert CANDIDATE_D.t4_state == "SCENARIO_SUPPORTED"
    assert CANDIDATE_D.t5_state == "WITHHELD"
    assert CANDIDATE_D.t6_state == "WITHHELD"

def test_candidate_d_outcome_is_directional_not_causal():
    assert CANDIDATE_D_OUTCOME.directional_score == "CONSISTENT"
    assert CANDIDATE_D_OUTCOME.causal_attribution == "NOT_ESTABLISHED"
    assert CANDIDATE_D_OUTCOME.numerical_forecast == "NOT_APPLICABLE"

def test_candidate_d_preserves_predeclared_counterchannels():
    text = CANDIDATE_D.scenario.lower()
    assert "crude-oil revenue" in text
    assert "production" in text
    assert "fx" in text
    assert "policy change" in text
