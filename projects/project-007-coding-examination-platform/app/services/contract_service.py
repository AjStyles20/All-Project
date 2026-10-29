"""FD-05 Examination Capability Contract management (ECC v1.0, DR-013)."""
from dataclasses import dataclass, replace
from uuid import uuid4

from app.domain.capability_contract import (
    AssistanceConstruct, CapabilityContract, ContractException, ContractStatus,
    ExceptionReason, IntegrityMode, normalise_capabilities,
)
from app.domain.examination import Examination, ExaminationConflictError, ExaminationStatus
from app.services.candidate_session_service import AssignmentNotFoundError, utc_now
from app.services.examination_service import ExaminationNotFoundError, ExaminationOwnershipError

AMENDABLE_STATUSES = {ExaminationStatus.SCHEDULED, ExaminationStatus.ACTIVE}


@dataclass(frozen=True)
class ContractDeclaration:
    """What an examiner declares; versioning fields are filled in by the service."""
    capabilities: dict
    integrity_mode: IntegrityMode = IntegrityMode.LAB_CONTROLLED  # DR-013 Q5 default
    assistance_default: AssistanceConstruct = AssistanceConstruct.INDEPENDENT
    assistance_per_claim: dict | None = None
    remote_proctoring_justification: str | None = None


@dataclass(frozen=True)
class CandidateContractView:
    contract: CapabilityContract
    exceptions: list[ContractException]


class ContractService:
    def __init__(self, contract_repository, examination_repository, session_repository, clock=utc_now):
        self.contracts = contract_repository
        self.examinations = examination_repository
        self.sessions = session_repository
        self.clock = clock

    def list_versions(self, examination_id: str, actor_user_id: str) -> list[CapabilityContract]:
        self._owned_exam(examination_id, actor_user_id)
        return self.contracts.list_versions(examination_id)

    def save_draft(self, examination_id: str, actor_user_id: str, declaration: ContractDeclaration,
                   amendment_reason: str | None = None) -> CapabilityContract:
        exam = self._owned_exam(examination_id, actor_user_id)
        if exam.status is not ExaminationStatus.DRAFT:
            raise ExaminationConflictError("Draft contracts can only be edited while the examination is DRAFT; "
                                           "use an amendment once it is scheduled.")
        latest = self.contracts.get_latest(examination_id)
        if latest is None:
            version, supersedes = 1, None
        elif latest.status is ContractStatus.DRAFT:
            version, supersedes = latest.version, latest.supersedes_version
        else:
            # The exam went back to DRAFT after binding: candidates may have seen the bound
            # rules, so the next version must say why it changes them (spec §5.3).
            version, supersedes = latest.version + 1, latest.version
        contract = self._build(exam, version, ContractStatus.DRAFT, declaration, supersedes,
                               amendment_reason if supersedes is not None else None)
        if not self.contracts.save_draft(contract):
            raise ExaminationConflictError("Examination is no longer DRAFT; reload before editing the contract.")
        return replace(contract, content_hash=contract.compute_hash())

    def amend(self, examination_id: str, actor_user_id: str, declaration: ContractDeclaration,
              amendment_reason: str) -> CapabilityContract:
        exam = self._owned_exam(examination_id, actor_user_id)
        if exam.status not in AMENDABLE_STATUSES:
            raise ExaminationConflictError(f"A {exam.status.value} examination's contract cannot be amended.")
        bound = self.contracts.get_bound(examination_id)
        if bound is None:
            raise ExaminationConflictError("No bound contract to amend.")
        latest = self.contracts.get_latest(examination_id)
        now = self.clock()
        contract = self._build(exam, latest.version + 1, ContractStatus.BOUND, declaration,
                               bound.version, amendment_reason)
        contract = replace(contract, bound_at=now, content_hash=contract.compute_hash())
        if not self.contracts.amend_bound(contract, now):
            raise ExaminationConflictError("Contract or examination changed; reload before amending.")
        return contract

    def grant_exception(self, examination_id: str, actor_user_id: str, candidate_user_id: str,
                        reason_category: ExceptionReason, capability_overrides: dict | None = None,
                        extra_time_minutes: int = 0) -> ContractException:
        exam = self._owned_exam(examination_id, actor_user_id)
        if exam.status not in AMENDABLE_STATUSES:
            raise ExaminationConflictError("Exceptions can be granted only while the examination is SCHEDULED or ACTIVE.")
        bound = self.contracts.get_bound(examination_id)
        if bound is None:
            raise ExaminationConflictError("No bound contract to add an exception to.")
        if self.sessions.get_assignment(examination_id, candidate_user_id) is None:
            raise AssignmentNotFoundError("Candidate is not assigned to this examination.")
        exception = ContractException(str(uuid4()), examination_id, bound.version, candidate_user_id,
                                      reason_category, actor_user_id, self.clock(),
                                      capability_overrides or {}, extra_time_minutes)
        exception.validate()
        self.contracts.create_exception(exception)
        return exception

    def list_exceptions(self, examination_id: str, actor_user_id: str) -> list[ContractException]:
        self._owned_exam(examination_id, actor_user_id)
        return self.contracts.list_exceptions(examination_id)

    def candidate_view(self, examination_id: str, candidate_user_id: str) -> CandidateContractView:
        if self.sessions.get_assignment(examination_id, candidate_user_id) is None:
            raise AssignmentNotFoundError("No assignment for this examination.")
        bound = self.contracts.get_bound(examination_id)
        if bound is None:
            raise ExaminationConflictError("The examination rules have not been published yet.")
        return CandidateContractView(bound, self.contracts.list_exceptions(examination_id, candidate_user_id))

    def in_force_at(self, examination_id: str, at) -> CapabilityContract | None:
        """For evidence labelling (FD-06): the version in force when an event happened."""
        return self.contracts.in_force_at(examination_id, at)

    def _build(self, exam: Examination, version: int, status: ContractStatus,
               declaration: ContractDeclaration, supersedes: int | None,
               reason: str | None) -> CapabilityContract:
        contract = CapabilityContract(
            exam.examination_id, version, status, declaration.integrity_mode,
            normalise_capabilities(declaration.capabilities), declaration.assistance_default,
            dict(declaration.assistance_per_claim or {}), declaration.remote_proctoring_justification,
            # Only the owner can schedule or amend (FD-02 ownership), so the binder is known now
            # and can be inside the content hash (spec §8).
            exam.owner_user_id, supersedes, reason,
        )
        contract.validate()
        return contract

    def _owned_exam(self, examination_id: str, actor_user_id: str) -> Examination:
        exam = self.examinations.get_examination(examination_id)
        if exam is None:
            raise ExaminationNotFoundError(examination_id)
        if exam.owner_user_id != actor_user_id:
            raise ExaminationOwnershipError("Only the owning examiner may manage this examination's contract.")
        return exam
