from app.domain.claim_review import ClaimJudgment
from app.domain.reviewer_agreement import ReviewerResponse, cohens_kappa, raw_agreement


def rr(cid, rid, label):
    return ReviewerResponse(cid, rid, label, "Independent rationale.")


def test_raw_agreement_uses_shared_claim_ids():
    a = (rr("C1","R1",ClaimJudgment.SUPPORTED), rr("C2","R1",ClaimJudgment.UNSUPPORTED))
    b = (rr("C1","R2",ClaimJudgment.SUPPORTED), rr("C2","R2",ClaimJudgment.SUPPORTED))
    assert raw_agreement(a,b) == 0.5


def test_perfect_agreement_has_kappa_one_when_multiple_labels_used():
    a = (rr("C1","R1",ClaimJudgment.SUPPORTED), rr("C2","R1",ClaimJudgment.UNSUPPORTED))
    b = (rr("C1","R2",ClaimJudgment.SUPPORTED), rr("C2","R2",ClaimJudgment.UNSUPPORTED))
    assert cohens_kappa(a,b) == 1.0


def test_no_shared_claims_returns_none():
    a = (rr("C1","R1",ClaimJudgment.SUPPORTED),)
    b = (rr("C2","R2",ClaimJudgment.SUPPORTED),)
    assert raw_agreement(a,b) is None
    assert cohens_kappa(a,b) is None
