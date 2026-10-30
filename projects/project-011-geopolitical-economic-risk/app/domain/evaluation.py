"""Historical evaluation records kept separate from causal attribution."""
from dataclasses import dataclass
from enum import Enum


class DirectionalScore(str, Enum):
    CONSISTENT = "CONSISTENT"
    INCONSISTENT = "INCONSISTENT"
    INDETERMINATE = "INDETERMINATE"


class CounterevidenceState(str, Enum):
    MATERIAL = "MATERIAL"
    MATERIAL_COMPETING = "MATERIAL_COMPETING"
    MATERIAL_MITIGATION = "MATERIAL_MITIGATION"
    RELEVANT_UNQUANTIFIED = "RELEVANT_UNQUANTIFIED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class CounterevidenceItem:
    counterevidence_id: str
    description: str
    state: CounterevidenceState
    evidence_reference: str | None = None


@dataclass(frozen=True)
class HistoricalOutcomeEvaluation:
    case_id: str
    replay_mode: str
    target_family: str
    horizon: str
    directional_score: DirectionalScore
    causal_attribution_established: bool
    numerical_forecast_applicable: bool
    notes: str
    counterevidence: tuple[CounterevidenceItem, ...]


def validate_historical_evaluation(e: HistoricalOutcomeEvaluation) -> None:
    if e.replay_mode not in {"R1", "R2"}:
        raise ValueError("replay_mode must be R1 or R2")
    if not e.target_family.strip() or not e.horizon.strip() or not e.notes.strip():
        raise ValueError("target, horizon and notes are required")
    if e.numerical_forecast_applicable:
        raise ValueError("Candidate A has no T5 model eligibility; numerical forecast is prohibited")
    if e.causal_attribution_established:
        raise ValueError("Candidate A evidence does not establish exclusive causal attribution")
