import json
import sqlite3
from dataclasses import replace
from datetime import datetime, timedelta

import pytest

from app.domain.capability_contract import ExceptionReason
from app.domain.enums import ClaimApplicability, EvidenceType
from app.domain.examination import (
    Examination, ExaminationConflictError, ExaminationStatus, ProgrammingQuestion,
)
from app.domain.models import CaseClaim, CompetenceClaim, ProgrammingCase
from app.domain.research_bridge import (
    BridgeOutcome, ConsentStatus, ResearchBridgeError, ResearchStoreNotConfigured,
)
from app.persistence.database import Database
from app.persistence.repositories import P001Repository
from app.persistence.research_case_store import ResearchCaseStore
from app.services.candidate_session_service import AssignmentNotFoundError, CandidateSessionService
from app.services.contract_service import ContractDeclaration, ContractService
from app.services.examination_service import ExaminationService, QuestionNotFoundError
from app.services.research_bridge_service import ResearchBridgeService
from tests.candidate_session_fakes import InMemoryCandidateSessionRepository
from tests.contract_fakes import InMemoryContractRepository
from tests.contract_helpers import LAB_CAPABILITIES
from tests.examination_fakes import InMemoryExaminationRepository
from tests.research_fakes import InMemoryResearchRepository
from tests.review_fakes import InMemoryReviewRepository


def research_store(tmp_path):
    database = Database(tmp_path / "research.sqlite3")
    database.initialize()
    repo = P001Repository(database)
    repo.add_case(ProgrammingCase("TPL-CC3", "Template: test design", "Write tests for a function.", "python", "1.0"))
    repo.add_claim(CompetenceClaim("CC3", "Test design", "Can design useful tests.", "1.0"))
    repo.add_claim(CompetenceClaim("CC1", "Other", "Not applicable here.", "1.0"))
    repo.add_case_claim(CaseClaim("TPL-CC3", "CC3", ClaimApplicability.REQUIRED))
    repo.add_case_claim(CaseClaim("TPL-CC3", "CC1", ClaimApplicability.NOT_APPLICABLE))
    return database, ResearchCaseStore(database)


class World:
    """A closed exam with two submitted sessions, ready for bridging."""

    def __init__(self, tmp_path, configured=True):
        self.now = datetime(2026, 11, 4, 9, 0)
        clock = lambda: self.now
        self.exam_repo = InMemoryExaminationRepository()
        self.contract_repo = InMemoryContractRepository(self.exam_repo)
        self.session_repo = InMemoryCandidateSessionRepository({"student-1", "student-2"})
        self.exam_repo.on_close.append(self.session_repo.finalize_open_sessions)
        self.research_repo = InMemoryResearchRepository()
        self.db, store = research_store(tmp_path)
        self.exams = ExaminationService(self.exam_repo)
        self.contracts = ContractService(self.contract_repo, self.exam_repo, self.session_repo, clock)
        self.candidates = CandidateSessionService(self.session_repo, self.exam_repo, clock, self.contract_repo)
        self.bridge = ResearchBridgeService(
            self.research_repo, store if configured else None, self.exam_repo, self.session_repo,
            InMemoryReviewRepository(self.session_repo, self.exam_repo), self.contract_repo, clock)

        self.exam_repo.create_examination(Examination("e1", "Exam", "", "lecturer-1", ExaminationStatus.DRAFT))
        for qid in ("q1", "q2"):
            self.exam_repo.create_question(ProgrammingQuestion(qid, qid, "Write tests", "python", 10), "lecturer-1")
        self.exam_repo.attachments += [("e1", "q1", 1, 10), ("e1", "q2", 2, 10)]
        for student in ("student-1", "student-2"):
            self.candidates.assign_candidate("e1", student, "lecturer-1")
        self.contracts.save_draft("e1", "lecturer-1", ContractDeclaration(dict(LAB_CAPABILITIES)))
        self.exams.transition("e1", "lecturer-1", ExaminationStatus.SCHEDULED)
        # Binding stamps real wall-clock time; pin it before the test clock for in_force_at.
        bound = self.contract_repo.get_bound("e1")
        self.contract_repo.versions[("e1", bound.version)] = replace(bound, bound_at=self.now - timedelta(hours=1))
        self.exams.transition("e1", "lecturer-1", ExaminationStatus.ACTIVE)
        self.s1 = self.candidates.start_session("e1", "student-1").session_id
        self.s2 = self.candidates.start_session("e1", "student-2").session_id
        self.candidates.save_response(self.s1, "q1", "student-1", "def test_add(): assert add(1, 2) == 3")
        self.candidates.save_response(self.s2, "q1", "student-2", "student two answer")

    def link(self, question="q1", claims=("CC3",), ethics="ETH-2026-041"):
        return self.bridge.create_link("admin-1", "e1", question, "TPL-CC3", list(claims), ethics)

    def close(self):
        self.exams.transition("e1", "lecturer-1", ExaminationStatus.CLOSED)

    def research_text(self) -> str:
        """Every value in the research store, to prove no personal identifiers leaked."""
        connection = sqlite3.connect(self.db.path)
        dump = "\n".join(connection.iterdump())
        connection.close()
        return dump


