from dataclasses import replace
import pytest
from app.domain.claim_review import IndependentClaimReview, ClaimJudgment
from app.domain.review_lock import lock_review_batch
from app.domain.analysis_gate import authorize_comparative_review_analysis

def batch(reviewer, judgments):
    rs=tuple(IndependentClaimReview(cid,reviewer,j,"r") for cid,j in judgments)
    return lock_review_batch("blind-batch-v1",reviewer,rs)

def test_gate_accepts_two_locked_reviewers_with_same_claim_set():
    a=batch("R1",(("BC-1",ClaimJudgment.SUPPORTED),("BC-2",ClaimJudgment.UNSUPPORTED)))
    b=batch("R2",(("BC-1",ClaimJudgment.SUPPORTED),("BC-2",ClaimJudgment.PARTIALLY_SUPPORTED)))
    out=authorize_comparative_review_analysis(a,b)
    assert out.claim_ids==("BC-1","BC-2")
    assert out.raw_agreement==0.5

def test_gate_rejects_same_reviewer_or_incomplete_claim_set():
    a=batch("R1",(("BC-1",ClaimJudgment.SUPPORTED),))
    with pytest.raises(ValueError):
        authorize_comparative_review_analysis(a,a)
    b=batch("R2",(("BC-2",ClaimJudgment.SUPPORTED),))
    with pytest.raises(ValueError):
        authorize_comparative_review_analysis(a,b)

def test_gate_rejects_tampered_locked_batch():
    a=batch("R1",(("BC-1",ClaimJudgment.SUPPORTED),))
    b=batch("R2",(("BC-1",ClaimJudgment.SUPPORTED),))
    tampered=replace(b,reviews=(IndependentClaimReview("BC-1","R2",ClaimJudgment.UNSUPPORTED,"changed"),))
    with pytest.raises(ValueError):
        authorize_comparative_review_analysis(a,tampered)
