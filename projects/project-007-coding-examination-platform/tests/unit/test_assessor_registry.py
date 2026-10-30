import pytest

from app.domain.enums import EvidenceState
from app.research.assessor_judgment import AssessorJudgment, DimensionJudgment
from app.research.assessor_registry import AssessorJudgmentRegistry


def record(code, state=EvidenceState.UNRESOLVED):
    return AssessorJudgment(
        code, "CASE-PILOT-001", state,
        DimensionJudgment.CANNOT_DETERMINE,
        DimensionJudgment.CANNOT_DETERMINE,
        DimensionJudgment.CANNOT_DETERMINE,
        "Rationale from assessor.", True, None,
        False, None, False, None, True,
    )


def test_registry_preserves_two_independent_records_and_disagreement():
    registry = AssessorJudgmentRegistry()
    registry.add(record("ASSESSOR-A"))
    registry.add(record("ASSESSOR-B", EvidenceState.PARTIAL))
    summary = registry.summarize_two_assessor_case("CASE-PILOT-001")
    assert len(summary.judgments) == 2
    assert summary.comparison is not None
    assert summary.comparison.state_agreement is False


def test_original_judgment_cannot_be_silently_overwritten():
    registry = AssessorJudgmentRegistry()
    registry.add(record("ASSESSOR-A"))
    with pytest.raises(ValueError, match="preserve original"):
        registry.add(record("ASSESSOR-A", EvidenceState.PARTIAL))


def test_one_assessor_does_not_create_fake_comparison():
    registry = AssessorJudgmentRegistry()
    registry.add(record("ASSESSOR-A"))
    summary = registry.summarize_two_assessor_case("CASE-PILOT-001")
    assert summary.comparison is None
