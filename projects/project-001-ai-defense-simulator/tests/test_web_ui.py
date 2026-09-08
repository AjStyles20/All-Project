from pathlib import Path

from fastapi.testclient import TestClient
import pytest

from app import main
from app.db import Database
from app.evaluation import FEEDBACK_CATEGORIES, EvaluationResult, FeedbackItem


class FakeQuestionGenerator:
    provider_name = "test-only"
    model_name = "question-ui-fixture"
    model_version = "1"

    def generate(self, request):
        return "What evidence supports the rainfall threshold used in this project?"


class FakeAnswerEvaluator:
    provider_name = "test-only"
    model_name = "evaluation-ui-fixture"
    model_version = "1"

    def evaluate(self, request):
        evidence_id = request.evidence[0].chunk_id
        return EvaluationResult(
            summary="The answer is grounded in the supplied evidence.",
            feedback=tuple(
                FeedbackItem(
                    category=category,
                    status="adequate",
                    explanation=f"Feedback for {category} uses the source evidence.",
                    evidence_chunk_ids=(evidence_id,),
                )
                for category in FEEDBACK_CATEGORIES
            ),
        )


@pytest.fixture()
def ui_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    database = Database(tmp_path / "ui.db")
    database.initialize()
    monkeypatch.setattr(main, "db", database)
    monkeypatch.setattr(main, "MAX_UPLOAD_BYTES", 4096)
    monkeypatch.setattr(main, "embedding_provider", None)
    monkeypatch.setattr(main, "question_generator", None)
    monkeypatch.setattr(main, "answer_evaluator", None)
    with TestClient(main.app) as client:
        yield client, database


def create_workspace_via_ui(client: TestClient, name: str = "UI Workspace") -> str:
    response = client.post(
        "/ui/workspaces",
        data={"name": name},
        follow_redirects=False,
    )
    assert response.status_code == 303
    location = response.headers["location"]
    assert location.startswith("/workspaces/")
    return location.split("/workspaces/", 1)[1].split("?", 1)[0]


def test_home_renders_security_headers_and_truthful_capability_state(ui_client):
    client, _ = ui_client
    response = client.get("/")

    assert response.status_code == 200
    assert "Prepare for a defense" in response.text
    assert "No questions will be fabricated while unconfigured." in response.text
    assert "No AI feedback will be fabricated while unconfigured." in response.text
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert "default-src 'self'" in response.headers["content-security-policy"]
    assert "frame-ancestors 'none'" in response.headers["content-security-policy"]
    assert response.headers["cache-control"] == "no-store"


def test_api_docs_are_disabled_by_default(ui_client):
    client, _ = ui_client
    response = client.get("/docs")
    assert response.status_code == 404


def test_cross_origin_browser_mutation_is_rejected(ui_client):
    client, database = ui_client
    response = client.post(
        "/ui/workspaces",
        data={"name": "Should Not Exist"},
        headers={"Origin": "https://evil.example", "Sec-Fetch-Site": "cross-site"},
        follow_redirects=False,
    )
    assert response.status_code == 403
    with database.connect() as connection:
        count = connection.execute("SELECT COUNT(*) FROM workspaces").fetchone()[0]
    assert count == 0


def test_workspace_creation_and_upload_work_through_web_forms(ui_client):
    client, _ = ui_client
    workspace_id = create_workspace_via_ui(client)

    upload = client.post(
        f"/ui/workspaces/{workspace_id}/documents",
        files={"file": ("evidence.md", b"Rainfall evidence for a defense.", "text/markdown")},
        follow_redirects=False,
    )
    assert upload.status_code == 303

    page = client.get(f"/workspaces/{workspace_id}")
    assert page.status_code == 200
    assert "evidence.md" in page.text
    assert "Question generation is not configured" in page.text


