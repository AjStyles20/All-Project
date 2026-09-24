"""Opt-in FD-02 live MySQL integration test."""
import os
from uuid import uuid4
import pytest

from app.domain.examination import Examination, ExaminationStatus, ProgrammingQuestion
from app.domain.identity import Role
from app.persistence.mysql_database import MySQLDatabase
from app.persistence.mysql_examination_repository import MySQLExaminationRepository
from app.persistence.mysql_user_repository import MySQLUserRepository
from app.services.auth_service import AuthService
from app.services.examination_service import ExaminationService

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

    service.create_examination(exam)
    service.create_question(question, owner_id)
    service.attach_question(exam.examination_id, question.question_id, owner_id, 1, 10)

    stored = repo.get_examination(exam.examination_id)
    assert stored is not None
    assert stored.owner_user_id == owner_id
    assert stored.status is ExaminationStatus.DRAFT

    scheduled = service.transition(exam.examination_id, owner_id, ExaminationStatus.SCHEDULED)
    assert scheduled.status is ExaminationStatus.SCHEDULED
    assert repo.get_examination(exam.examination_id).status is ExaminationStatus.SCHEDULED