def test_link_validation(tmp_path):
    world = World(tmp_path)
    with pytest.raises(ValueError, match="ethics"):
        world.link(ethics="  ")
    with pytest.raises(ResearchBridgeError, match="REQUIRED"):
        world.link(claims=("CC1",))  # NOT_APPLICABLE on the template
    with pytest.raises(QuestionNotFoundError):
        world.link(question="not-in-exam")
    with pytest.raises(ResearchBridgeError, match="Template"):
        world.bridge.create_link("admin-1", "e1", "q1", "NO-SUCH-CASE", ["CC3"], "ETH-1")
    world.link()
    with pytest.raises(ExaminationConflictError):
        world.link()  # one link per exam question


def test_not_configured_store_refuses(tmp_path):
    world = World(tmp_path, configured=False)
    with pytest.raises(ResearchStoreNotConfigured):
        world.link()
    world.close()
    with pytest.raises(ResearchStoreNotConfigured):
        world.bridge.run("e1")


def test_consent_requires_assignment_and_a_linked_study(tmp_path):
    world = World(tmp_path)
    with pytest.raises(ExaminationConflictError, match="No research study"):
        world.bridge.set_consent("e1", "student-1", True)
    world.link()
    with pytest.raises(AssignmentNotFoundError):
        world.bridge.set_consent("e1", "stranger", True)
    assert world.bridge.set_consent("e1", "student-1", True) is ConsentStatus.OPTED_IN
    assert world.bridge.consent_info("e1", "student-1").status is ConsentStatus.OPTED_IN
    assert world.bridge.consent_info("e1", "student-2").status is None


def test_bridge_copies_only_consenting_closed_work_with_provenance(tmp_path):
    world = World(tmp_path)
    world.link("q1")
    world.link("q2")  # q2 is unanswered by everyone
    world.bridge.set_consent("e1", "student-1", True)  # student-2 never opts in
    world.now += timedelta(minutes=5)  # the exception comes after the answer was saved
    world.contracts.grant_exception("e1", "lecturer-1", "student-1", ExceptionReason.ACCESSIBILITY,
                                    {"external_ide": "ALLOW"}, 15)
    with pytest.raises(ResearchBridgeError, match="CLOSED"):
        world.bridge.run("e1")
    world.close()

    summary = world.bridge.run("e1")
    assert (summary.bridged, summary.no_response, summary.skipped_no_consent) == (1, 1, 1)
    code = world.research_repo.get_research_code("e1", "student-1")
    assert code.startswith("R-") and world.research_repo.get_research_code("e1", "student-2") is None
    [case_id] = summary.research_case_ids
    assert case_id == f"op-{code}-q1"

    store = ResearchCaseStore(world.db)
    assert store.get_case(case_id).title == "Template: test design"
    assert [(c.claim_id, c.applicability) for c in store.get_case_claims(case_id)] == \
        [("CC1", ClaimApplicability.NOT_APPLICABLE), ("CC3", ClaimApplicability.REQUIRED)]
    evidence = P001Repository(world.db).get_evidence_for_claim(case_id, "CC3")
    by_type = {e.evidence_type: e for e in evidence}
    artifact, policy = by_type[EvidenceType.ARTIFACT], by_type[EvidenceType.POLICY_CONTEXT]
    assert artifact.content == "def test_add(): assert add(1, 2) == 3"
    assert artifact.policy_version == policy.policy_version and artifact.policy_version.startswith("ecc:e1@v1#")
    context = json.loads(artifact.assistance_context)
    assert context["capabilities"]["ai_assistance"] == "DENY"
    assert context["assistance_construct"] == {"CC3": "INDEPENDENT"}
    # The exception was granted after the answer was saved, so it does not apply (spec §5.4).
    assert context["exceptions"] == []
    # POLICY_CONTEXT carries the bound contract (DR-013 Q3) minus the examiner's identity,
    # with the full hash so it stays verifiable against the operational record.
    bound = world.contract_repo.get_bound("e1")
    policy_doc = json.loads(policy.content)
    assert policy_doc["content_hash"] == bound.content_hash
    assert policy_doc["redacted_fields"] == ["bound_by_user_id"]
    expected = {k: v for k, v in bound.hashed_document().items() if k != "bound_by_user_id"}
    assert policy_doc["contract"] == expected

    # No personal identifier reaches the research store (DR-015 (2)).
    dump = world.research_text()
    for secret in ("student-1", "student-2", "student two answer", "lecturer-1"):
        assert secret not in dump


