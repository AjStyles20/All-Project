"""Gate comparative analysis on complete, immutable reviewer evidence."""
from dataclasses import dataclass
from .review_lock import LockedReviewBatch, verify_locked_batch
from .reviewer_agreement import ReviewerResponse, raw_agreement, cohens_kappa
from .claim_review import IndependentClaimReview, unsupported_downstream_claim_rate


@dataclass(frozen=True)
class ComparativeReviewResult:
    reviewer_ids: tuple[str, str]
    claim_ids: tuple[str, ...]
    raw_agreement: float | None
    cohens_kappa: float | None


def authorize_comparative_review_analysis(
    first: LockedReviewBatch, second: LockedReviewBatch
) -> ComparativeReviewResult:
    if first.reviewer_id == second.reviewer_id:
        raise ValueError("Two distinct reviewer identities are required.")
    if not verify_locked_batch(first) or not verify_locked_batch(second):
        raise ValueError("Every reviewer batch must verify against its pre-unblinding lock.")

    a_ids={r.claim_id for r in first.reviews}
    b_ids={r.claim_id for r in second.reviews}
    if a_ids != b_ids:
        raise ValueError("Reviewer batches must cover exactly the same blinded claim set.")

    def convert(batch):
        return tuple(ReviewerResponse(r.claim_id,r.reviewer_id,r.judgment,r.rationale)
                     for r in batch.reviews)

    a,b=convert(first),convert(second)
    return ComparativeReviewResult(
        reviewer_ids=(first.reviewer_id,second.reviewer_id),
        claim_ids=tuple(sorted(a_ids)),
        raw_agreement=raw_agreement(a,b),
        cohens_kappa=cohens_kappa(a,b),
    )


def pooled_udcr_after_unblinding(reviews: tuple[IndependentClaimReview, ...]) -> float | None:
    """Metric helper only; caller must supply legitimately unblinded downstream claims."""
    return unsupported_downstream_claim_rate(reviews)
