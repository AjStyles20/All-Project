"""FD-06 operational -> EGPCV evidence bridge (ECC v1.0 §6, DR-013, DR-015)."""
import json
from dataclasses import dataclass, field
from pathlib import Path
from uuid import uuid4

import app

from app.domain.candidate_session import SessionStatus
from app.domain.enums import ClaimApplicability, EvidenceType
from app.domain.examination import ExaminationConflictError, ExaminationStatus
from app.domain.models import CaseClaim, ClaimEvidenceLink, EvidenceItem, ProgrammingCase
from app.domain.research_bridge import (
    SOURCE_TYPE, BridgeOutcome, BridgeRecord, ConsentStatus, ResearchBridgeError, ResearchLink,
    ResearchStoreNotConfigured,
    assistance_context, new_research_code, research_case_id, research_policy_document,
)
from app.services.candidate_session_service import AssignmentNotFoundError, utc_now
from app.services.examination_service import ExaminationNotFoundError, QuestionNotFoundError

BRIDGEABLE_STATUSES = {ExaminationStatus.CLOSED, ExaminationStatus.ARCHIVED}
# DR-016 (2): the research store must not live inside the application directory,
# where it would travel with deployments and be readable by anything serving the app.
APPLICATION_DIR = Path(app.__file__).resolve().parent.parent


@dataclass
class BridgeSummary:
    bridged: int = 0
    no_response: int = 0
    no_contract: int = 0
    already_recorded: int = 0
    skipped_no_consent: int = 0
    research_case_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class WithdrawalResult:
    cases_deleted: int = 0
    cases_retained_as_shell: int = 0
    # True if bridged data exists but the research store was unavailable: the
    # withdrawal still counts (no further copying) and an administrator must re-run the purge.
    purge_pending: bool = False


@dataclass(frozen=True)
class ConsentResult:
    status: ConsentStatus
    withdrawal: WithdrawalResult | None = None


@dataclass(frozen=True)
class ConsentInfo:
    links: list[ResearchLink]
    status: ConsentStatus | None


