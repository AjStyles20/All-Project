"""Domain invariants for the P001 research prototype."""
from .enums import ClaimApplicability


def claim_requires_evaluation(applicability: ClaimApplicability) -> bool:
    """Only REQUIRED claims participate in evidence-gap evaluation."""
    return applicability is ClaimApplicability.REQUIRED


def claim_may_generate_gap(applicability: ClaimApplicability) -> bool:
    """NOT_APPLICABLE claims must never generate an evidence gap."""
    return claim_requires_evaluation(applicability)
