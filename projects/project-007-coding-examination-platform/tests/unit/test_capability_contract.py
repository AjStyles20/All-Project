from dataclasses import replace
from datetime import datetime, timedelta

import pytest

from app.domain.candidate_session import SessionConflictError
from app.domain.capability_contract import (
    CapabilityContract, ContractException, ContractRequiredError, ContractStatus, ExceptionReason,
    IntegrityMode,
)
from app.domain.examination import (
    Examination, ExaminationConflictError, ExaminationStatus, ProgrammingQuestion,
)
from app.services.candidate_session_service import AssignmentNotFoundError, CandidateSessionService
from app.services.contract_service import ContractDeclaration, ContractService
from app.services.examination_service import ExaminationOwnershipError, ExaminationService
from tests.candidate_session_fakes import InMemoryCandidateSessionRepository
from tests.contract_fakes import InMemoryContractRepository
from tests.contract_helpers import LAB_CAPABILITIES
from tests.examination_fakes import InMemoryExaminationRepository

NOW = datetime(2026, 11, 3, 9, 0)


# ---- domain ----

def contract(**changes):
    base = CapabilityContract("e1", 1, ContractStatus.DRAFT, IntegrityMode.LAB_CONTROLLED,
                              dict(LAB_CAPABILITIES), bound_by_user_id="lecturer-1")
    return replace(base, **changes)


def test_every_capability_key_is_required_and_values_are_checked():
    missing = dict(LAB_CAPABILITIES); missing.pop("internet")
    with pytest.raises(ValueError, match="missing"):
        contract(capabilities=missing).validate()
    with pytest.raises(ValueError):
        contract(capabilities={**LAB_CAPABILITIES, "ai_assistance": "MAYBE"}).validate()
    with pytest.raises(ValueError):
        contract(capabilities={**LAB_CAPABILITIES, "teleport": "ALLOW"}).validate()


def test_values_needing_detail_require_it():
    with pytest.raises(ValueError, match="allowlist"):
        contract(capabilities={**LAB_CAPABILITIES, "terminal": "LIMITED"}).validate()
    with pytest.raises(ValueError, match="limits"):
        contract(capabilities={**LAB_CAPABILITIES, "ai_assistance": {"value": "ALLOW_BOUNDED"}}).validate()
    with pytest.raises(ValueError, match="no extra detail"):
        contract(capabilities={**LAB_CAPABILITIES, "internet": {"value": "DENY", "sources": ["x"]}}).validate()
    contract(capabilities={**LAB_CAPABILITIES, "ai_assistance": {"value": "ALLOW_BOUNDED",
                                                                "limits": "Syntax lookup only"}}).validate()


def test_remote_proctoring_needs_justification_and_amendments_need_reason():
    with pytest.raises(ValueError, match="justification"):
        contract(integrity_mode=IntegrityMode.REMOTE_PROCTORED).validate()
    contract(integrity_mode=IntegrityMode.REMOTE_PROCTORED,
             remote_proctoring_justification="Distance cohort; policy ref approved").validate()
    with pytest.raises(ValueError, match="reason"):
        contract(version=2, supersedes_version=1).validate()


def test_hash_is_canonical_and_excludes_status_and_binding_time():
    a = contract()
    shuffled = contract(capabilities=dict(reversed(list(LAB_CAPABILITIES.items()))))
    assert a.compute_hash() == shuffled.compute_hash()
    assert a.compute_hash() == replace(a, status=ContractStatus.BOUND, bound_at=NOW).compute_hash()
    assert a.compute_hash() != contract(capabilities={**LAB_CAPABILITIES, "internet": "ALLOW"}).compute_hash()
    assert a.compute_hash().startswith("sha256:") and len(a.compute_hash()) == 71
    assert a.policy_version_label().startswith("ecc:e1@v1#")


def test_exception_validation():
    base = ContractException("x", "e1", 1, "s1", ExceptionReason.ACCESSIBILITY, "l1", NOW)
    with pytest.raises(ValueError):
        base.validate()  # changes nothing
    replace(base, extra_time_minutes=30).validate()
    with pytest.raises(ValueError):
        replace(base, capability_overrides={"terminal": "LIMITED"}).validate()  # missing allowlist
    replace(base, capability_overrides={"ai_assistance": "DECLARE"}).validate()


