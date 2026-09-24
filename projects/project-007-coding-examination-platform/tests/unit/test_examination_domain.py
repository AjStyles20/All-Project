from datetime import datetime, timezone
import pytest

from app.domain.examination import Examination, ExaminationStatus, ProgrammingQuestion


def test_examination_rejects_invalid_time_window():
    exam = Examination(
        "e1", "Python Exam", "", "lecturer-1", ExaminationStatus.DRAFT,
        datetime(2026, 9, 24, 12, tzinfo=timezone.utc),
        datetime(2026, 9, 24, 11, tzinfo=timezone.utc),
    )
    with pytest.raises(ValueError):
        exam.validate()


def test_programming_question_requires_positive_score_and_version():
    with pytest.raises(ValueError):
        ProgrammingQuestion("q1", "Loops", "Write code", "python", 0).validate()
    with pytest.raises(ValueError):
        ProgrammingQuestion("q2", "Loops", "Write code", "python", 10, 0).validate()


def test_valid_exam_and_question():
    Examination("e1", "Python Exam", "", "lecturer-1", ExaminationStatus.DRAFT).validate()
    ProgrammingQuestion("q1", "Loops", "Write a loop", "python", 10).validate()
