from pathlib import Path

from fastapi.testclient import TestClient
import pytest

from app import main
from app.db import Database


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    database = Database(tmp_path / "api-test.db")
    database.initialize()
    monkeypatch.setattr(main, "db", database)
    monkeypatch.setattr(main, "MAX_UPLOAD_BYTES", 64)
    monkeypatch.setattr(main, "embedding_provider", None)
    monkeypatch.setattr(main, "question_generator", None)
    monkeypatch.setattr(main, "answer_evaluator", None)
    with TestClient(main.app) as test_client:
        yield test_client


def create_workspace(client: TestClient, name: str = "Verification Workspace") -> str:
    response = client.post("/api/workspaces", data={"name": name})
    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == name
    return payload["id"]


def test_health_reports_ai_semantic_and_evaluation_providers_not_configured(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "application": "available",
        "database": "available",
        "ai_provider": {"status": "not configured", "provider": None, "model": None},
        "semantic_retrieval": {
            "status": "not configured",
            "provider": None,
            "model": None,
        },
        "answer_evaluation": {
            "status": "not configured",
            "provider": None,
            "model": None,
        },
    }


def test_workspace_creation_rejects_blank_name(client: TestClient):
    response = client.post("/api/workspaces", data={"name": "   "})
    assert response.status_code == 422
    assert response.json()["detail"] == "Workspace name is required"


def test_workspace_creation_rejects_excessive_name(client: TestClient):
    response = client.post("/api/workspaces", data={"name": "x" * 121})
    assert response.status_code == 422
    assert response.json()["detail"] == "Workspace name is too long"


def test_valid_markdown_upload_and_search_preserve_provenance(client: TestClient):
    workspace_id = create_workspace(client)
    source = b"Flood forecasting uses rainfall and river-level evidence."

    upload = client.post(
        f"/api/workspaces/{workspace_id}/documents",
        files={"file": ("evidence.md", source, "text/markdown")},
    )
    assert upload.status_code == 200
    document = upload.json()
    assert document["original_filename"] == "evidence.md"
    assert document["workspace_id"] == workspace_id
    assert document["extraction_status"] == "EXTRACTED"
    assert document["chunk_count"] >= 1
    assert len(document["content_hash"]) == 64
    assert document["warnings"] == []

    search = client.get(
        f"/api/workspaces/{workspace_id}/search",
        params={"q": "rainfall"},
    )
    assert search.status_code == 200
    payload = search.json()
    assert payload["workspace_id"] == workspace_id
    assert payload["query"] == "rainfall"
    assert payload["retrieval"]["effective_mode"] == "lexical"
    assert len(payload["results"]) == 1
    result = payload["results"][0]
    assert result["document_id"] == document["id"]
    assert result["filename"] == "evidence.md"
    assert result["locator"]
    assert "rainfall" in result["text"].lower()


def test_hybrid_request_fails_closed_to_explicit_lexical_when_provider_missing(client: TestClient):
    workspace_id = create_workspace(client)
    upload = client.post(
        f"/api/workspaces/{workspace_id}/documents",
        files={"file": ("evidence.md", b"Rainfall evidence for flood review.", "text/markdown")},
    )
    assert upload.status_code == 200

    response = client.get(
        f"/api/workspaces/{workspace_id}/search",
        params={"q": "rainfall", "mode": "hybrid"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["retrieval"] == {
        "requested_mode": "hybrid",
        "effective_mode": "lexical",
        "semantic_status": "not configured",
        "provider": None,
        "model": None,
    }
    assert payload["results"][0]["semantic_similarity"] is None


def test_question_generation_unavailable_without_provider(client: TestClient):
    workspace_id = create_workspace(client)
    response = client.post(
        f"/api/workspaces/{workspace_id}/questions",
        data={"topic": "rainfall", "reviewer_role": "technical"},
    )
    assert response.status_code == 503
    assert response.json()["detail"] == "Question generation is not configured"


def test_answer_evaluation_unavailable_without_provider(client: TestClient):
    workspace_id = create_workspace(client)
    response = client.post(
        f"/api/workspaces/{workspace_id}/questions/not-configured/answers",
        data={"answer": "A bounded answer."},
    )
    assert response.status_code == 503
    assert response.json()["detail"] == "Answer evaluation is not configured"


def test_invalid_search_mode_is_rejected(client: TestClient):
    workspace_id = create_workspace(client)
    response = client.get(
        f"/api/workspaces/{workspace_id}/search",
        params={"q": "rainfall", "mode": "unsafe-mode"},
    )
    assert response.status_code == 422


def test_upload_to_unknown_workspace_returns_404(client: TestClient):
    response = client.post(
        "/api/workspaces/not-a-real-workspace/documents",
        files={"file": ("evidence.md", b"content", "text/markdown")},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Workspace not found"


def test_unsupported_upload_is_rejected(client: TestClient):
    workspace_id = create_workspace(client)
    response = client.post(
        f"/api/workspaces/{workspace_id}/documents",
        files={"file": ("evidence.exe", b"not supported", "application/octet-stream")},
    )
    assert response.status_code == 415
    assert "Unsupported file type" in response.json()["detail"]


def test_excessive_filename_is_rejected(client: TestClient):
    workspace_id = create_workspace(client)
    response = client.post(
        f"/api/workspaces/{workspace_id}/documents",
        files={"file": (("a" * 253) + ".md", b"content", "text/markdown")},
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "Filename is too long"


def test_empty_upload_is_rejected(client: TestClient):
    workspace_id = create_workspace(client)
    response = client.post(
        f"/api/workspaces/{workspace_id}/documents",
        files={"file": ("empty.md", b"", "text/markdown")},
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "File is empty"


def test_invalid_utf8_upload_is_rejected(client: TestClient):
    workspace_id = create_workspace(client)
    response = client.post(
        f"/api/workspaces/{workspace_id}/documents",
        files={"file": ("broken.txt", b"\xff\xfe\xfa", "text/plain")},
    )
    assert response.status_code == 422
    assert response.json()["detail"] == "Text file must contain valid UTF-8"


def test_oversized_upload_is_rejected(client: TestClient):
    workspace_id = create_workspace(client)
    response = client.post(
        f"/api/workspaces/{workspace_id}/documents",
        files={"file": ("large.md", b"a" * 65, "text/markdown")},
    )
    assert response.status_code == 413
    assert response.json()["detail"] == "File exceeds configured upload limit"


def test_search_is_workspace_scoped_through_api(client: TestClient):
    workspace_a = create_workspace(client, "Workspace A")
    workspace_b = create_workspace(client, "Workspace B")

    upload_a = client.post(
        f"/api/workspaces/{workspace_a}/documents",
        files={"file": ("flood.md", b"Rainfall drives this flood example.", "text/markdown")},
    )
    upload_b = client.post(
        f"/api/workspaces/{workspace_b}/documents",
        files={"file": ("chess.md", b"Chess engines evaluate positions.", "text/markdown")},
    )
    assert upload_a.status_code == 200
    assert upload_b.status_code == 200

    response = client.get(
        f"/api/workspaces/{workspace_a}/search",
        params={"q": "chess"},
    )
    assert response.status_code == 200
    assert response.json()["results"] == []
