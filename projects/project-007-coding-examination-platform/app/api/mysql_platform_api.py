"""MySQL-backed construction entry point for the full P001 platform."""
from contextlib import contextmanager
from datetime import datetime, timezone
from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field
from uuid import uuid4

from app.domain.examination import (
    Examination, ExaminationConflictError, ExaminationQuestionEntry, ExaminationStatus,
    ProgrammingQuestion,
)
from app.domain.candidate_session import (
    MAX_RESPONSE_CHARS, CandidateAssignment, ExaminationSession, SavedResponse, SessionConflictError,
)
from app.persistence.mysql_candidate_session_repository import MySQLCandidateSessionRepository
from app.domain.capability_contract import (
    AssistanceConstruct, CapabilityContract, ContractException, ContractStatus, ExceptionReason,
    IntegrityMode,
)
from app.persistence.mysql_contract_repository import MySQLContractRepository
from app.services.contract_service import ContractDeclaration, ContractService
from app.domain.review import MAX_COMMENT_CHARS, MarkingConflictError, ResponseMark, ResultRelease
from app.persistence.mysql_examination_repository import MySQLExaminationRepository
from app.persistence.mysql_review_repository import MySQLReviewRepository
from app.services.review_service import ReviewService
from app.services.candidate_session_service import (
    AssignmentNotFoundError, CandidateNotFoundError, CandidateSessionService, SessionNotFoundError,
)
from app.services.examination_service import (
    ExaminationNotFoundError, ExaminationOwnershipError, ExaminationService,
    InvalidExaminationTransition, QuestionNotFoundError,
)

from app.domain.identity import Role
from app.persistence.mysql_database import MySQLDatabase, MySQLSettings
from app.persistence.mysql_user_repository import MySQLUserRepository
from app.services.auth_service import AuthenticationError, AuthService


class LoginInput(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)

