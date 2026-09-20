from dataclasses import replace
import pytest
from app.domain.claim_review import IndependentClaimReview, ClaimJudgment
from app.domain.review_lock import lock_review_batch, verify_locked_batch

def r(cid, reviewer="R1", j=ClaimJudgment.SUPPORTED):
    return IndependentClaimReview(cid,reviewer,j,"reason")

def test_review_batch_lock_is_deterministic_and_verifiable():
    a=lock_review_batch("batch-1","R1",(r("BC-2"),r("BC-1")))
    b=lock_review_batch("batch-1","R1",(r("BC-1"),r("BC-2")))
    assert a.lock_digest==b.lock_digest
    assert verify_locked_batch(a)

def test_changed_judgment_breaks_existing_lock():
    a=lock_review_batch("batch-1","R1",(r("BC-1"),))
    changed=replace(a,reviews=(r("BC-1",j=ClaimJudgment.UNSUPPORTED),))
    assert not verify_locked_batch(changed)

def test_rejects_mixed_reviewers_and_duplicates():
    with pytest.raises(ValueError):
        lock_review_batch("b","R1",(r("BC-1","R1"),r("BC-2","R2")))
    with pytest.raises(ValueError):
        lock_review_batch("b","R1",(r("BC-1"),r("BC-1")))
