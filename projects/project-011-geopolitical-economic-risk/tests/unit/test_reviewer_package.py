import pytest
from app.domain.blinded_review import BlindedClaim
from app.domain.claim_review import ClaimJudgment
from app.domain.reviewer_package import ReviewerPackage, ReviewerSubmission, reviewer_package_hash, validate_submission

def pkg():
    return ReviewerPackage("PKG-A-v1","M9-v1","P003-A","P003-A-R2-PKT-v1","a"*64,
        (BlindedClaim("BC-1","Claim one","scenario"),BlindedClaim("BC-2","Claim two","mechanism")),
        "Judge only against supplied evidence.")

def test_package_hash_is_deterministic():
    assert reviewer_package_hash(pkg())==reviewer_package_hash(pkg())
    assert len(reviewer_package_hash(pkg()))==64

def test_submission_requires_exact_frozen_claim_set():
    good=ReviewerSubmission("PKG-A-v1","R1",(("BC-1",ClaimJudgment.SUPPORTED,"evidence"),("BC-2",ClaimJudgment.INDETERMINATE,"insufficient")))
    validate_submission(pkg(),good)
    bad=ReviewerSubmission("PKG-A-v1","R1",(("BC-1",ClaimJudgment.SUPPORTED,"evidence"),))
    with pytest.raises(ValueError): validate_submission(pkg(),bad)

def test_submission_rejects_duplicate_or_blank_rationale():
    dup=ReviewerSubmission("PKG-A-v1","R1",(("BC-1",ClaimJudgment.SUPPORTED,"x"),("BC-1",ClaimJudgment.SUPPORTED,"x")))
    with pytest.raises(ValueError): validate_submission(pkg(),dup)
    blank=ReviewerSubmission("PKG-A-v1","R1",(("BC-1",ClaimJudgment.SUPPORTED,""),("BC-2",ClaimJudgment.SUPPORTED,"x")))
    with pytest.raises(ValueError): validate_submission(pkg(),blank)