class ExaminationInput(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    starts_at: datetime | None = None
    ends_at: datetime | None = None

class QuestionInput(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    prompt: str = Field(min_length=1)
    language: str = Field(min_length=1, max_length=50)
    max_score: int = Field(gt=0)

class AttachQuestionInput(BaseModel):
    question_id: str
    display_order: int = Field(gt=0)
    score_weight: int = Field(gt=0)

class TransitionInput(BaseModel):
    target_status: ExaminationStatus

class AssignCandidateInput(BaseModel):
    candidate_user_id: str = Field(min_length=1, max_length=64)

class ContractInput(BaseModel):
    capabilities: dict
    integrity_mode: IntegrityMode = IntegrityMode.LAB_CONTROLLED
    assistance_default: AssistanceConstruct = AssistanceConstruct.INDEPENDENT
    assistance_per_claim: dict[str, AssistanceConstruct] = Field(default_factory=dict)
    remote_proctoring_justification: str | None = Field(default=None, max_length=2000)
    amendment_reason: str | None = Field(default=None, max_length=2000)

    def declaration(self) -> ContractDeclaration:
        return ContractDeclaration(self.capabilities, self.integrity_mode, self.assistance_default,
                                   dict(self.assistance_per_claim), self.remote_proctoring_justification)

class ExceptionInput(BaseModel):
    candidate_user_id: str = Field(min_length=1, max_length=64)
    reason_category: ExceptionReason
    capability_overrides: dict = Field(default_factory=dict)
    extra_time_minutes: int = Field(default=0, ge=0, le=1440)

class MarkInput(BaseModel):
    score: int = Field(ge=0)
    comment: str = Field(default="", max_length=MAX_COMMENT_CHARS)

class ResponseInput(BaseModel):
    content: str = Field(max_length=MAX_RESPONSE_CHARS)
    base_revision: int | None = Field(default=None, ge=0)


def _naive_utc(value: datetime | None) -> datetime | None:
    # MySQL DATETIME has no zone; store UTC so aware and naive inputs compare safely.
    if value is None or value.tzinfo is None:
        return value
    return value.astimezone(timezone.utc).replace(tzinfo=None)


def _examination_body(exam: Examination) -> dict:
    return {"examination_id": exam.examination_id, "title": exam.title,
            "description": exam.description, "status": exam.status.value,
            "starts_at": exam.starts_at.isoformat() if exam.starts_at else None,
            "ends_at": exam.ends_at.isoformat() if exam.ends_at else None}


def _question_body(question: ProgrammingQuestion) -> dict:
    return {"question_id": question.question_id, "title": question.title,
            "prompt": question.prompt, "language": question.language,
            "max_score": question.max_score, "version": question.version}


def _entry_body(entry: ExaminationQuestionEntry) -> dict:
    return {**_question_body(entry.question), "display_order": entry.display_order,
            "score_weight": entry.score_weight}


def _iso(value: datetime | None) -> str | None:
    return value.isoformat() if value else None


def _assignment_body(assignment: CandidateAssignment) -> dict:
    return {"assignment_id": assignment.assignment_id, "examination_id": assignment.examination_id,
            "candidate_user_id": assignment.candidate_user_id}


def _session_body(session: ExaminationSession) -> dict:
    return {"session_id": session.session_id, "status": session.status.value,
            "started_at": _iso(session.started_at), "submitted_at": _iso(session.submitted_at),
            "submission_mode": session.submission_mode.value if session.submission_mode else None}


def _contract_body(contract: CapabilityContract) -> dict:
    return {**contract.hashed_document(), "status": contract.status.value,
            "bound_at": _iso(contract.bound_at), "content_hash": contract.content_hash,
            "policy_version": contract.policy_version_label()
            if contract.status is not ContractStatus.DRAFT else None}


def _exception_body(exception: ContractException) -> dict:
    return {"exception_id": exception.exception_id, "candidate_user_id": exception.candidate_user_id,
            "contract_version": exception.contract_version,
            "capability_overrides": exception.capability_overrides,
            "extra_time_minutes": exception.extra_time_minutes,
            # Applied to the candidate's FD-03 deadline (largest single grant wins).
            "extra_time_applied_to_deadline": exception.extra_time_minutes > 0,
            "reason_category": exception.reason_category.value,
            "approved_at": _iso(exception.approved_at)}


def _mark_body(mark: ResponseMark) -> dict:
    return {"score": mark.score, "comment": mark.comment,
            "response_revision": mark.response_revision,
            "marked_by_user_id": mark.marked_by_user_id, "marked_at": _iso(mark.marked_at)}


def _release_body(release: ResultRelease | None) -> dict | None:
    return None if release is None else {"released_at": _iso(release.released_at),
                                         "released_by_user_id": release.released_by_user_id}


def _response_body(response: SavedResponse) -> dict:
    return {"question_id": response.question_id, "content": response.content,
            "revision": response.revision, "saved_at": _iso(response.saved_at)}


@contextmanager
def _policy_errors():
    """Map service-layer policy failures to HTTP status codes in one place."""
    try:
        yield
    except ExaminationNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Examination not found.") from exc
    except QuestionNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Question not found.") from exc
    except (AssignmentNotFoundError, CandidateNotFoundError, SessionNotFoundError) as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ExaminationOwnershipError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except (InvalidExaminationTransition, ExaminationConflictError, SessionConflictError,
            MarkingConflictError) as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


def create_mysql_platform_app(settings: MySQLSettings | None = None, *, auth_service=None,
                              examination_service=None, candidate_session_service=None,
                              review_service=None, contract_service=None) -> FastAPI:
    database = MySQLDatabase(settings)
    auth = auth_service or AuthService(MySQLUserRepository(database))
    examinations = examination_service or ExaminationService(MySQLExaminationRepository(database))
    sessions = candidate_session_service or CandidateSessionService(
        MySQLCandidateSessionRepository(database), MySQLExaminationRepository(database),
        contract_repository=MySQLContractRepository(database))
    contracts = contract_service or ContractService(
        MySQLContractRepository(database), MySQLExaminationRepository(database),
        MySQLCandidateSessionRepository(database))
    reviews = review_service or ReviewService(
        MySQLReviewRepository(database), MySQLCandidateSessionRepository(database),
        MySQLExaminationRepository(database))
    app = FastAPI(title="P001 Intelligent Coding Examination Platform", version="0.3.0")

    def current_principal(authorization: str | None = Header(default=None)):
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Bearer authentication required.")
        principal = auth.authenticate(authorization[7:])
        if principal is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid or expired session.")
        return principal

    def require_roles(*roles: Role):
        allowed = set(roles)
        def dependency(principal=Depends(current_principal)):
            if not principal.has_any_role(allowed):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Insufficient role.")
            return principal
        return dependency

    @app.get("/health")
    def health():
        return {"status": "ok", "scope": "platform", "database": "mysql"}

    @app.post("/auth/login")
    def login(payload: LoginInput):
        try:
            token, expires = auth.login(payload.username, payload.password)
        except AuthenticationError as exc:
            raise HTTPException(status_code=401, detail=str(exc)) from exc
        return {"access_token": token, "token_type": "bearer",
                "expires_at": expires.isoformat()}

    @app.post("/auth/logout", status_code=204)
    def logout(authorization: str | None = Header(default=None),
               principal=Depends(current_principal)):
        del principal
        auth.logout(authorization[7:])
        return None

    @app.get("/auth/me")
    def me(principal=Depends(current_principal)):
        return {"user_id": principal.user_id, "username": principal.username,
                "roles": sorted(role.value for role in principal.roles)}

    @app.get("/admin/ping")
    def admin_ping(principal=Depends(require_roles(Role.ADMINISTRATOR))):
        return {"status": "ok", "user_id": principal.user_id}

    @app.get("/examiner/ping")
    def examiner_ping(principal=Depends(require_roles(Role.EXAMINER, Role.ADMINISTRATOR))):
        return {"status": "ok", "user_id": principal.user_id}

    examiner = require_roles(Role.EXAMINER, Role.ADMINISTRATOR)

    @app.post("/examiner/examinations", status_code=201)
    def create_examination(payload: ExaminationInput, principal=Depends(examiner)):
        exam = Examination(str(uuid4()), payload.title, payload.description, principal.user_id,
                           ExaminationStatus.DRAFT, _naive_utc(payload.starts_at),
                           _naive_utc(payload.ends_at))
        with _policy_errors():
            examinations.create_examination(exam)
        return {"examination_id": exam.examination_id, "status": exam.status.value}

    @app.get("/examiner/examinations")
    def list_examinations(principal=Depends(examiner)):
        return [_examination_body(exam) for exam in examinations.list_examinations(principal.user_id)]

    @app.get("/examiner/examinations/{examination_id}")
    def get_examination(examination_id: str, principal=Depends(examiner)):
        with _policy_errors():
            exam = examinations.get_examination(examination_id, principal.user_id)
            entries = examinations.list_examination_questions(examination_id, principal.user_id)
        return {**_examination_body(exam), "questions": [_entry_body(entry) for entry in entries]}

    @app.patch("/examiner/examinations/{examination_id}")
    def update_examination(examination_id: str, payload: ExaminationInput, principal=Depends(examiner)):
        with _policy_errors():
            exam = examinations.update_details(
                examination_id, principal.user_id, title=payload.title,
                description=payload.description, starts_at=_naive_utc(payload.starts_at),
                ends_at=_naive_utc(payload.ends_at),
            )
        return _examination_body(exam)

    @app.post("/examiner/questions", status_code=201)
    def create_question(payload: QuestionInput, principal=Depends(examiner)):
        question = ProgrammingQuestion(str(uuid4()), payload.title, payload.prompt, payload.language, payload.max_score)
        with _policy_errors():
            examinations.create_question(question, principal.user_id)
        return {"question_id": question.question_id, "version": question.version}

    @app.get("/examiner/questions")
    def list_questions(principal=Depends(examiner)):
        return [_question_body(question) for question in examinations.list_questions(principal.user_id)]

    @app.post("/examiner/examinations/{examination_id}/questions", status_code=204)
    def attach_question(examination_id: str, payload: AttachQuestionInput, principal=Depends(examiner)):
        with _policy_errors():
            examinations.attach_question(examination_id, payload.question_id, principal.user_id,
                                         payload.display_order, payload.score_weight)
        return None

    @app.delete("/examiner/examinations/{examination_id}/questions/{question_id}", status_code=204)
    def detach_question(examination_id: str, question_id: str, principal=Depends(examiner)):
        with _policy_errors():
            examinations.detach_question(examination_id, question_id, principal.user_id)
        return None

    @app.post("/examiner/examinations/{examination_id}/transition")
    def transition_examination(examination_id: str, payload: TransitionInput, principal=Depends(examiner)):
        with _policy_errors():
            exam = examinations.transition(examination_id, principal.user_id, payload.target_status)
        return {"examination_id": exam.examination_id, "status": exam.status.value}

    @app.post("/examiner/examinations/{examination_id}/assignments", status_code=201)
    def assign_candidate(examination_id: str, payload: AssignCandidateInput, principal=Depends(examiner)):
        with _policy_errors():
            assignment = sessions.assign_candidate(examination_id, payload.candidate_user_id, principal.user_id)
        return _assignment_body(assignment)

    @app.get("/examiner/examinations/{examination_id}/assignments")
    def list_assignments(examination_id: str, principal=Depends(examiner)):
        with _policy_errors():
            assignments = sessions.list_assignments(examination_id, principal.user_id)
        return [_assignment_body(assignment) for assignment in assignments]

    @app.get("/examiner/examinations/{examination_id}/sessions")
    def list_exam_sessions(examination_id: str, principal=Depends(examiner)):
        with _policy_errors():
            summaries = reviews.list_sessions(examination_id, principal.user_id)
        return [{**_session_body(s.session), "candidate_user_id": s.assignment.candidate_user_id,
                 "marked_questions": s.marked_questions, "total_questions": s.total_questions,
                 "raw_score": s.raw_score, "raw_max": s.raw_max,
                 "weighted_percent": s.weighted_percent}
                for s in summaries]

    @app.get("/examiner/sessions/{session_id}")
    def review_session(session_id: str, principal=Depends(examiner)):
        with _policy_errors():
            review = reviews.get_review(session_id, principal.user_id)
        return {**_session_body(review.session),
                "candidate_user_id": review.assignment.candidate_user_id,
                "examination_id": review.examination.examination_id,
                "release": _release_body(review.release),
                "questions": [{**_entry_body(e),
                               "response": _response_body(review.responses[e.question.question_id])
                               if e.question.question_id in review.responses else None,
                               "mark": _mark_body(review.marks[e.question.question_id])
                               if e.question.question_id in review.marks else None,
                               "mark_history": [_mark_body(m) for m in
                                                review.history.get(e.question.question_id, [])]}
                              for e in review.questions]}

    @app.put("/examiner/sessions/{session_id}/marks/{question_id}")
    def mark_response(session_id: str, question_id: str, payload: MarkInput, principal=Depends(examiner)):
        with _policy_errors():
            mark = reviews.mark(session_id, question_id, principal.user_id, payload.score, payload.comment)
        return _mark_body(mark)

    @app.post("/examiner/examinations/{examination_id}/release")
    def release_results(examination_id: str, principal=Depends(examiner)):
        with _policy_errors():
            release = reviews.release_results(examination_id, principal.user_id)
        return _release_body(release)

    @app.get("/examiner/examinations/{examination_id}/contract")
    def contract_versions(examination_id: str, principal=Depends(examiner)):
        with _policy_errors():
            versions = contracts.list_versions(examination_id, principal.user_id)
        return [_contract_body(contract) for contract in versions]

    @app.put("/examiner/examinations/{examination_id}/contract")
    def save_contract_draft(examination_id: str, payload: ContractInput, principal=Depends(examiner)):
        with _policy_errors():
            contract = contracts.save_draft(examination_id, principal.user_id, payload.declaration(),
                                            payload.amendment_reason)
        return _contract_body(contract)

    @app.post("/examiner/examinations/{examination_id}/contract/amendments", status_code=201)
    def amend_contract(examination_id: str, payload: ContractInput, principal=Depends(examiner)):
        with _policy_errors():
            contract = contracts.amend(examination_id, principal.user_id, payload.declaration(),
                                       payload.amendment_reason or "")
        return _contract_body(contract)

    @app.post("/examiner/examinations/{examination_id}/contract/exceptions", status_code=201)
    def grant_exception(examination_id: str, payload: ExceptionInput, principal=Depends(examiner)):
        with _policy_errors():
            exception = contracts.grant_exception(
                examination_id, principal.user_id, payload.candidate_user_id, payload.reason_category,
                payload.capability_overrides, payload.extra_time_minutes)
        return _exception_body(exception)

    @app.get("/examiner/examinations/{examination_id}/contract/exceptions")
    def list_exceptions(examination_id: str, principal=Depends(examiner)):
        with _policy_errors():
            exceptions = contracts.list_exceptions(examination_id, principal.user_id)
        return [_exception_body(exception) for exception in exceptions]

    candidate = require_roles(Role.CANDIDATE)

    @app.get("/candidate/examinations/{examination_id}/contract")
    def candidate_contract(examination_id: str, principal=Depends(candidate)):
        # Candidates can read the rules in force before and during the exam (spec §9).
        with _policy_errors():
            view = contracts.candidate_view(examination_id, principal.user_id)
        return {**_contract_body(view.contract),
                "my_exceptions": [_exception_body(e) for e in view.exceptions]}

    @app.get("/candidate/ping")
    def candidate_ping(principal=Depends(candidate)):
        return {"status": "ok", "user_id": principal.user_id}

    @app.get("/candidate/examinations")
    def candidate_examinations(principal=Depends(candidate)):
        # Candidates see schedule metadata only; questions appear once a session starts.
        return [{"examination_id": exam.examination_id, "title": exam.title,
                 "status": exam.status.value, "starts_at": _iso(exam.starts_at),
                 "ends_at": _iso(exam.ends_at)}
                for _, exam in sessions.list_candidate_examinations(principal.user_id)]

    @app.post("/candidate/examinations/{examination_id}/session")
    def start_session(examination_id: str, principal=Depends(candidate)):
        with _policy_errors():
            session = sessions.start_session(examination_id, principal.user_id)
        return _session_body(session)

    @app.get("/candidate/sessions/{session_id}")
    def get_session(session_id: str, principal=Depends(candidate)):
        with _policy_errors():
            view = sessions.get_session_view(session_id, principal.user_id)
        return {**_session_body(view.session),
                "examination": {"examination_id": view.examination.examination_id,
                                "title": view.examination.title,
                                "status": view.examination.status.value,
                                "ends_at": _iso(view.examination.ends_at),
                                "my_ends_at": _iso(view.effective_ends_at)},
                "questions": [{"question_id": e.question.question_id, "title": e.question.title,
                               "prompt": e.question.prompt, "language": e.question.language,
                               "display_order": e.display_order,
                               "response": _response_body(view.responses[e.question.question_id])
                               if e.question.question_id in view.responses else None}
                              for e in view.questions]}

    @app.put("/candidate/sessions/{session_id}/responses/{question_id}")
    def save_response(session_id: str, question_id: str, payload: ResponseInput,
                      principal=Depends(candidate)):
        with _policy_errors():
            response = sessions.save_response(session_id, question_id, principal.user_id,
                                              payload.content, payload.base_revision)
        return _response_body(response)

    @app.get("/candidate/sessions/{session_id}/result")
    def candidate_result(session_id: str, principal=Depends(candidate)):
        with _policy_errors():
            result = reviews.candidate_result(session_id, principal.user_id)
        # Candidates see their scores and comments, not who marked or the mark history.
        return {"session_id": result.session.session_id,
                "examination_id": result.examination.examination_id,
                "released_at": _iso(result.release.released_at),
                "raw_score": result.raw_score, "raw_max": result.raw_max,
                "weighted_percent": result.weighted_percent,
                "questions": [{"question_id": e.question.question_id, "title": e.question.title,
                               "max_score": e.question.max_score,
                               "score": result.marks[e.question.question_id].score,
                               "comment": result.marks[e.question.question_id].comment}
                              for e in result.questions]}

    @app.post("/candidate/sessions/{session_id}/submit")
    def submit_session(session_id: str, principal=Depends(candidate)):
        with _policy_errors():
            session = sessions.submit(session_id, principal.user_id)
        return _session_body(session)

    return app
