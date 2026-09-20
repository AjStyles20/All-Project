"""Machine-readable M8 Candidate D R2 historical case.

Outcome evidence is deliberately separate from the pre-outcome pathway.
"""
from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class CandidateDOutcome:
    directional_score: str = "CONSISTENT"
    causal_attribution: str = "NOT_ESTABLISHED"
    numerical_forecast: str = "NOT_APPLICABLE"
    later_fuel_subsidy_gdp_2021: float = 1.1
    later_fuel_subsidy_gdp_2022: float = 2.2

@dataclass(frozen=True)
class CandidateDFixture:
    case_id: str = "P003-D"
    replay_mode: str = "R2"
    target: str = "PMS subsidy / fiscal burden"
    t1_state: str = "SUPPORTED"
    t2_state: str = "SUPPORTED"
    t3_state: str = "SUPPORTED"
    t4_state: str = "SCENARIO_SUPPORTED"
    t5_state: str = "WITHHELD"
    t6_state: str = "WITHHELD"
    scenario: str = (
        "Following a material external increase in imported refined-fuel/PMS costs, "
        "Nigeria faces upward pressure on the fiscal burden of maintaining regulated "
        "PMS prices over subsequent months, conditional on the subsidy regime remaining "
        "in place and unless sufficiently offset by higher net crude-oil revenue, stronger "
        "production, favourable FX, lower volumes, or policy change."
    )
    exclusions: Tuple[str, ...] = (
        "no exclusive causal attribution to the Russia-Ukraine war",
        "no numerical subsidy forecast",
        "no probability forecast",
        "no claim that all HS2710 imports are PMS",
        "no T5/T6 eligibility",
    )

CANDIDATE_D = CandidateDFixture()
CANDIDATE_D_OUTCOME = CandidateDOutcome()
