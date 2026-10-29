"""In-memory stand-in for MySQLContractRepository used by FD-05 tests.

Mirrors the SQL semantics: DRAFT-only edits while the exam is DRAFT, binding on
schedule (supersede the old BOUND version, bind the draft, require one BOUND),
amendments only while SCHEDULED/ACTIVE, and bound versions never rewritten.
"""
from dataclasses import replace
from datetime import datetime, timezone

from app.domain.capability_contract import ContractRequiredError, ContractStatus
from app.domain.examination import ExaminationConflictError, ExaminationStatus


class InMemoryContractRepository:
    def __init__(self, examination_repository):
        self.examinations = examination_repository
        examination_repository.contract_repository = self
        self.versions = {}  # (examination_id, version) -> contract
        self.exceptions = []

    def _of(self, examination_id):
        return sorted((c for (eid, _), c in self.versions.items() if eid == examination_id),
                      key=lambda c: c.version)

    def list_versions(self, examination_id):
        return self._of(examination_id)

    def get_latest(self, examination_id):
        versions = self._of(examination_id)
        return versions[-1] if versions else None

    def get_bound(self, examination_id):
        return next((c for c in self._of(examination_id) if c.status is ContractStatus.BOUND), None)

    def has_bindable(self, examination_id):
        return any(c.status in (ContractStatus.DRAFT, ContractStatus.BOUND) for c in self._of(examination_id))

    def in_force_at(self, examination_id, at):
        bound = [c for c in self._of(examination_id) if c.bound_at is not None and c.bound_at <= at]
        return max(bound, key=lambda c: (c.bound_at, c.version)) if bound else None

    def save_draft(self, contract):
        contract.validate()
        exam = self.examinations.exams.get(contract.examination_id)
        if exam is None or exam.status is not ExaminationStatus.DRAFT:
            return False
        existing = self.versions.get((contract.examination_id, contract.version))
        if existing is not None and existing.status is not ContractStatus.DRAFT:
            raise ExaminationConflictError("That contract version is already bound.")
        self.versions[(contract.examination_id, contract.version)] = replace(
            contract, status=ContractStatus.DRAFT, content_hash=contract.compute_hash())
        return True

    def bind(self, examination_id):
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        draft = next((c for c in self._of(examination_id) if c.status is ContractStatus.DRAFT), None)
        if draft is not None:
            for c in self._of(examination_id):
                if c.status is ContractStatus.BOUND:
                    self.versions[(examination_id, c.version)] = replace(c, status=ContractStatus.SUPERSEDED)
            self.versions[(examination_id, draft.version)] = replace(draft, status=ContractStatus.BOUND, bound_at=now)
        if self.get_bound(examination_id) is None:
            raise ContractRequiredError("Scheduling requires a capability contract (ECC spec §5.2).")

    def amend_bound(self, contract, bound_at):
        contract.validate()
        exam = self.examinations.exams[contract.examination_id]
        current = self.versions.get((contract.examination_id, contract.supersedes_version))
        if (exam.status not in (ExaminationStatus.SCHEDULED, ExaminationStatus.ACTIVE)
                or current is None or current.status is not ContractStatus.BOUND):
            return False
        if (contract.examination_id, contract.version) in self.versions:
            raise ExaminationConflictError("A newer contract version already exists.")
        self.versions[(contract.examination_id, current.version)] = replace(current, status=ContractStatus.SUPERSEDED)
        self.versions[(contract.examination_id, contract.version)] = replace(
            contract, status=ContractStatus.BOUND, bound_at=bound_at, content_hash=contract.compute_hash())
        return True

    def create_exception(self, exception):
        exception.validate()
        self.exceptions.append(exception)

    def list_exceptions(self, examination_id, candidate_user_id=None):
        return [e for e in self.exceptions if e.examination_id == examination_id
                and (candidate_user_id is None or e.candidate_user_id == candidate_user_id)]