class ResearchBridgeService:
    def __init__(self, research_repository, case_store, examination_repository, session_repository,
                 review_repository, contract_repository, clock=utc_now):
        self.research = research_repository
        # None when no research store is configured: the bridge then refuses to run
        # instead of pretending to copy anything.
        self.store = case_store
        self.examinations = examination_repository
        self.sessions = session_repository
        self.reviews = review_repository
        self.contracts = contract_repository
        self.clock = clock

    # Administrator: links

    def create_link(self, actor_user_id: str, examination_id: str, question_id: str,
                    template_case_id: str, claim_ids: list[str], ethics_reference: str) -> ResearchLink:
        store = self._store()
        if self.examinations.get_examination(examination_id) is None:
            raise ExaminationNotFoundError(examination_id)
        if question_id not in {e.question.question_id
                               for e in self.examinations.list_examination_questions(examination_id)}:
            raise QuestionNotFoundError("Question is not part of this examination.")
        if store.get_case(template_case_id) is None:
            raise ResearchBridgeError("Template case does not exist in the research store.")
        required = {c.claim_id for c in store.get_case_claims(template_case_id)
                    if c.applicability is ClaimApplicability.REQUIRED}
        unknown = sorted(set(claim_ids) - required)
        if unknown:
            raise ResearchBridgeError(f"Claims {unknown} are not REQUIRED claims of the template case.")
        link = ResearchLink(str(uuid4()), examination_id, question_id, template_case_id, tuple(claim_ids),
                            ethics_reference, actor_user_id, self.clock())
        self.research.create_link(link)
        return link

    def list_questions(self, examination_id: str):
        """Question ids and titles for the administrator's link form (no answers or scores)."""
        if self.examinations.get_examination(examination_id) is None:
            raise ExaminationNotFoundError(examination_id)
        return self.examinations.list_examination_questions(examination_id)

    def list_links(self, examination_id: str) -> list[ResearchLink]:
        return self.research.list_links(examination_id)

    def list_identities(self, examination_id: str) -> list[tuple[str, str]]:
        return self.research.list_identities(examination_id)

    def list_records(self, examination_id: str) -> list[BridgeRecord]:
        return self.research.list_bridge_records(examination_id)

    # Candidate: consent

    def consent_info(self, examination_id: str, candidate_user_id: str) -> ConsentInfo:
        self._require_assignment(examination_id, candidate_user_id)
        return ConsentInfo(self.research.list_links(examination_id),
                           self.research.current_consent(examination_id, candidate_user_id))

    def set_consent(self, examination_id: str, candidate_user_id: str, opt_in: bool) -> ConsentResult:
        self._require_assignment(examination_id, candidate_user_id)
        if not self.research.list_links(examination_id):
            raise ExaminationConflictError("No research study is linked to this examination.")
        status = ConsentStatus.OPTED_IN if opt_in else ConsentStatus.WITHDRAWN
        # Recorded first: even if deletion cannot run now, no further copying happens.
        self.research.record_consent(examination_id, candidate_user_id, status, self.clock())
        if opt_in:
            return ConsentResult(status)
        return ConsentResult(status, self.purge_candidate(examination_id, candidate_user_id))

    def purge_candidate(self, examination_id: str, candidate_user_id: str) -> WithdrawalResult:
        """DR-016 (1): delete a withdrawn candidate's bridged cases. Safe to repeat."""
        case_ids = self.research.bridged_case_ids(examination_id, candidate_user_id)
        code = self.research.get_research_code(examination_id, candidate_user_id)
        if case_ids:
            try:
                store = self._store()
            except ResearchStoreNotConfigured:
                return WithdrawalResult(purge_pending=True)
        # Research store first: if MySQL then fails, the case ids are still known and a
        # retry re-deletes (idempotently) before forgetting them.
        deleted = retained = 0
        for case_id in case_ids:
            if store.purge_case(case_id):
                deleted += 1
            else:
                retained += 1
        self.research.complete_withdrawal(examination_id, candidate_user_id, code, deleted, retained, self.clock())
        return WithdrawalResult(deleted, retained)

    def purge_withdrawn(self, examination_id: str) -> WithdrawalResult:
        """Administrator retry for pending deletions (e.g. store was unavailable)."""
        deleted = retained = 0
        for candidate_user_id, _ in self.research.list_identities(examination_id):
            if self.research.current_consent(examination_id, candidate_user_id) is not ConsentStatus.WITHDRAWN:
                continue
            result = self.purge_candidate(examination_id, candidate_user_id)
            if result.purge_pending:
                return WithdrawalResult(deleted, retained, purge_pending=True)
            deleted += result.cases_deleted
            retained += result.cases_retained_as_shell
        return WithdrawalResult(deleted, retained)

    def list_withdrawal_log(self, examination_id: str) -> list[dict]:
        return self.research.list_withdrawal_log(examination_id)

    # Administrator: run

    def run(self, examination_id: str) -> BridgeSummary:
        store = self._store()
        exam = self.examinations.get_examination(examination_id)
        if exam is None:
            raise ExaminationNotFoundError(examination_id)
        if exam.status not in BRIDGEABLE_STATUSES:
            # Only final, closed work is copied; a running exam could still change.
            raise ResearchBridgeError("The bridge runs only after the examination is CLOSED.")
        links = self.research.list_links(examination_id)
        summary = BridgeSummary()
        for session, assignment in self.reviews.list_sessions_for_examination(examination_id):
            if session.status is not SessionStatus.SUBMITTED:
                continue
            # Gate 2 (DR-015 (1)): the candidate's *current* consent. Withdrawal stops copying.
            if self.research.current_consent(examination_id, assignment.candidate_user_id) is not ConsentStatus.OPTED_IN:
                summary.skipped_no_consent += 1
                continue
            for link in links:
                self._bridge_one(store, exam.examination_id, session, assignment.candidate_user_id, link, summary)
        return summary

    def _bridge_one(self, store, examination_id, session, candidate_user_id, link, summary) -> None:
        if self.research.get_bridge_record(session.session_id, link.question_id) is not None:
            summary.already_recorded += 1
            return
        now = self.clock()
        response = self.sessions.get_response(session.session_id, link.question_id)
        if response is None:
            self._record(BridgeRecord(session.session_id, link.question_id, link.link_id,
                                      BridgeOutcome.NO_RESPONSE, None, None, None, now), summary)
            return
        contract = self.contracts.in_force_at(examination_id, response.saved_at)
        if contract is None:
            self._record(BridgeRecord(session.session_id, link.question_id, link.link_id,
                                      BridgeOutcome.NO_CONTRACT, None, response.revision, None, now), summary)
            return

        code = self._research_code(examination_id, candidate_user_id)
        case_id = research_case_id(code, link.question_id)
        template = store.get_case(link.template_case_id)
        case = ProgrammingCase(case_id, template.title, template.task_description, template.language,
                               template.version)
        case_claims = [CaseClaim(case_id, c.claim_id, c.applicability)
                       for c in store.get_case_claims(link.template_case_id)]
        policy_version = contract.policy_version_label()
        context = assistance_context(contract, self.contracts.list_exceptions(examination_id, candidate_user_id),
                                     link.claim_ids, response.saved_at)
        # Deterministic ids: a re-run after a partial failure writes the same rows.
        artifact = EvidenceItem(f"{case_id}:artifact:r{response.revision}", case_id, EvidenceType.ARTIFACT,
                                response.content, SOURCE_TYPE, response.saved_at, policy_version, context)
        policy = EvidenceItem(f"{case_id}:policy:v{contract.version}", case_id, EvidenceType.POLICY_CONTEXT,
                              research_policy_document(contract),
                              SOURCE_TYPE, contract.bound_at, policy_version, None)
        rationale = f"FD-06 bridged submission under research link {link.link_id} (ethics ref {link.ethics_reference})."
        links = [ClaimEvidenceLink(case_id, claim, evidence.evidence_id, rationale)
                 for claim in link.claim_ids for evidence in (artifact, policy)]
        store.materialise(case, case_claims, [artifact, policy], links)
        self._record(BridgeRecord(session.session_id, link.question_id, link.link_id, BridgeOutcome.BRIDGED,
                                  case_id, response.revision, policy_version, now), summary)

    def _record(self, record: BridgeRecord, summary: BridgeSummary) -> None:
        if not self.research.save_bridge_record(record):
            summary.already_recorded += 1
            return
        if record.outcome is BridgeOutcome.BRIDGED:
            summary.bridged += 1
            summary.research_case_ids.append(record.research_case_id)
        elif record.outcome is BridgeOutcome.NO_RESPONSE:
            summary.no_response += 1
        else:
            summary.no_contract += 1

    def _research_code(self, examination_id: str, candidate_user_id: str) -> str:
        code = self.research.get_research_code(examination_id, candidate_user_id)
        if code is None:
            self.research.create_research_code(examination_id, candidate_user_id, new_research_code(), self.clock())
            code = self.research.get_research_code(examination_id, candidate_user_id)
        return code

    def _require_assignment(self, examination_id: str, candidate_user_id: str) -> None:
        if self.sessions.get_assignment(examination_id, candidate_user_id) is None:
            raise AssignmentNotFoundError("No assignment for this examination.")

    def _store(self):
        if self.store is None:
            raise ResearchStoreNotConfigured("Research store is not configured (set P001_RESEARCH_DB_PATH).")
        if Path(self.store.database.path).resolve().is_relative_to(APPLICATION_DIR):
            raise ResearchStoreNotConfigured(
                "Research store must live outside the application directory (DR-016); "
                "move the file and update P001_RESEARCH_DB_PATH.")
        return self.store
