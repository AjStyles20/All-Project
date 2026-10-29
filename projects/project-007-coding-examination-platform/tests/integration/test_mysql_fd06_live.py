"""Opt-in FD-06 live MySQL integration test (research store: temporary SQLite)."""
import json
import os
import sqlite3
from uuid import uuid4
import pytest

from app.domain.enums import ClaimApplicability, EvidenceType
from app.domain.examination import Examination, ExaminationStatus, ProgrammingQuestion
from app.domain.identity import Role
from app.domain.models import CaseClaim, CompetenceClaim, ProgrammingCase
from app.persistence.database import Database
from app.persistence.mysql_candidate_session_repository import MySQLCandidateSessionRepository
from app.persistence.mysql_contract_repository import MySQLContractRepository
from app.persistence.mysql_database import MySQLDatabase
from app.persistence.mysql_examination_repository import MySQLExaminationRepository
from app.persistence.mysql_research_repository import MySQLResearchRepository
from app.persistence.mysql_review_repository import MySQLReviewRepository
from app.persistence.mysql_user_repository import MySQLUserRepository
from app.persistence.repositories import P001Repository
from app.persistence.research_case_store import ResearchCaseStore
from app.services.auth_service import AuthService
from app.services.candidate_session_service import CandidateSessionService
from app.services.examination_service import ExaminationService
from app.services.research_bridge_service import ResearchBridgeService
from tests.contract_helpers import save_lab_contract

pytestmark = pytest.mark.skipif(
    os.getenv("P001_RUN_MYSQL_TESTS") != "1",
    reason="Set P001_RUN_MYSQL_TESTS=1 to run live MySQL integration tests.",
)


def test_mysql_fd06_bridge_with_consent_and_pseudonyms(tmp_path):
    database = MySQLDatabase()
    auth = AuthService(MySQLUserRepository(database))
    exam_repo = MySQLExaminationRepository(database)
    session_repo = MySQLCandidateSessionRepository(database)
    contract_repo = MySQLContractRepository(database)
    research_repo = MySQLResearchRepository(database)
    exams = ExaminationService(exam_repo)
    candidates = CandidateSessionService(session_repo, exam_repo, contract_repository=contract_repo)

    research_db = Database(tmp_path / "research.sqlite3")
    research_db.initialize()
    p001 = P001Repository(research_db)
    p001.add_case(ProgrammingCase("TPL-CC3", "Template: test design", "Write tests.", "python", "1.0"))
    p001.add_claim(CompetenceClaim("CC3", "Test design", "Can design useful tests.", "1.0"))
    p001.add_case_claim(CaseClaim("TPL-CC3", "CC3", ClaimApplicability.REQUIRED))
    bridge = ResearchBridgeService(research_repo, ResearchCaseStore(research_db), exam_repo, session_repo,
                                   MySQLReviewRepository(database), contract_repo)

    suffix = uuid4().hex[:10]
    admin, lecturer = "fd06-admin-" + suffix, "fd06-lect-" + suffix
    yes, no = "fd06-yes-" + suffix, "fd06-no-" + suffix
    auth.create_user(admin, "fd06_admin_" + suffix, "TemporaryTestPass123!", "FD06 Admin", {Role.ADMINISTRATOR})
    auth.create_user(lecturer, "fd06_lect_" + suffix, "TemporaryTestPass123!", "FD06 Examiner", {Role.EXAMINER})
    for user in (yes, no):
        auth.create_user(user, user.replace("-", "_"), "TemporaryTestPass123!", "FD06 Candidate", {Role.CANDIDATE})

    exam = Examination("fd06-exam-" + suffix, "FD06 Live Exam", "", lecturer, ExaminationStatus.DRAFT)
    question = ProgrammingQuestion("fd06-q-" + suffix, "Tests", "Write tests for add().", "python", 10)
    exams.create_examination(exam)
    exams.create_question(question, lecturer)
    exams.attach_question(exam.examination_id, question.question_id, lecturer, 1, 10)
    for user in (yes, no):
        candidates.assign_candidate(exam.examination_id, user, lecturer)
    save_lab_contract(database, exam.examination_id, lecturer)
    exams.transition(exam.examination_id, lecturer, ExaminationStatus.SCHEDULED)
    exams.transition(exam.examination_id, lecturer, ExaminationStatus.ACTIVE)

    link = bridge.create_link(admin, exam.examination_id, question.question_id, "TPL-CC3", ["CC3"], "ETH-LIVE-1")
    assert [l.link_id for l in research_repo.list_links(exam.examination_id)] == [link.link_id]
    bridge.set_consent(exam.examination_id, yes, True)
    bridge.set_consent(exam.examination_id, no, True)
    bridge.set_consent(exam.examination_id, no, False)  # latest event wins

    for user, text in ((yes, "def test_add(): assert add(2, 2) == 4"), (no, "secret answer of the no student")):
        sid = candidates.start_session(exam.examination_id, user).session_id
        candidates.save_response(sid, question.question_id, user, text)
    exams.transition(exam.examination_id, lecturer, ExaminationStatus.CLOSED)

    summary = bridge.run(exam.examination_id)
    assert (summary.bridged, summary.skipped_no_consent) == (1, 1)
    assert bridge.run(exam.examination_id).already_recorded == 1  # idempotent on a real server

    [(who, code)] = research_repo.list_identities(exam.examination_id)
    assert who == yes and code.startswith("R-")
    [record] = research_repo.list_bridge_records(exam.examination_id)
    assert record.research_case_id == f"op-{code}-{question.question_id}" and record.response_revision == 1

    evidence = P001Repository(research_db).get_evidence_for_claim(record.research_case_id, "CC3")
    by_type = {e.evidence_type: e for e in evidence}
    assert by_type[EvidenceType.ARTIFACT].content == "def test_add(): assert add(2, 2) == 4"
    bound = contract_repo.get_bound(exam.examination_id)
    assert by_type[EvidenceType.ARTIFACT].policy_version == bound.policy_version_label() == record.policy_version
    assert json.loads(by_type[EvidenceType.POLICY_CONTEXT].content)["content_hash"] == bound.content_hash

    connection = sqlite3.connect(research_db.path)
    dump = "\n".join(connection.iterdump())
    connection.close()
    for personal in (yes, no, lecturer, admin, "secret answer of the no student"):
        assert personal not in dump
