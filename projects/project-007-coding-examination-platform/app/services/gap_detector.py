"""Evidence-gap detection for the P001 research prototype."""
from dataclasses import dataclass

from app.domain.enums import ClaimApplicability, EvidenceState


@dataclass(frozen=True)
class EvidenceGapCandidate:
    gap_type: str
    claim_id: str
    description: str


class GapDetector:
    """Map bounded unresolved claim states to explicit evidence gaps."""

    def detect(
        self,
        claim_id: str,
        applicability: ClaimApplicability,
        state: EvidenceState,
    ) -> EvidenceGapCandidate | None:
        if applicability is ClaimApplicability.NOT_APPLICABLE:
            return None

        if state is EvidenceState.SUPPORTED:
            return None

        if claim_id == "CC3" and state is EvidenceState.UNRESOLVED:
            return EvidenceGapCandidate(
                gap_type="EG-T3",
                claim_id="CC3",
                description=(
                    "Missing independent test-design evidence: the candidate has not "
                    "yet demonstrated a relevant unsupplied test, its expected result, "
                    "and why the test is useful."
                ),
            )

        return None
