"""Opt-in FD-02 live MySQL integration test."""
import os
from uuid import uuid4
import pytest

from app.domain.examination import (
    Examination, ExaminationConflictError, ExaminationStatus, ProgrammingQuestion,
)
from app.domain.identity import Role
from app.persistence.mysql_database import MySQLDatabase
from app.persistence.mysql_examination_repository import MySQLExaminationRepository
from app.persistence.mysql_user_repository import MySQLUserRepository
from app.services.auth_service import AuthService
from app.services.examination_service import (
    ExaminationService, InvalidExaminationTransition, QuestionNotFoundError,
)

from tests.contract_helpers import save_lab_contract

pytestmark = pytest.mark.skipif(
    os.getenv("P001_RUN_MYSQL_TESTS") != "1",
    reason="Set P001_RUN_MYSQL_TESTS=1 to run live MySQL integration tests.",
)

def test_mysql_fd02_exam_question_lifecycle():
    database = MySQLDatabase()
    users = MySQLUserRepository(database)
    auth = AuthService(users)
    repo = MySQLExaminationRepository(database)
    service = ExaminationService(repo)

    suffix = uuid4().hex[:10]
    owner_id = "fd02-owner-" + suffix
    auth.create_user(owner_id, "fd02_examiner_" + suffix, "TemporaryTestPass123!",
                     "FD02 MySQL Examiner", {Role.EXAMINER})

    exam = Examination("fd02-exam-" + suffix, "FD02 Live Integration Exam", "",
                       owner_id, ExaminationStatus.DRAFT)
    question = ProgrammingQuestion("fd02-q-" + suffix, "Loop Task",
                                   "Write a loop that prints 1 to 5.", "python", 10)
    spare = ProgrammingQuestion("fd02-q2-" + suffix, "List Task",
                                "Build a list of squares.", "python", 5)

    service.create_examination(exam)
    service.create_question(question, owner_id)
    service.create_question(spare, owner_id)

    # Scheduling an empty examination is refused before any membership exists.
    with pytest.raises(InvalidExaminationTransition):
        service.transition(exam.examination_id, owner_id, ExaminationStatus.SCHEDULED)

    service.attach_question(exam.examination_id, question.question_id, owner_id, 1, 10)
    service.attach_question(exam.examination_id, spare.question_id, owner_id, 2, 5)

    # DR-011: another examiner's question cannot be attached, even by a valid owner.
    other_id = "fd02-other-" + suffix
    auth.create_user(other_id, "fd02_other_" + suffix, "TemporaryTestPass123!",
                     "FD02 Other Examiner", {Role.EXAMINER})
    foreign = ProgrammingQuestion("fd02-qx-" + suffix, "Foreign", "Not yours.", "python", 3)
    service.create_question(foreign, other_id)
    assert repo.question_created_by(foreign.question_id) == other_id
    with pytest.raises(QuestionNotFoundError):
        service.attach_question(exam.examination_id, foreign.question_id, owner_id, 3, 3)

    # The unique (examination, question) key is translated into a domain conflict.
    with pytest.raises(ExaminationConflictError):
        repo.attach_question(exam.examination_id, question.question_id, 3, 10)

    service.detach_question(exam.examination_id, spare.question_id, owner_id)
    entries = service.list_examination_questions(exam.examination_id, owner_id)
    assert [(e.question.question_id, e.display_order) for e in entries] == [(question.question_id, 1)]

    service.update_details(exam.examination_id, owner_id, title="FD02 Live Exam (renamed)",
                           description="Updated in DRAFT", starts_at=None, ends_at=None)

    stored = repo.get_examination(exam.examination_id)
    assert stored is not None
    assert stored.owner_user_id == owner_id
    assert stored.status is ExaminationStatus.DRAFT
    assert stored.title == "FD02 Live Exam (renamed)"
    assert exam.examination_id in [e.examination_id for e in service.list_examinations(owner_id)]
    assert {q.question_id for q in service.list_questions(owner_id)} == {question.question_id, spare.question_id}
    # Re-saving identical values still counts as found (FOUND_ROWS client flag).
    assert repo.update_details(stored)

    save_lab_contract(database, exam.examination_id, owner_id)
    scheduled = service.transition(exam.examination_id, owner_id, ExaminationStatus.SCHEDULED)
    assert scheduled.status is ExaminationStatus.SCHEDULED
    assert repo.get_examination(exam.examination_id).status is ExaminationStatus.SCHEDULED

    # Status predicates in SQL: a stale expected status and post-DRAFT edits change nothing.
    assert not repo.update_status(exam.examination_id, ExaminationStatus.SCHEDULED,
                                  expected=ExaminationStatus.DRAFT)
    assert not repo.update_details(stored)
    with pytest.raises(ExaminationConflictError):
        repo.attach_question(exam.examination_id, spare.question_id, 2, 5)
    assert not repo.detach_question(exam.examination_id, question.question_id)