def test_uploaded_script_like_text_is_escaped_in_search_results(ui_client):
    client, _ = ui_client
    workspace_id = create_workspace_via_ui(client)
    malicious = b"<script>alert(1)</script> rainfall evidence remains data, not executable markup."
    upload = client.post(
        f"/ui/workspaces/{workspace_id}/documents",
        files={"file": ("malicious.md", malicious, "text/markdown")},
        follow_redirects=False,
    )
    assert upload.status_code == 303

    page = client.get(
        f"/workspaces/{workspace_id}",
        params={"q": "rainfall", "mode": "lexical"},
    )
    assert page.status_code == 200
    assert "<script>alert(1)</script>" not in page.text
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in page.text
    assert "malicious.md" in page.text
    assert "paragraph 1" in page.text


def test_full_server_rendered_question_answer_feedback_loop_with_test_providers(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    database = Database(tmp_path / "ui-loop.db")
    database.initialize()
    monkeypatch.setattr(main, "db", database)
    monkeypatch.setattr(main, "MAX_UPLOAD_BYTES", 4096)
    monkeypatch.setattr(main, "embedding_provider", None)
    monkeypatch.setattr(main, "question_generator", FakeQuestionGenerator())
    monkeypatch.setattr(main, "answer_evaluator", FakeAnswerEvaluator())

    with TestClient(main.app) as client:
        workspace_id = create_workspace_via_ui(client, "Full Loop")
        upload = client.post(
            f"/ui/workspaces/{workspace_id}/documents",
            files={
                "file": (
                    "evidence.md",
                    b"Rainfall threshold evidence is derived from river-level observations.",
                    "text/markdown",
                )
            },
            follow_redirects=False,
        )
        assert upload.status_code == 303

        question = client.post(
            f"/ui/workspaces/{workspace_id}/questions",
            data={
                "topic": "rainfall",
                "reviewer_role": "evidence",
                "retrieval_mode": "lexical",
            },
            follow_redirects=False,
        )
        assert question.status_code == 303
        question_path = question.headers["location"].split("?", 1)[0]
        assert f"/workspaces/{workspace_id}/questions/" in question_path

        question_page = client.get(question_path)
        assert question_page.status_code == 200
        assert "What evidence supports the rainfall threshold" in question_page.text
        assert "evidence.md" in question_page.text

        answer = client.post(
            f"/ui{question_path}/answers",
            data={
                "answer": "The threshold is supported by the rainfall and river-level observations in the source material."
            },
            follow_redirects=False,
        )
        assert answer.status_code == 303

        feedback_page = client.get(question_path)
        assert feedback_page.status_code == 200
        assert "The answer is grounded in the supplied evidence." in feedback_page.text
        assert "source content correctness" in feedback_page.text
        assert "No validated objective overall grade is claimed." in feedback_page.text


def test_question_cannot_be_read_through_another_workspace_url(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    database = Database(tmp_path / "ui-isolation.db")
    database.initialize()
    monkeypatch.setattr(main, "db", database)
    monkeypatch.setattr(main, "MAX_UPLOAD_BYTES", 4096)
    monkeypatch.setattr(main, "embedding_provider", None)
    monkeypatch.setattr(main, "question_generator", FakeQuestionGenerator())
    monkeypatch.setattr(main, "answer_evaluator", FakeAnswerEvaluator())

    with TestClient(main.app) as client:
        workspace_a = create_workspace_via_ui(client, "A")
        workspace_b = create_workspace_via_ui(client, "B")
        client.post(
            f"/ui/workspaces/{workspace_a}/documents",
            files={"file": ("a.md", b"Rainfall evidence for A.", "text/markdown")},
            follow_redirects=False,
        )
        generated = client.post(
            f"/ui/workspaces/{workspace_a}/questions",
            data={"topic": "rainfall", "reviewer_role": "technical", "retrieval_mode": "lexical"},
            follow_redirects=False,
        )
        question_id = generated.headers["location"].split("/questions/", 1)[1].split("?", 1)[0]

        wrong_workspace = client.get(f"/workspaces/{workspace_b}/questions/{question_id}")
        assert wrong_workspace.status_code == 404
        assert "What evidence supports the rainfall threshold" not in wrong_workspace.text
