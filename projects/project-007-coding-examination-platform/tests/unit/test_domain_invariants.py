from app.domain.enums import ClaimApplicability, EvidenceState
from app.domain.invariants import claim_may_generate_gap, claim_requires_evaluation


def test_required_claim_requires_evaluation():
    assert claim_requires_evaluation(ClaimApplicability.REQUIRED)


def test_not_applicable_claim_does_not_require_evaluation():
    assert not claim_requires_evaluation(ClaimApplicability.NOT_APPLICABLE)


def test_not_applicable_claim_does_not_generate_gap():
    assert not claim_may_generate_gap(ClaimApplicability.NOT_APPLICABLE)


def test_authoritative_evidence_states_are_preserved():
    assert {state.value for state in EvidenceState} == {
        "SUPPORTED",
        "PARTIAL",
        "UNRESOLVED",
        "CONTRADICTED",
    }
