import pytest

from app.domain.evaluation import (
    HistoricalOutcomeEvaluation,
    DirectionalScore,
    validate_historical_evaluation,
)
from app.fixtures.candidate_a_evaluation import CANDIDATE_A_EVALUATION


def test_candidate_a_evaluation_preserves_direction_without_causal_upgrade():
    validate_historical_evaluation(CANDIDATE_A_EVALUATION)
    assert CANDIDATE_A_EVALUATION.directional_score is DirectionalScore.CONSISTENT
    assert CANDIDATE_A_EVALUATION.causal_attribution_established is False
    assert CANDIDATE_A_EVALUATION.numerical_forecast_applicable is False
    assert len(CANDIDATE_A_EVALUATION.counterevidence) == 6


def test_candidate_a_cannot_be_silently_upgraded_to_causal_claim():
    e = HistoricalOutcomeEvaluation(
        **{**CANDIDATE_A_EVALUATION.__dict__, "causal_attribution_established": True}
    )
    with pytest.raises(ValueError, match="exclusive causal attribution"):
        validate_historical_evaluation(e)


def test_candidate_a_cannot_emit_numerical_forecast_without_t5():
    e = HistoricalOutcomeEvaluation(
        **{**CANDIDATE_A_EVALUATION.__dict__, "numerical_forecast_applicable": True}
    )
    with pytest.raises(ValueError, match="numerical forecast is prohibited"):
        validate_historical_evaluation(e)
