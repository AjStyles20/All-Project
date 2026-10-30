from app.domain.enums import ClaimApplicability, EvidenceState
from app.services.gap_detector import GapDetector


def test_unresolved_required_cc3_creates_test_design_gap():
    gap = GapDetector().detect(
        claim_id="CC3",
        applicability=ClaimApplicability.REQUIRED,
        state=EvidenceState.UNRESOLVED,
    )

    assert gap is not None
    assert gap.gap_type == "EG-T3"
    assert gap.claim_id == "CC3"


def test_not_applicable_cc3_never_creates_gap():
    gap = GapDetector().detect(
        claim_id="CC3",
        applicability=ClaimApplicability.NOT_APPLICABLE,
        state=EvidenceState.UNRESOLVED,
    )

    assert gap is None


def test_supported_cc3_does_not_create_gap():
    gap = GapDetector().detect(
        claim_id="CC3",
        applicability=ClaimApplicability.REQUIRED,
        state=EvidenceState.SUPPORTED,
    )

    assert gap is None