# ---- service ----

def setup():
    exams = InMemoryExaminationRepository()
    contracts_repo = InMemoryContractRepository(exams)
    session_repo = InMemoryCandidateSessionRepository({"student-1"})
    exams.create_examination(Examination("e1", "Exam", "", "lecturer-1", ExaminationStatus.DRAFT))
    exams.create_question(ProgrammingQuestion("q1", "Loops", "Write a loop", "python", 10), "lecturer-1")
    exams.attachments.append(("e1", "q1", 1, 10))
    clock = lambda: NOW
    contracts = ContractService(contracts_repo, exams, session_repo, clock)
    candidates = CandidateSessionService(session_repo, exams, clock)
    return contracts, ExaminationService(exams), candidates, contracts_repo


DECLARATION = ContractDeclaration(dict(LAB_CAPABILITIES))


def test_scheduling_without_contract_is_refused_and_rolls_back():
    contracts, exams, _, _ = setup()
    with pytest.raises(ContractRequiredError):
        exams.transition("e1", "lecturer-1", ExaminationStatus.SCHEDULED)
    assert exams.repository.exams["e1"].status is ExaminationStatus.DRAFT


def test_draft_is_editable_then_bound_on_schedule():
    contracts, exams, _, repo = setup()
    first = contracts.save_draft("e1", "lecturer-1", DECLARATION)
    assert (first.version, first.status, first.integrity_mode) == (1, ContractStatus.DRAFT, IntegrityMode.LAB_CONTROLLED)
    edited = contracts.save_draft("e1", "lecturer-1", ContractDeclaration({**LAB_CAPABILITIES, "debugger": "DENY"}))
    assert edited.version == 1 and edited.content_hash != first.content_hash
    exams.transition("e1", "lecturer-1", ExaminationStatus.SCHEDULED)
    bound = repo.get_bound("e1")
    assert bound.status is ContractStatus.BOUND and bound.bound_at is not None
    assert bound.content_hash == edited.content_hash
    with pytest.raises(ExaminationConflictError):
        contracts.save_draft("e1", "lecturer-1", DECLARATION)  # exam no longer DRAFT


def test_return_to_draft_keeps_bound_rules_until_a_reasoned_new_version():
    contracts, exams, _, repo = setup()
    contracts.save_draft("e1", "lecturer-1", DECLARATION)
    exams.transition("e1", "lecturer-1", ExaminationStatus.SCHEDULED)
    exams.transition("e1", "lecturer-1", ExaminationStatus.DRAFT)
    with pytest.raises(ValueError, match="reason"):
        contracts.save_draft("e1", "lecturer-1", DECLARATION)
    v2 = contracts.save_draft("e1", "lecturer-1", DECLARATION, amendment_reason="Allow debugger for all")
    assert (v2.version, v2.supersedes_version) == (2, 1)
    assert repo.get_bound("e1").version == 1  # still v1 until scheduled again
    exams.transition("e1", "lecturer-1", ExaminationStatus.SCHEDULED)
    assert repo.get_bound("e1").version == 2
    assert [c.status for c in repo.list_versions("e1")] == [ContractStatus.SUPERSEDED, ContractStatus.BOUND]


def test_amendment_is_new_version_and_never_retroactive():
    contracts, exams, _, repo = setup()
    contracts.save_draft("e1", "lecturer-1", DECLARATION)
    exams.transition("e1", "lecturer-1", ExaminationStatus.SCHEDULED)
    v1 = repo.get_bound("e1")
    contracts.clock = lambda: v1.bound_at + timedelta(hours=1)
    v2 = contracts.amend("e1", "lecturer-1", ContractDeclaration({**LAB_CAPABILITIES, "internet": "ALLOW"}),
                         "Network docs mirror unavailable")
    assert (v2.version, v2.status, v2.supersedes_version) == (2, ContractStatus.BOUND, 1)
    assert repo.list_versions("e1")[0].status is ContractStatus.SUPERSEDED
    assert repo.list_versions("e1")[0].content_hash == v1.content_hash  # v1 unchanged
    # Events before the amendment keep v1; later events get v2.
    assert contracts.in_force_at("e1", v1.bound_at + timedelta(minutes=30)).version == 1
    assert contracts.in_force_at("e1", v2.bound_at + timedelta(minutes=1)).version == 2
    assert contracts.in_force_at("e1", v1.bound_at - timedelta(minutes=1)) is None


