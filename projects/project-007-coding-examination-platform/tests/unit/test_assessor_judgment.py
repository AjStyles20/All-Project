import pytest

from app.domain.enums import EvidenceState
from app.research.assessor_judgment import (
    AssessorJudgment, DimensionJudgment, compare_independent_judgments,
)


def judgment(code="A", case="CASE-PILOT-001", state=EvidenceState.UNRESOLVED):
    return AssessorJudgment(
        code, case, state,
        DimensionJudgment.CANNOT_DETERMINE,
        DimensionJudgment.CANNOT_DETERMINE,
        DimensionJudgment.CANNOT_DETERMINE,
        "Independent rationale.",
        True, None, True, "Independent test-design evidence.", False, None, True,
    )


def test_valid_human_judgment_is_accepted_without_inference():
    j = judgment()
    j.validate()
    assert j.state is EvidenceState.UNRESOLVED


def test_independence_confirmation_is_mandatory():
    j = judgment()
    bad = AssessorJudgment(**{**j.__dict__, "independence_confirmed": False})
    with pytest.raises(ValueError, match="independence"):
        bad.validate()


def test_ambiguity_requires_boundary_description():
    j = judgment()
    bad = AssessorJudgment(**{**j.__dict__, "boundary_confident": False, "ambiguous_boundary": None})
    with pytest.raises(ValueError, match="ambiguous boundary"):
        bad.validate()


def test_comparison_preserves_disagreement_instead_of_reconciling_it():
    a = judgment("A", state=EvidenceState.UNRESOLVED)
    b = judgment("B", state=EvidenceState.PARTIAL)
    result = compare_independent_judgments(a, b)
    assert result.state_agreement is False
    assert result.dimension_agreement_count == 3


def test_same_assessor_cannot_be_used_as_two_independent_assessors():
    with pytest.raises(ValueError, match="distinct assessor"):
        compare_independent_judgments(judgment("A"), judgment("A"))
