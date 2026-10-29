"""Web UI slice 1: static serving, security headers, and the UI's supporting endpoint."""
import re
from pathlib import Path

from fastapi.testclient import TestClient

from app.api.mysql_platform_api import WEB_DIR, create_mysql_platform_app
from tests.integration.test_fd03_candidate_api import FakeAuth, active_exam_client, bearer


def plain_client():
    return TestClient(create_mysql_platform_app(auth_service=FakeAuth()))


def test_root_redirects_to_ui_and_ui_is_served():
    client = plain_client()
    root = client.get("/", follow_redirects=False)
    assert root.status_code in (307, 302) and root.headers["location"] == "/ui/"
    page = client.get("/ui/")
    assert page.status_code == 200 and "<main id=\"main\"" in page.text
    assert client.get("/ui/app.js").status_code == 200
    assert client.get("/ui/app.css").status_code == 200


def test_ui_responses_carry_strict_security_headers():
    page = plain_client().get("/ui/")
    csp = page.headers["content-security-policy"]
    assert "script-src 'self'" in csp and "frame-ancestors 'none'" in csp and "object-src 'none'" in csp
    assert "unsafe-inline" not in csp and "unsafe-eval" not in csp
    assert page.headers["x-content-type-options"] == "nosniff"
    assert page.headers["cache-control"] == "no-store"


def test_ui_has_no_inline_script_or_style_and_no_html_sinks():
    # The CSP forbids inline code, so the page must not depend on any.
    html = (WEB_DIR / "index.html").read_text(encoding="utf-8")
    assert not re.search(r"<script(?![^>]*\bsrc=)", html)
    assert "style=" not in html and "<style" not in html and "onclick=" not in html
    script = (WEB_DIR / "app.js").read_text(encoding="utf-8")
    for sink in ("innerHTML", "outerHTML", "insertAdjacentHTML", "eval(", "new Function", "document.write"):
        assert sink not in script


def test_find_session_does_not_start_one():
    client, eid, _ = active_exam_client()
    student = bearer("student-token")
    assert client.get(f"/candidate/examinations/{eid}/session", headers=student).status_code == 404
    started = client.post(f"/candidate/examinations/{eid}/session", headers=student).json()
    found = client.get(f"/candidate/examinations/{eid}/session", headers=student).json()
    assert found["session_id"] == started["session_id"]
    assert client.get(f"/candidate/examinations/{eid}/session", headers=bearer("student2-token")).status_code == 404


def test_api_responses_are_not_affected_by_ui_headers():
    response = plain_client().get("/health")
    assert "content-security-policy" not in response.headers
