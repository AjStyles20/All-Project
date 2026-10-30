"""Locked reviewer-batch primitives.

A lock digest makes the exact set of reviewer judgments immutable-by-reference
before unblinding and comparative scoring.
"""
from dataclasses import dataclass
from hashlib import sha256
import json
from .claim_review import IndependentClaimReview


@dataclass(frozen=True)
class LockedReviewBatch:
    batch_id: str
    reviewer_id: str
    reviews: tuple[IndependentClaimReview, ...]
    lock_digest: str


def _payload(batch_id: str, reviewer_id: str, reviews: tuple[IndependentClaimReview, ...]) -> str:
    rows = [{
        "claim_id": r.claim_id,
        "reviewer_id": r.reviewer_id,
        "judgment": r.judgment.value,
        "rationale": r.rationale,
    } for r in sorted(reviews, key=lambda x: x.claim_id)]
    return json.dumps({"batch_id":batch_id,"reviewer_id":reviewer_id,"reviews":rows},
                      sort_keys=True,separators=(",",":"),ensure_ascii=False)


def lock_review_batch(batch_id: str, reviewer_id: str,
                      reviews: tuple[IndependentClaimReview, ...]) -> LockedReviewBatch:
    if not batch_id.strip() or not reviewer_id.strip() or not reviews:
        raise ValueError("batch_id, reviewer_id and at least one review are required")
    if any(r.reviewer_id != reviewer_id for r in reviews):
        raise ValueError("Every review must belong to the declared reviewer")
    ids=[r.claim_id for r in reviews]
    if len(ids)!=len(set(ids)):
        raise ValueError("Duplicate claim review in batch")
    digest=sha256(_payload(batch_id,reviewer_id,reviews).encode("utf-8")).hexdigest()
    return LockedReviewBatch(batch_id,reviewer_id,reviews,digest)


def verify_locked_batch(batch: LockedReviewBatch) -> bool:
    expected=sha256(_payload(batch.batch_id,batch.reviewer_id,batch.reviews).encode("utf-8")).hexdigest()
    return expected==batch.lock_digest
