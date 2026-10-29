"""Opt-in FD-05 live MySQL integration test (ECC v1.0)."""
import os
from datetime import timedelta
from uuid import uuid4
import pytest

from app.domain.capability_contract import (
    ContractRequiredError, ContractStatus, ExceptionReason,
)
from app.domain.examination import (
    Examination, ExaminationConflictError, ExaminationStatus, ProgrammingQuestion,
)
from app.domain.identity import Role
from app.persistence.mysql_candidate_session_repository import MySQLCandidateSessionRepository
from app.persistence.mysql_contract_repository import MySQLContractRepository
from app.persistence.mysql_database import MySQLDatabase
from app.persistence.mysql_examination_repository import MySQLExaminationRepository
from app.persistence.mysql_user_repository import MySQLUserRepository
from app.services.auth_service import AuthService
from app.services.candidate_session_service import CandidateSessionService
from app.services.contract_service import ContractDeclaration, ContractService
from app.services.examination_service import ExaminationService
from tests.contract_helpers import LAB_CAPABILITIES

pytestmark = pytest.mark.skipif(
    os.getenv("P001_RUN_MYSQL_TESTS") != "1",
    reason="Set P001_RUN_MYSQL_TESTS=1 to run live MySQL integration tests.",
)


def test_mysql_fd05_contract_binding_amendment_and_exceptions():
    database = MySQLDatabase()
    auth = AuthService(MySQLUserRepository(database))
    exam_repo = MySQLExaminationRepository(database)
    contract_repo = MySQLContractRepository(database)
    session_repo = MySQLCandidateSessionRepository(database)
    exams = ExaminationService(exam_repo)
    contracts = ContractService(contract_repo, exam_repo, session_repo)
    candidates = CandidateSessionService(session_repo, exam_repo)

    suffix = uuid4().hex[:10]
    lecturer, student = "fd05-lect-" + suffix, "fd05-cand-" + suffix
    auth.create_user(lecturer, "fd05_lecturer_" + suffix, "TemporaryTestPass123!", "FD05 Examiner", {Role.EXAMINER})
    auth.create_user(student, "fd05_candidate_" + suffix, "TemporaryTestPass123!", "FD05 Candidate", {Role.CANDIDATE})
    exam = Examination("fd05-exam-" + suffix, "FD05 Live Exam", "", lecturer, ExaminationStatus.DRAFT)
    question = ProgrammingQuestion("fd05-q-" + suffix, "Loop Task", "Print 1 to 5.", "python", 10)
    exams.create_examination(exam)
    exams.create_question(question, lecturer)
    exams.attach_question(exam.examination_id, question.question_id, lecturer, 1, 10)
    candidates.assign_candidate(exam.examination_id, student, lecturer)

    # No contract: the service refuses, and the SQL backstop rolls the status back.
    with pytest.raises(ContractRequiredError):
        exams.transition(exam.examination_id, lecturer, ExaminationStatus.SCHEDULED)
    with pytest.raises(ContractRequiredError):
        exam_repo.update_status(exam.examination_id, ExaminationStatus.SCHEDULED, expected=ExaminationStatus.DRAFT)
    assert exam_repo.get_examination(exam.examination_id).status is ExaminationStatus.DRAFT

    first = contracts.save_draft(exam.examination_id, lecturer, ContractDeclaration(dict(LAB_CAPABILITIES)))
    edited = contracts.save_draft(exam.examination_id, lecturer,
                                  ContractDeclaration({**LAB_CAPABILITIES, "debugger": "DENY"}))
    # Re-saving identical content still counts as found (CLIENT_FOUND_ROWS).
    assert contracts.save_draft(exam.examination_id, lecturer,
                                ContractDeclaration({**LAB_CAPABILITIES, "debugger": "DENY"})).version == 1
    assert edited.version == first.version == 1

    exams.transition(exam.examination_id, lecturer, ExaminationStatus.SCHEDULED)
    bound = contract_repo.get_bound(exam.examination_id)
    assert bound.status is ContractStatus.BOUND and bound.bound_at is not None
    # The JSON document survives MySQL storage: the recomputed hash matches the stored one.
    assert bound.compute_hash() == bound.content_hash == edited.content_hash
    with pytest.raises(ExaminationConflictError):
        contracts.save_draft(exam.examination_id, lecturer, ContractDeclaration(dict(LAB_CAPABILITIES)))

    granted = contracts.grant_exception(exam.examination_id, lecturer, student, ExceptionReason.ACCESSIBILITY,
                                        {"external_ide": "ALLOW"}, 30)
    view = contracts.candidate_view(exam.examination_id, student)
    assert view.contract.version == 1
    assert [(e.exception_id, e.capability_overrides, e.extra_time_minutes) for e in view.exceptions] == \
        [(granted.exception_id, {"external_ide": "ALLOW"}, 30)]

    contracts.clock = lambda: bound.bound_at + timedelta(minutes=10)
    v2 = contracts.amend(exam.examination_id, lecturer,
                         ContractDeclaration({**LAB_CAPABILITIES, "internet": "ALLOW"}), "Docs mirror down")
    versions = contract_repo.list_versions(exam.examination_id)
    assert [(c.version, c.status) for c in versions] == [(1, ContractStatus.SUPERSEDED), (2, ContractStatus.BOUND)]
    assert versions[0].content_hash == bound.content_hash  # v1 never rewritten
    assert contracts.in_force_at(exam.examination_id, bound.bound_at + timedelta(minutes=5)).version == 1
    assert contracts.in_force_at(exam.examination_id, v2.bound_at + timedelta(minutes=1)).version == 2
