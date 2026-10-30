"""Common runner for P001 B0-B3 comparison methods.

The runner applies each method to the same case-level evidence collection while
preserving each baseline's information boundary. It records exposure; it does
not claim that any baseline is scientifically better.
"""
from dataclasses import dataclass

from app.domain.models import EvidenceItem
from app.services.baseline_engines import (
    B0Engine, B1Engine, B2Engine, B3Engine, BaselineResult,
)


@dataclass(frozen=True)
class BaselineExperimentResult:
    case_id: str
    claim_id: str
    results: tuple[BaselineResult, ...]

    def by_method(self, method: str) -> BaselineResult:
        for result in self.results:
            if result.method == method:
                return result
        raise KeyError(method)


class BaselineExperimentRunner:
    """Run B0-B3 against one frozen evidence collection."""

    def __init__(self):
        self.engines = (B0Engine(), B1Engine(), B2Engine(), B3Engine())

    def run(
        self, *, case_id: str, claim_id: str, evidence: list[EvidenceItem]
    ) -> BaselineExperimentResult:
        if any(item.case_id != case_id for item in evidence):
            raise ValueError("All evidence must belong to the experiment case.")
        results = tuple(engine.evaluate(claim_id, evidence) for engine in self.engines)
        return BaselineExperimentResult(
            case_id=case_id, claim_id=claim_id, results=results
        )
