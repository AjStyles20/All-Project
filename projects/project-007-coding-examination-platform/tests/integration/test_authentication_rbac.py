from fastapi.testclient import TestClient
from app.api.platform_api import create_platform_app
from app.domain.identity import Role
from app.persistence.database import Database
from app.persistence.user_repository import UserRepository
from app.services.auth_service import AuthService

def make_client(tmp_path):
    path = str(tmp_path / "platform.db")
    database = Database(path)
    database.initialize()
    auth = AuthService(UserRepository(database))
    auth.create_user("u-admin", "admin", "AdminPass123!", "Admin", {Role.ADMINISTRATOR})
    auth.create_user("u-candidate", "student", "StudentPass123!", "Student", {Role.CANDIDATE})
    return TestClient(create_platform_app(path))

def login(client, username, password):
    response = client.post("/auth/login", json={"username": username, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]

def test_login_me_and_logout(tmp_path):
    client = make_client(tmp_path)
    token = login(client, "student", "StudentPass123!")
    headers = {"Authorization": "Bearer " + token}
    me = client.get("/auth/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["roles"] == ["CANDIDATE"]
    assert client.post("/auth/logout", headers=headers).status_code == 204
    assert client.get("/auth/me", headers=headers).status_code == 401

def test_role_boundaries(tmp_path):
    client = make_client(tmp_path)
    candidate = {"Authorization": "Bearer " + login(client, "student", "StudentPass123!")}
    admin = {"Authorization": "Bearer " + login(client, "admin", "AdminPass123!")}
    assert client.get("/candidate/ping", headers=candidate).status_code == 200
    assert client.get("/admin/ping", headers=candidate).status_code == 403
    assert client.get("/admin/ping", headers=admin).status_code == 200
    assert client.get("/candidate/ping", headers=admin).status_code == 403

def test_bad_credentials_and_missing_token(tmp_path):
    client = make_client(tmp_path)
    assert client.post("/auth/login", json={"username": "student", "password": "wrong"}).status_code == 401
    assert client.get("/auth/me").status_code == 401
