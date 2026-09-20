from app.domain.enums import ClaimApplicability, EvidenceState
from app.services.stop_rule import ClaimControlInput, StopRule


def claim(claim_id, state, *, applicable=True, unused=False):
    return ClaimControlInput(
        claim_id=claim_id,
        applicability=(ClaimApplicability.REQUIRED if applicable else ClaimApplicability.NOT_APPLICABLE),
        state=state,
        has_adequate_unused_probe=unused,
    )


def test_all_required_supported_completes():
    result = StopRule().decide([
        claim("CC1", EvidenceState.SUPPORTED),
        claim("CC3", EvidenceState.SUPPORTED),
        claim("CC4", EvidenceState.UNRESOLVED, applicable=False),
    ])
    assert result.decision == "VERIFICATION_COMPLETE"


def test_unresolved_with_adequate_unused_probe_continues():
    result = StopRule().decide([
        claim("CC1", EvidenceState.SUPPORTED),
        claim("CC3", EvidenceState.UNRESOLVED, unused=True),
    ])
    assert result.decision == "CONTINUE_VERIFICATION"
    assert result.blocking_claim_ids == ("CC3",)


def test_partial_with_adequate_unused_probe_continues():
    result = StopRule().decide([
        claim("CC3", EvidenceState.PARTIAL, unused=True),
    ])
    assert result.decision == "CONTINUE_VERIFICATION"


def test_unresolved_with_no_adequate_unused_probe_escalates():
    result = StopRule().decide([
        claim("CC3", EvidenceState.UNRESOLVED, unused=False),
    ])
    assert result.decision == "HUMAN_REVIEW_REQUIRED"


def test_partial_with_exhausted_probes_escalates():
    result = StopRule().decide([
        claim("CC3", EvidenceState.PARTIAL, unused=False),
    ])
    assert result.decision == "HUMAN_REVIEW_REQUIRED"


def test_contradicted_required_claim_escalates_even_if_probe_exists():
    result = StopRule().decide([
        claim("CC3", EvidenceState.CONTRADICTED, unused=True),
    ])
    assert result.decision == "HUMAN_REVIEW_REQUIRED"
    assert result.blocking_claim_ids == ("CC3",)


def test_not_applicable_claim_never_blocks_completion():
    result = StopRule().decide([
        claim("CC1", EvidenceState.SUPPORTED),
        claim("CC4", EvidenceState.CONTRADICTED, applicable=False),
    ])
    assert result.decision == "VERIFICATION_COMPLETE"
