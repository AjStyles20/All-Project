from app.domain.claim_review import (
    ClaimJudgment,
    IndependentClaimReview,
    unsupported_downstream_claim_rate,
)


def r(i, judgment):
    return IndependentClaimReview(i, "R1", judgment, "Frozen reviewer rationale.")


def test_udcr_counts_unsupported_and_contradicted_only_in_primary_rule():
    reviews = (
        r("C1", ClaimJudgment.SUPPORTED),
        r("C2", ClaimJudgment.PARTIALLY_SUPPORTED),
        r("C3", ClaimJudgment.UNSUPPORTED),
        r("C4", ClaimJudgment.CONTRADICTED),
    )
    assert unsupported_downstream_claim_rate(reviews) == 0.5


def test_indeterminate_claims_are_excluded_not_silently_reclassified():
    reviews = (
        r("C1", ClaimJudgment.UNSUPPORTED),
        r("C2", ClaimJudgment.INDETERMINATE),
    )
    assert unsupported_downstream_claim_rate(reviews) == 1.0


def test_all_indeterminate_returns_no_rate():
    reviews = (r("C1", ClaimJudgment.INDETERMINATE),)
    assert unsupported_downstream_claim_rate(reviews) is None
