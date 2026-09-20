import pytest

from app.services.verification_burden import BurdenComparison, VerificationBurden


def test_burden_keeps_count_time_and_complexity_separate():
    burden = VerificationBurden(
        question_count=2, verification_seconds=95.5,
        complexity=("LOW", "MEDIUM"),
    )
    assert burden.question_count == 2
    assert burden.verification_seconds == 95.5
    assert burden.complexity == ("LOW", "MEDIUM")


def test_burden_rejects_inconsistent_question_complexity_count():
    with pytest.raises(ValueError, match="one entry per"):
        VerificationBurden(2, 30.0, ("LOW",))


def test_burden_rejects_negative_measurements():
    with pytest.raises(ValueError):
        VerificationBurden(-1, 0.0, ())
    with pytest.raises(ValueError):
        VerificationBurden(0, -0.1, ())


def test_comparison_reports_raw_differences_not_composite_score():
    comparison = BurdenComparison(
        b2=VerificationBurden(4, 240.0, ("MEDIUM",) * 4),
        b4=VerificationBurden(1, 70.0, ("MEDIUM",)),
    )
    assert comparison.question_difference == 3
    assert comparison.time_difference_seconds == 170.0
    assert not hasattr(comparison, "score")
