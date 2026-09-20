"""Comparison records for B0-B3 without declaring empirical superiority."""
from dataclasses import dataclass

from .baselines import BaselineResult
from .enums import OutputClass


OUTPUT_RANK = {
    OutputClass.ABSTAIN_INSUFFICIENT_EVIDENCE: 0,
    OutputClass.VERIFIED_EVENT_ONLY: 1,
    OutputClass.EXPOSURE_IDENTIFIED: 2,
    OutputClass.TRANSMISSION_SUPPORTED: 3,
    OutputClass.MECHANISM_SUPPORTED_SCENARIO: 4,
    OutputClass.MODEL_ESTIMATE: 5,
    OutputClass.CALIBRATED_FORECAST: 6,
}


@dataclass(frozen=True)
class ComparisonRow:
    baseline_id: str
    output_class: OutputClass
    claim_strength: int
    structurally_gated: bool


def comparison_rows(results: tuple[BaselineResult, ...]) -> tuple[ComparisonRow, ...]:
    seen = set()
    rows = []
    for result in results:
        if result.baseline_id in seen:
            raise ValueError(f"duplicate baseline {result.baseline_id}")
        seen.add(result.baseline_id)
        rows.append(ComparisonRow(
            result.baseline_id,
            result.output_class,
            OUTPUT_RANK[result.output_class],
            result.structurally_gated,
        ))
    return tuple(rows)
