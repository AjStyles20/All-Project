"""Independent claim-review schema; intentionally separate from ETEC progression."""
from dataclasses import dataclass
from enum import Enum


class ClaimJudgment(str, Enum):
    SUPPORTED = "SUPPORTED"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    INDETERMINATE = "INDETERMINATE"


class AbstentionJudgment(str, Enum):
    APPROPRIATE_ABSTENTION = "APPROPRIATE_ABSTENTION"
    OVER_ABSTENTION = "OVER_ABSTENTION"
    INDETERMINATE_ABSTENTION = "INDETERMINATE_ABSTENTION"


@dataclass(frozen=True)
class IndependentClaimReview:
    claim_id: str
    reviewer_id: str
    judgment: ClaimJudgment
    rationale: str


def unsupported_downstream_claim_rate(reviews: tuple[IndependentClaimReview, ...]) -> float | None:
    determinate = [r for r in reviews if r.judgment is not ClaimJudgment.INDETERMINATE]
    if not determinate:
        return None
    errors = [
        r for r in determinate
        if r.judgment in {ClaimJudgment.UNSUPPORTED, ClaimJudgment.CONTRADICTED}
    ]
    return len(errors) / len(determinate)
