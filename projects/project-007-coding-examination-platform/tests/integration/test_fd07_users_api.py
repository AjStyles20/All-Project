from fastapi.testclient import TestClient

from app.api.mysql_platform_api import create_mysql_platform_app
from app.domain.identity import Role
from app.persistence.user_repository import UserRecord
from app.security.passwords import hash_password
from app.services.auth_service import AuthService
from app.services.user_admin_service import UserAdminService
from app.services.login_guard import LoginGuard
from tests.user_fakes import InMemoryLoginThrottleRepository, InMemoryUserRepository


class SessionAuth:
    """Real AuthService password checks over the in-memory repository's session table."""
    def __init__(self, repo):
        self.repo = repo
        self.service = AuthService(repo)

    def login(self, username, password):
        from app.security.passwords import verify_password
        from app.security.tokens import issue_token
        from datetime import datetime, timezone
        from app.services.auth_service import AuthenticationError
        user = self.repo.get_by_username(username.strip().lower())
        if user is None or not user.is_active or not verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid username or password.")
        raw, digest = issue_token()
        self.repo.sessions[digest] = user.user_id
        return raw, datetime.now(timezone.utc)

    def authenticate(self, raw):
        from app.security.tokens import token_digest
        user_id = self.repo.sessions.get(token_digest(raw))
        return None if user_id is None else self.repo.principal_for_user(user_id)

    def logout(self, raw):
        from app.security.tokens import token_digest
        return self.repo.sessions.pop(token_digest(raw), None) is not None


def setup():
    repo = InMemoryUserRepository()
    repo.create(UserRecord("admin-1", "root", hash_password("AdminPassword123"), "Root", True), {Role.ADMINISTRATOR})
    repo.create(UserRecord("lect-1", "lecturer", hash_password("LecturerPass123"), "Lecturer", True), {Role.EXAMINER})
    guard = LoginGuard(InMemoryLoginThrottleRepository())
    client = TestClient(create_mysql_platform_app(auth_service=SessionAuth(repo),
                                                  user_admin_service=UserAdminService(repo, guard), login_guard=guard))
    return client, repo


def sign_in(client, username, password):
    response = client.post("/auth/login", json={"username": username, "password": password})
    assert response.status_code == 200, response.text
    return {"Authorization": "Bearer " + response.json()["access_token"]}


def test_new_user_must_change_password_before_doing_anything_else():
    client, _ = setup()
    admin = sign_in(client, "root", "AdminPassword123")
    created = client.post("/admin/users", json={"username": "Ann", "display_name": "Ann A", "roles": ["CANDIDATE"]}, headers=admin)
    assert created.status_code == 201 and created.headers["cache-control"] == "no-store"
    body = created.json()
    assert body["must_change_password"] and "password_hash" not in body

    ann = sign_in(client, "ann", body["one_time_password"])
    blocked = client.get("/candidate/examinations", headers=ann)
    assert blocked.status_code == 403 and blocked.json()["detail"] == "PASSWORD_CHANGE_REQUIRED"
    assert client.get("/auth/me", headers=ann).json()["must_change_password"] is True

    weak = client.post("/auth/password", json={"current_password": body["one_time_password"], "new_password": "short"}, headers=ann)
    assert weak.status_code == 422
    wrong = client.post("/auth/password", json={"current_password": "not-it", "new_password": "a-long-enough-one"}, headers=ann)
    assert wrong.status_code == 403
    changed = client.post("/auth/password", json={"current_password": body["one_time_password"], "new_password": "a-long-enough-one"}, headers=ann)
    assert changed.status_code == 204
    assert client.get("/auth/me", headers=ann).json()["must_change_password"] is False
    assert client.get("/candidate/ping", headers=ann).status_code == 200
    assert client.post("/auth/login", json={"username": "ann", "password": body["one_time_password"]}).status_code == 401


def test_user_administration_is_administrator_only():
    client, _ = setup()
    lecturer = sign_in(client, "lecturer", "LecturerPass123")
    assert client.get("/admin/users", headers=lecturer).status_code == 403
    assert client.post("/admin/users", json={"username": "x", "display_name": "X", "roles": ["CANDIDATE"]}, headers=lecturer).status_code == 403
    assert client.post("/admin/users/admin-1/password-reset", headers=lecturer).status_code == 403
    assert client.get("/admin/users").status_code == 401


def test_listing_never_exposes_password_material():
    client, _ = setup()
    admin = sign_in(client, "root", "AdminPassword123")
    listed = client.get("/admin/users", headers=admin)
    assert [u["username"] for u in listed.json()] == ["lecturer", "root"]
    assert "hash" not in listed.text and "pbkdf2" not in listed.text


def test_examiner_sees_only_active_candidates_with_minimal_fields():
    client, repo = setup()
    admin = sign_in(client, "root", "AdminPassword123")
    made = client.post("/admin/users", json={"username": "cand", "display_name": "Cand", "roles": ["CANDIDATE"]}, headers=admin).json()
    lecturer = sign_in(client, "lecturer", "LecturerPass123")
    listed = client.get("/examiner/candidates", headers=lecturer).json()
    assert listed == [{"user_id": made["user_id"], "username": "cand", "display_name": "Cand"}]
    assert client.patch(f"/admin/users/{made['user_id']}/active", json={"active": False}, headers=admin).status_code == 204
    assert client.get("/examiner/candidates", headers=lecturer).json() == []


def test_deactivated_user_is_cut_off_immediately_and_lockout_is_refused():
    client, _ = setup()
    admin = sign_in(client, "root", "AdminPassword123")
    lecturer = sign_in(client, "lecturer", "LecturerPass123")
    assert client.patch("/admin/users/lect-1/active", json={"active": False}, headers=admin).status_code == 204
    assert client.get("/examiner/ping", headers=lecturer).status_code == 401
    assert client.post("/auth/login", json={"username": "lecturer", "password": "LecturerPass123"}).status_code == 401
    assert client.patch("/admin/users/admin-1/active", json={"active": False}, headers=admin).status_code == 409
    assert client.put("/admin/users/admin-1/roles", json={"roles": ["EXAMINER"]}, headers=admin).status_code == 409
    assert client.patch("/admin/users/missing/active", json={"active": False}, headers=admin).status_code == 404


def test_role_change_takes_effect_on_the_next_request():
    client, _ = setup()
    admin = sign_in(client, "root", "AdminPassword123")
    lecturer = sign_in(client, "lecturer", "LecturerPass123")
    assert client.get("/examiner/ping", headers=lecturer).status_code == 200
    assert client.put("/admin/users/lect-1/roles", json={"roles": ["CANDIDATE"]}, headers=admin).status_code == 204
    assert client.get("/examiner/ping", headers=lecturer).status_code == 403
    assert client.put("/admin/users/lect-1/roles", json={"roles": []}, headers=admin).status_code == 422
