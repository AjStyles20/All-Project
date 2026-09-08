from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from app import main as runtime
from app.db import Database
from app.evaluation import EvaluationResult, FeedbackItem, FEEDBACK_CATEGORIES, evaluate_and_store_answer
from app.ingestion import chunk_text
from app.session_routes import build_session_router
from app.sessions import FollowUpResult


class Q:
    provider_name = "test"
    model_name = "question"
    model_version = "1"

    def generate(self, request):
        return "Explain how the server preserves evidence provenance before persistence."


class E:
    provider_name = "test"
    model_name = "eval"
    model_version = "1"

    def evaluate(self, request):
        chunk_id = request.evidence[0].chunk_id
        return EvaluationResult(
            "The answer needs a more precise ownership explanation.",
            tuple(
                FeedbackItem(
                    category,
                    "needs_improvement",
                    "Explain the server-side ownership and provenance recheck.",
                    (chunk_id,),
                )
                for category in FEEDBACK_CATEGORIES
            ),
        )


class F:
    provider_name = "test"
    model_name = "followup"
    model_version = "1"

    def generate_follow_up(self, request):
        return FollowUpResult(
            "probe_missing",
            "The prior answer did not explain the authoritative ownership check.",
            "How is workspace ownership revalidated before the follow-up evidence is trusted?",
        )


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    database = Database(tmp_path / "routes.db")
    database.initialize()
    monkeypatch.setattr(runtime, "db", database)
    monkeypatch.setattr(runtime, "question_generator", Q())
    monkeypatch.setattr(runtime, "answer_evaluator", E())

    app = FastAPI()
    app.include_router(build_session_router(runtime, F()))
    with TestClient(app) as test_client:
        yield test_client, database


def seed(database: Database) -> str:
    workspace = database.create_workspace("Defense")
    database.store_document(
        workspace_id=workspace["id"],
        original_filename="source.md",
        extension=".md",
        content_hash="abc",
        chunks=chunk_text("The server revalidates workspace ownership and evidence provenance before persistence."),
    )
    return workspace["id"]


def test_http_session_start_answer_then_followup(client):
    http, database = client
    workspace_id = seed(database)

    started = http.post(
        f"/api/workspaces/{workspace_id}/sessions",
        data={
            "topic": "provenance",
            "reviewer_role": "technical",
            "retrieval_mode": "lexical",
            "max_turns": "3",
        },
    )
    assert started.status_code == 200
    session = started.json()
    assert session["status"] == "active"
    assert len(session["turns"]) == 1
    question_id = session["turns"][0]["question_id"]

    blocked = http.post(f"/api/workspaces/{workspace_id}/sessions/{session['id']}/follow-up")
    assert blocked.status_code == 422

    evaluate_and_store_answer(
        database,
        workspace_id=workspace_id,
        question_id=question_id,
        answer="The server stores source provenance.",
        provider=E(),
    )

    follow_up = http.post(f"/api/workspaces/{workspace_id}/sessions/{session['id']}/follow-up")
    assert follow_up.status_code == 200
    payload = follow_up.json()
    assert payload["turn_index"] == 2
    assert payload["parent_question_id"] == question_id
    assert payload["follow_up_type"] == "probe_missing"

    history = http.get(f"/api/workspaces/{workspace_id}/sessions/{session['id']}")
    assert history.status_code == 200
    assert len(history.json()["turns"]) == 2


def test_session_history_is_workspace_scoped(client):
    http, database = client
    workspace_id = seed(database)
    other = database.create_workspace("Other")["id"]
    started = http.post(
        f"/api/workspaces/{workspace_id}/sessions",
        data={"topic": "provenance", "reviewer_role": "technical", "retrieval_mode": "lexical"},
    )
    assert started.status_code == 200
    session_id = started.json()["id"]

    denied = http.get(f"/api/workspaces/{other}/sessions/{session_id}")
    assert denied.status_code == 404
