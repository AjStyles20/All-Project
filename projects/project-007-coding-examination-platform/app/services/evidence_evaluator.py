"""Deterministic evidence evaluation for the P001 research prototype.

M2 starts deliberately narrowly with CC3 (Test Design). The evaluator does not
infer authorship, misconduct, or general programming competence.
"""
from dataclasses import dataclass
from typing import Iterable

from app.domain.enums import EvidenceState, EvidenceType
from app.domain.models import EvidenceItem


@dataclass(frozen=True)
class EvaluationResult:
    state: EvidenceState
    rationale: str


class EvidenceEvaluator:
    """Evaluate bounded competence claims using frozen development rules."""

    def evaluate(self, claim_id: str, evidence: Iterable[EvidenceItem]) -> EvaluationResult:
        items = list(evidence)

        if claim_id == "CC3":
            return self._evaluate_cc3(items)

        return EvaluationResult(
            state=EvidenceState.UNRESOLVED,
            rationale=f"No frozen evaluation rule exists yet for {claim_id}.",
        )

    def _evaluate_cc3(self, evidence: list[EvidenceItem]) -> EvaluationResult:
        verification_items = [
            item for item in evidence if item.evidence_type is EvidenceType.VERIFICATION
        ]

        # M2-v0.1 intentionally does not parse free text to manufacture a competence
        # judgment. Until a structured CC3 verification result exists, the claim
        # remains unresolved.
        if not verification_items:
            return EvaluationResult(
                state=EvidenceState.UNRESOLVED,
                rationale=(
                    "No independent test-design verification evidence is available. "
                    "Passing supplied tests or possessing a correct artifact does not "
                    "by itself establish CC3 Test Design."
                ),
            )

        return EvaluationResult(
            state=EvidenceState.UNRESOLVED,
            rationale=(
                "Verification evidence exists, but M2-v0.1 has no frozen structured "
                "CC3 response rubric yet; automated support is therefore withheld."
            ),
        )