def test_amend_and_exceptions_require_scheduled_or_active():
    contracts, _, _, _ = setup()
    contracts.save_draft("e1", "lecturer-1", DECLARATION)
    with pytest.raises(ExaminationConflictError):
        contracts.amend("e1", "lecturer-1", DECLARATION, "why")
    with pytest.raises(ExaminationConflictError):
        contracts.grant_exception("e1", "lecturer-1", "student-1", ExceptionReason.ACCESSIBILITY, extra_time_minutes=20)


def test_exceptions_need_assigned_candidate_and_are_visible_to_that_candidate():
    contracts, exams, candidates, _ = setup()
    contracts.save_draft("e1", "lecturer-1", DECLARATION)
    candidates.assign_candidate("e1", "student-1", "lecturer-1")
    with pytest.raises(ExaminationConflictError):
        contracts.candidate_view("e1", "student-1")  # rules not published yet
    exams.transition("e1", "lecturer-1", ExaminationStatus.SCHEDULED)
    with pytest.raises(AssignmentNotFoundError):
        contracts.grant_exception("e1", "lecturer-1", "stranger", ExceptionReason.TECHNICAL, extra_time_minutes=5)
    granted = contracts.grant_exception("e1", "lecturer-1", "student-1", ExceptionReason.ACCESSIBILITY,
                                        {"external_ide": "ALLOW"}, 30)
    assert granted.contract_version == 1
    view = contracts.candidate_view("e1", "student-1")
    assert view.contract.version == 1 and [e.exception_id for e in view.exceptions] == [granted.exception_id]
    with pytest.raises(AssignmentNotFoundError):
        contracts.candidate_view("e1", "student-2")


def test_only_owner_manages_contract():
    contracts, _, _, _ = setup()
    with pytest.raises(ExaminationOwnershipError):
        contracts.save_draft("e1", "lecturer-2", DECLARATION)
    with pytest.raises(ExaminationOwnershipError):
        contracts.list_versions("e1", "lecturer-2")


# ---- extra time applied to the candidate deadline ----

def test_extra_time_extends_only_that_candidates_deadline():
    contracts, exams, _, repo = setup()
    ends = NOW + timedelta(hours=2)
    exams.repository.exams["e1"] = replace(exams.repository.exams["e1"], starts_at=NOW, ends_at=ends)
    session_repo = InMemoryCandidateSessionRepository({"student-1", "student-2"})
    clock = {"now": NOW}
    candidates = CandidateSessionService(session_repo, exams.repository, lambda: clock["now"], repo)
    contracts.sessions = session_repo
    candidates.assign_candidate("e1", "student-1", "lecturer-1")
    candidates.assign_candidate("e1", "student-2", "lecturer-1")
    contracts.save_draft("e1", "lecturer-1", DECLARATION)
    exams.transition("e1", "lecturer-1", ExaminationStatus.SCHEDULED)
    exams.transition("e1", "lecturer-1", ExaminationStatus.ACTIVE)
    s1 = candidates.start_session("e1", "student-1").session_id
    s2 = candidates.start_session("e1", "student-2").session_id
    contracts.grant_exception("e1", "lecturer-1", "student-1", ExceptionReason.ACCESSIBILITY, extra_time_minutes=20)
    contracts.grant_exception("e1", "lecturer-1", "student-1", ExceptionReason.TECHNICAL, extra_time_minutes=30)

    clock["now"] = ends + timedelta(minutes=10)
    candidates.save_response(s1, "q1", "student-1", "still within extra time")
    with pytest.raises(SessionConflictError):
        candidates.save_response(s2, "q1", "student-2", "too late")
    view = candidates.get_session_view(s1, "student-1")
    # Largest single grant applies (30), not the sum (50).
    assert view.effective_ends_at == ends + timedelta(minutes=30)
    assert candidates.get_session_view(s2, "student-2").effective_ends_at == ends
    clock["now"] = ends + timedelta(minutes=30)
    with pytest.raises(SessionConflictError):
        candidates.save_response(s1, "q1", "student-1", "past extended deadline")
