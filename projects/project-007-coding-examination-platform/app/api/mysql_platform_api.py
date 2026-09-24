"""MySQL-backed construction entry point for the full P001 platform."""
from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field
from uuid import uuid4

from app.domain.examination import Examination, ExaminationStatus, ProgrammingQuestion
from app.persistence.mysql_examination_repository import MySQLExaminationRepository
from app.services.examination_service import ExaminationNotFoundError, ExaminationOwnershipError, ExaminationService, InvalidExaminationTransition

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


def create_mysql_platform_app(settings: MySQLSettings | None = None, *, auth_service=None, examination_service=None) -> FastAPI:
    database = MySQLDatabase(settings)
    auth = auth_service or AuthService(MySQLUserRepository(database))
    examinations = examination_service or ExaminationService(MySQLExaminationRepository(database))
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

    @app.post("/examiner/examinations", status_code=201)
    def create_examination(payload: ExaminationInput, principal=Depends(require_roles(Role.EXAMINER, Role.ADMINISTRATOR))):
        exam = Examination(str(uuid4()), payload.title, payload.description, principal.user_id, ExaminationStatus.DRAFT)
        examinations.create_examination(exam)
        return {"examination_id": exam.examination_id, "status": exam.status.value}

    @app.post("/examiner/questions", status_code=201)
    def create_question(payload: QuestionInput, principal=Depends(require_roles(Role.EXAMINER, Role.ADMINISTRATOR))):
        question = ProgrammingQuestion(str(uuid4()), payload.title, payload.prompt, payload.language, payload.max_score)
        examinations.create_question(question, principal.user_id)
        return {"question_id": question.question_id, "version": question.version}

    @app.post("/examiner/examinations/{examination_id}/questions", status_code=204)
    def attach_question(examination_id: str, payload: AttachQuestionInput, principal=Depends(require_roles(Role.EXAMINER, Role.ADMINISTRATOR))):
        try:
            examinations.attach_question(examination_id, payload.question_id, principal.user_id, payload.display_order, payload.score_weight)
        except ExaminationNotFoundError as exc:
            raise HTTPException(status_code=404, detail="Examination not found.") from exc
        except ExaminationOwnershipError as exc:
            raise HTTPException(status_code=403, detail=str(exc)) from exc
        except (InvalidExaminationTransition, LookupError, ValueError) as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        return None

    @app.post("/examiner/examinations/{examination_id}/transition")
    def transition_examination(examination_id: str, payload: TransitionInput, principal=Depends(require_roles(Role.EXAMINER, Role.ADMINISTRATOR))):
        try:
            exam = examinations.transition(examination_id, principal.user_id, payload.target_status)
        except ExaminationNotFoundError as exc:
            raise HTTPException(status_code=404, detail="Examination not found.") from exc
        except ExaminationOwnershipError as exc:
            raise HTTPException(status_code=403, detail=str(exc)) from exc
        except InvalidExaminationTransition as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        return {"examination_id": exam.examination_id, "status": exam.status.value}

    @app.get("/candidate/ping")
    def candidate_ping(principal=Depends(require_roles(Role.CANDIDATE))):
        return {"status": "ok", "user_id": principal.user_id}

    return app