def test_rerun_is_idempotent_and_withdrawal_stops_future_copying(tmp_path):
    world = World(tmp_path)
    world.link()
    world.bridge.set_consent("e1", "student-1", True)
    world.bridge.set_consent("e1", "student-2", True)
    world.bridge.set_consent("e1", "student-2", False)  # withdrew before the run
    world.close()
    first = world.bridge.run("e1")
    assert (first.bridged, first.skipped_no_consent) == (1, 1)
    again = world.bridge.run("e1")
    assert (again.bridged, again.already_recorded) == (0, 1)
    rows = sqlite3.connect(world.db.path).execute("SELECT COUNT(*) FROM evidence_items").fetchone()[0]
    assert rows == 2  # artifact + policy, not duplicated


def test_exception_in_force_when_answer_was_saved_is_in_assistance_context(tmp_path):
    world = World(tmp_path)
    world.link()
    world.bridge.set_consent("e1", "student-1", True)
    world.now -= timedelta(minutes=30)  # granted before the (already saved) answer
    world.contracts.grant_exception("e1", "lecturer-1", "student-1", ExceptionReason.ACCESSIBILITY,
                                    {"external_ide": "ALLOW"}, 15)
    world.now += timedelta(hours=1)
    world.close()
    [case_id] = world.bridge.run("e1").research_case_ids
    [artifact] = [e for e in P001Repository(world.db).get_evidence_for_claim(case_id, "CC3")
                  if e.evidence_type is EvidenceType.ARTIFACT]
    context = json.loads(artifact.assistance_context)
    assert context["exceptions"] == [{"capability_overrides": {"external_ide": "ALLOW"}, "extra_time_minutes": 15}]
    assert "ACCESSIBILITY" not in artifact.assistance_context  # reason category is not copied


def test_partial_failure_converges_on_rerun(tmp_path):
    world = World(tmp_path)
    world.link()
    world.bridge.set_consent("e1", "student-1", True)
    world.close()
    real_save = world.research_repo.save_bridge_record
    world.research_repo.save_bridge_record = lambda record: (_ for _ in ()).throw(RuntimeError("MySQL down"))
    with pytest.raises(RuntimeError):
        world.bridge.run("e1")  # research store written, operational record not
    world.research_repo.save_bridge_record = real_save
    assert world.bridge.run("e1").bridged == 1  # same deterministic rows, no duplicate errors
    rows = sqlite3.connect(world.db.path).execute("SELECT COUNT(*) FROM evidence_items").fetchone()[0]
    assert rows == 2


def test_answer_saved_without_contract_in_force_is_recorded_not_assumed(tmp_path):
    world = World(tmp_path)
    world.link()
    world.bridge.set_consent("e1", "student-1", True)
    world.close()
    bound = world.contract_repo.get_bound("e1")
    world.contract_repo.versions[("e1", bound.version)] = replace(bound, bound_at=world.now + timedelta(days=1))
    summary = world.bridge.run("e1")
    assert (summary.bridged, summary.no_contract) == (0, 1)
    assert world.research_repo.records[(world.s1, "q1")].outcome is BridgeOutcome.NO_CONTRACT
