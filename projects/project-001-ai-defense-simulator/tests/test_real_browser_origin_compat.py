from pathlib import Path

from fastapi.testclient import TestClient
import pytest

from app import main as runtime
from app.configured_app import app
from app.db import Database


@pytest.fixture()
def configured_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    database = Database(tmp_path / "browser-origin.db")
    database.initialize()
    monkeypatch.setattr(runtime, "db", database)
    with TestClient(app) as client:
        yield client, database


def test_null_origin_same_origin_browser_form_is_allowed(configured_client):
    client, database = configured_client

    response = client.post(
        "/ui/workspaces",
        data={"name": "Real Browser Compatibility"},
        headers={"Origin": "null", "Sec-Fetch-Site": "same-origin"},
        follow_redirects=False,
    )

    assert response.status_code == 303
    assert response.headers["location"].startswith("/workspaces/")
    with database.connect() as connection:
        count = connection.execute("SELECT COUNT(*) FROM workspaces").fetchone()[0]
    assert count == 1


def test_null_origin_cross_site_browser_form_is_still_rejected(configured_client):
    client, database = configured_client

    response = client.post(
        "/ui/workspaces",
        data={"name": "Must Not Exist"},
        headers={"Origin": "null", "Sec-Fetch-Site": "cross-site"},
        follow_redirects=False,
    )

    assert response.status_code == 403
    with database.connect() as connection:
        count = connection.execute("SELECT COUNT(*) FROM workspaces").fetchone()[0]
    assert count == 0


def test_explicit_foreign_origin_remains_rejected(configured_client):
    client, database = configured_client

    response = client.post(
        "/ui/workspaces",
        data={"name": "Must Not Exist"},
        headers={"Origin": "https://evil.example", "Sec-Fetch-Site": "same-origin"},
        follow_redirects=False,
    )

    assert response.status_code == 403
    with database.connect() as connection:
        count = connection.execute("SELECT COUNT(*) FROM workspaces").fetchone()[0]
    assert count == 0
