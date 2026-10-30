from app.domain.evaluation import (
    CounterevidenceItem,
    CounterevidenceState,
    DirectionalScore,
    HistoricalOutcomeEvaluation,
)

CANDIDATE_A_EVALUATION = HistoricalOutcomeEvaluation(
    case_id="P003-RU-WHEAT-A",
    replay_mode="R2",
    target_family="NBS Bread and cereals / wheat-flour and bread price observations",
    horizon="3-6 months after 2022-02-24 event anchor",
    directional_score=DirectionalScore.CONSISTENT,
    causal_attribution_established=False,
    numerical_forecast_applicable=False,
    notes=(
        "Observed bread/flour direction is consistent with the frozen T4 scenario; "
        "pre-existing inflation and competing channels prevent exclusive attribution."
    ),
    counterevidence=(
        CounterevidenceItem("C1", "Pre-existing bread-price trend", CounterevidenceState.MATERIAL),
        CounterevidenceItem("C2", "Foreign-exchange scarcity", CounterevidenceState.MATERIAL_COMPETING),
        CounterevidenceItem("C3", "Supplier substitution/diversification", CounterevidenceState.MATERIAL_MITIGATION),
        CounterevidenceItem("C4", "Freight/energy/logistics pressure", CounterevidenceState.MATERIAL_COMPETING),
        CounterevidenceItem("C5", "Domestic wheat supply", CounterevidenceState.RELEVANT_UNQUANTIFIED),
        CounterevidenceItem("C6", "Inventories/contracts/policy effects", CounterevidenceState.UNKNOWN),
    ),
)
