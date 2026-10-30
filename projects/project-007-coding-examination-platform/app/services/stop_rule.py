"""Generic verification control rule for the P001 research prototype.

This rule decides control flow only. It does not assign competence states,
misconduct, marks, or pass/fail outcomes.
"""
from dataclasses import dataclass

from app.domain.enums import ClaimApplicability, EvidenceState


@dataclass(frozen=True)
class ClaimControlInput:
    claim_id: str
    applicability: ClaimApplicability
    state: EvidenceState
    has_adequate_unused_probe: bool


@dataclass(frozen=True)
class StopDecision:
    decision: str
    rationale: str
    blocking_claim_ids: tuple[str, ...] = ()


class StopRule:
    def decide(self, claims: list[ClaimControlInput]) -> StopDecision:
        required = [c for c in claims if c.applicability is ClaimApplicability.REQUIRED]
        if not required:
            return StopDecision(
                decision="VERIFICATION_COMPLETE",
                rationale="No REQUIRED competence claims remain for verification.",
            )

        contradicted = [c.claim_id for c in required if c.state is EvidenceState.CONTRADICTED]
        if contradicted:
            return StopDecision(
                decision="HUMAN_REVIEW_REQUIRED",
                rationale=(
                    "At least one REQUIRED claim is CONTRADICTED. The development "
                    "rule abstains from automatically resolving consequential contradiction."
                ),
                blocking_claim_ids=tuple(contradicted),
            )

        unresolved = [
            c for c in required
            if c.state in (EvidenceState.PARTIAL, EvidenceState.UNRESOLVED)
        ]
        if not unresolved:
            return StopDecision(
                decision="VERIFICATION_COMPLETE",
                rationale="All REQUIRED claims are SUPPORTED under the current bounded rules.",
            )

        continuable = [c.claim_id for c in unresolved if c.has_adequate_unused_probe]
        if continuable:
            return StopDecision(
                decision="CONTINUE_VERIFICATION",
                rationale=(
                    "At least one REQUIRED unresolved/partial claim has an adequate "
                    "unused verification probe available."
                ),
                blocking_claim_ids=tuple(c.claim_id for c in unresolved),
            )

        return StopDecision(
            decision="HUMAN_REVIEW_REQUIRED",
            rationale=(
                "Required claims remain PARTIAL/UNRESOLVED, but no adequate unused "
                "probe remains. Automated verification abstains."
            ),
            blocking_claim_ids=tuple(c.claim_id for c in unresolved),
        )
