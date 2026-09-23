"""MySQL-backed construction entry point for the full P001 platform."""
from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

from app.domain.identity import Role
from app.persistence.mysql_database import MySQLDatabase, MySQLSettings
from app.persistence.mysql_user_repository import MySQLUserRepository
from app.services.auth_service import AuthenticationError, AuthService


class LoginInput(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


def create_mysql_platform_app(settings: MySQLSettings | None = None) -> FastAPI:
    database = MySQLDatabase(settings)
    auth = AuthService(MySQLUserRepository(database))
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

    @app.get("/candidate/ping")
    def candidate_ping(principal=Depends(require_roles(Role.CANDIDATE))):
        return {"status": "ok", "user_id": principal.user_id}

    return app
