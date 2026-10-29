"""Opt-in FD-04 live MySQL integration test."""
import os
from uuid import uuid4
import pytest

from app.domain.examination import Examination, ExaminationStatus, ProgrammingQuestion
from app.domain.identity import Role
from app.domain.review import MarkingConflictError
from app.persistence.mysql_candidate_session_repository import MySQLCandidateSessionRepository
from app.persistence.mysql_database import MySQLDatabase
from app.persistence.mysql_examination_repository import MySQLExaminationRepository
from app.persistence.mysql_review_repository import MySQLReviewRepository
from app.persistence.mysql_user_repository import MySQLUserRepository
from app.services.auth_service import AuthService
from app.services.candidate_session_service import CandidateSessionService
from app.services.examination_service import ExaminationService
from app.services.review_service import ReviewService

pytestmark = pytest.mark.skipif(
    os.getenv("P001_RUN_MYSQL_TESTS") != "1",
    reason="Set P001_RUN_MYSQL_TESTS=1 to run live MySQL integration tests.",
)


def test_mysql_fd04_review_and_marking():
    database = MySQLDatabase()
    auth = AuthService(MySQLUserRepository(database))
    exam_repo = MySQLExaminationRepository(database)
    session_repo = MySQLCandidateSessionRepository(database)
    review_repo = MySQLReviewRepository(database)
    exams = ExaminationService(exam_repo)
    candidates = CandidateSessionService(session_repo, exam_repo)
    reviews = ReviewService(review_repo, session_repo, exam_repo)

    suffix = uuid4().hex[:10]
    lecturer, student, idle = "fd04-lect-" + suffix, "fd04-cand-" + suffix, "fd04-idle-" + suffix
    auth.create_user(lecturer, "fd04_lecturer_" + suffix, "TemporaryTestPass123!", "FD04 Examiner", {Role.EXAMINER})
    for user in (student, idle):
        auth.create_user(user, user.replace("-", "_"), "TemporaryTestPass123!", "FD04 Candidate", {Role.CANDIDATE})

    exam = Examination("fd04-exam-" + suffix, "FD04 Live Exam", "", lecturer, ExaminationStatus.DRAFT)
    q1 = ProgrammingQuestion("fd04-q1-" + suffix, "Loop Task", "Print 1 to 5.", "python", 10)
    q2 = ProgrammingQuestion("fd04-q2-" + suffix, "List Task", "Squares.", "python", 5)
    exams.create_examination(exam)
    for order, question in enumerate((q1, q2), start=1):
        exams.create_question(question, lecturer)
        exams.attach_question(exam.examination_id, question.question_id, lecturer, order, question.max_score)
    candidates.assign_candidate(exam.examination_id, student, lecturer)
    candidates.assign_candidate(exam.examination_id, idle, lecturer)
    exams.transition(exam.examination_id, lecturer, ExaminationStatus.SCHEDULED)
    exams.transition(exam.examination_id, lecturer, ExaminationStatus.ACTIVE)

    sid = candidates.start_session(exam.examination_id, student).session_id
    candidates.save_response(sid, q1.question_id, student, "print(1)")
    candidates.save_response(sid, q1.question_id, student, "for i in range(1, 6): print(i)")
    open_sid = candidates.start_session(exam.examination_id, idle).session_id

    # In-progress content can still change, so it cannot be marked (service and SQL guard).
    with pytest.raises(MarkingConflictError):
        reviews.mark(sid, q1.question_id, lecturer, 5, "")
    candidates.submit(sid, student)

    first = reviews.mark(sid, q1.question_id, lecturer, 7, "First pass.")
    assert first.response_revision == 2
    reviews.mark(sid, q1.question_id, lecturer, 9, "Re-marked.")
    assert reviews.mark(sid, q2.question_id, lecturer, 0, "Unanswered.").response_revision is None
    # Identical re-mark still counts as saved (CLIENT_FOUND_ROWS + ON DUPLICATE KEY).
    assert review_repo.save_mark(reviews.get_review(sid, lecturer).marks[q2.question_id])

    review = reviews.get_review(sid, lecturer)
    assert review.marks[q1.question_id].score == 9 and len(review.marks) == 2
    summaries = {s.session.session_id: s for s in reviews.list_sessions(exam.examination_id, lecturer)}
    assert (summaries[sid].raw_score, summaries[sid].raw_max, summaries[sid].marked_questions) == (9, 15, 2)
    assert summaries[open_sid].marked_questions == 0

    # Close auto-submits the idle session; it becomes markable. Archive then freezes marks.
    exams.transition(exam.examination_id, lecturer, ExaminationStatus.CLOSED)
    assert reviews.mark(open_sid, q1.question_id, lecturer, 0, "No work saved.").response_revision is None
    exams.transition(exam.examination_id, lecturer, ExaminationStatus.ARCHIVED)
    with pytest.raises(MarkingConflictError):
        reviews.mark(sid, q1.question_id, lecturer, 10, "Too late.")
    assert not review_repo.save_mark(review.marks[q1.question_id])
