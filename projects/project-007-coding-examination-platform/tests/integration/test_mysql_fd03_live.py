"""Opt-in FD-03 live MySQL integration test."""
import os
from uuid import uuid4
import pytest

from app.domain.candidate_session import SessionConflictError, SessionStatus, SubmissionMode
from app.domain.examination import Examination, ExaminationStatus, ProgrammingQuestion
from app.domain.identity import Role
from app.persistence.mysql_candidate_session_repository import MySQLCandidateSessionRepository
from app.persistence.mysql_database import MySQLDatabase
from app.persistence.mysql_examination_repository import MySQLExaminationRepository
from app.persistence.mysql_user_repository import MySQLUserRepository
from app.services.auth_service import AuthService
from app.services.candidate_session_service import CandidateNotFoundError, CandidateSessionService
from app.services.examination_service import ExaminationService

from tests.contract_helpers import save_lab_contract

pytestmark = pytest.mark.skipif(
    os.getenv("P001_RUN_MYSQL_TESTS") != "1",
    reason="Set P001_RUN_MYSQL_TESTS=1 to run live MySQL integration tests.",
)


def test_mysql_fd03_assignment_session_save_submit():
    database = MySQLDatabase()
    auth = AuthService(MySQLUserRepository(database))
    exam_repo = MySQLExaminationRepository(database)
    session_repo = MySQLCandidateSessionRepository(database)
    exams = ExaminationService(exam_repo)
    sessions = CandidateSessionService(session_repo, exam_repo)

    suffix = uuid4().hex[:10]
    lecturer, student = "fd03-lect-" + suffix, "fd03-cand-" + suffix
    auth.create_user(lecturer, "fd03_lecturer_" + suffix, "TemporaryTestPass123!", "FD03 Examiner", {Role.EXAMINER})
    auth.create_user(student, "fd03_candidate_" + suffix, "TemporaryTestPass123!", "FD03 Candidate", {Role.CANDIDATE})

    exam = Examination("fd03-exam-" + suffix, "FD03 Live Exam", "", lecturer, ExaminationStatus.DRAFT)
    question = ProgrammingQuestion("fd03-q-" + suffix, "Loop Task", "Print 1 to 5.", "python", 10)
    exams.create_examination(exam)
    exams.create_question(question, lecturer)
    exams.attach_question(exam.examination_id, question.question_id, lecturer, 1, 10)

    # Only users holding the CANDIDATE role can be assigned.
    with pytest.raises(CandidateNotFoundError):
        sessions.assign_candidate(exam.examination_id, lecturer, lecturer)
    sessions.assign_candidate(exam.examination_id, student, lecturer)
    with pytest.raises(SessionConflictError):
        session_repo.create_assignment(sessions.list_assignments(exam.examination_id, lecturer)[0])

    save_lab_contract(database, exam.examination_id, lecturer)
    exams.transition(exam.examination_id, lecturer, ExaminationStatus.SCHEDULED)
    exams.transition(exam.examination_id, lecturer, ExaminationStatus.ACTIVE)

    started = sessions.start_session(exam.examination_id, student)
    assert sessions.start_session(exam.examination_id, student).session_id == started.session_id

    first = sessions.save_response(started.session_id, question.question_id, student, "print(1)")
    second = sessions.save_response(started.session_id, question.question_id, student,
                                    "for i in range(1, 6): print(i)", base_revision=first.revision)
    assert second.revision == 2
    # Stale revision is rejected by the SQL compare-and-set, not only by the service.
    assert not session_repo.save_response(second, previous_revision=1)

    submitted = sessions.submit(started.session_id, student)
    assert submitted.status is SessionStatus.SUBMITTED and submitted.submitted_at is not None
    assert sessions.submit(started.session_id, student).submitted_at == submitted.submitted_at
    assert not session_repo.save_response(second, previous_revision=2)

    view = sessions.get_session_view(started.session_id, student)
    assert view.responses[question.question_id].content == "for i in range(1, 6): print(i)"
    assert submitted.submission_mode is SubmissionMode.CANDIDATE

    # DR-011 (6): closing the examination auto-submits a session still in progress.
    late = "fd03-cand2-" + suffix
    auth.create_user(late, "fd03_candidate2_" + suffix, "TemporaryTestPass123!", "FD03 Candidate 2", {Role.CANDIDATE})
    sessions.assign_candidate(exam.examination_id, late, lecturer)
    open_session = sessions.start_session(exam.examination_id, late)
    sessions.save_response(open_session.session_id, question.question_id, late, "unsubmitted work")

    exams.transition(exam.examination_id, lecturer, ExaminationStatus.CLOSED)

    auto = session_repo.get_session(open_session.session_id)
    assert auto.status is SessionStatus.SUBMITTED and auto.submission_mode is SubmissionMode.AUTO_ON_CLOSE
    assert auto.submitted_at is not None
    unchanged = session_repo.get_session(started.session_id)
    assert unchanged.submission_mode is SubmissionMode.CANDIDATE and unchanged.submitted_at == submitted.submitted_at
    assert sessions.get_session_view(open_session.session_id, late).responses[question.question_id].content == "unsubmitted work"
