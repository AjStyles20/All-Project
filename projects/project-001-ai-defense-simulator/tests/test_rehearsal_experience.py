from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from app import main as runtime
from app.db import Database
from app.evaluation import EvaluationResult, FeedbackItem, FEEDBACK_CATEGORIES
from app.ingestion import chunk_text
from app.session_routes import build_session_router
from app.sessions import FollowUpResult, reconcile_session_completion


class Q:
    provider_name = "test"
    model_name = "question"
    model_version = "1"

    def generate(self, request):
        return "Explain how authoritative provenance is preserved in this design."


class E:
    provider_name = "test"
    model_name = "evaluation"
    model_version = "1"

    def evaluate(self, request):
        chunk_id = request.evidence[0].chunk_id
        return EvaluationResult(
            "The answer should state the ownership recheck more precisely.",
            tuple(
                FeedbackItem(
                    category,
                    "needs_improvement",
                    "State the server-side workspace ownership and provenance verification.",
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
            "The answer did not explain the authoritative ownership check.",
            "How does the server independently verify workspace ownership before trusting evidence?",
        )


@pytest.fixture()
def rehearsal_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    database = Database(tmp_path / "rehearsal.db")
    database.initialize()
    monkeypatch.setattr(runtime, "db", database)
    monkeypatch.setattr(runtime, "question_generator", Q())
    monkeypatch.setattr(runtime, "answer_evaluator", E())

    app = FastAPI()
    app.include_router(build_session_router(runtime, F()))
    with TestClient(app, follow_redirects=False) as client:
        yield client, database


def seed(database: Database) -> str:
    workspace = database.create_workspace("Defense rehearsal")
    database.store_document(
        workspace_id=workspace["id"],
        original_filename="source.md",
        extension=".md",
        content_hash="f011-source",
        chunks=chunk_text(
            "The server independently validates workspace ownership and source provenance before trusting evidence."
        ),
    )
    return workspace["id"]


def start_session(client: TestClient, workspace_id: str, *, max_turns: int = 3):
    response = client.post(
        f"/api/workspaces/{workspace_id}/sessions",
        data={
            "topic": "provenance",
            "reviewer_role": "technical",
            "retrieval_mode": "lexical",
            "max_turns": str(max_turns),
        },
    )
    assert response.status_code == 200
    return response.json()


def test_web_session_creation_lands_directly_on_first_turn(rehearsal_client):
    client, database = rehearsal_client
    workspace_id = seed(database)
    response = client.post(
        f"/ui/workspaces/{workspace_id}/sessions",
        data={
            "topic": "provenance",
            "reviewer_role": "technical",
            "retrieval_mode": "lexical",
            "max_turns": "3",
        },
    )
    assert response.status_code == 303
    location = response.headers["location"]
    assert f"/workspaces/{workspace_id}/sessions/" in location
    assert "/questions/" in location
    assert "Defense+session+started" in location


def test_session_question_shows_turn_progress_and_session_answer_action(rehearsal_client):
    client, database = rehearsal_client
    workspace_id = seed(database)
    session = start_session(client, workspace_id, max_turns=3)
    question_id = session["current_question_id"]

    response = client.get(
        f"/workspaces/{workspace_id}/sessions/{session['id']}/questions/{question_id}"
    )
    assert response.status_code == 200
    assert "Defense turn 1 of 3" in response.text
    assert f"/ui/workspaces/{workspace_id}/sessions/{session['id']}/questions/{question_id}/answers" in response.text
    assert f"/workspaces/{workspace_id}/sessions/{session['id']}" in response.text


def test_cross_workspace_session_question_url_is_rejected(rehearsal_client):
    client, database = rehearsal_client
    workspace_id = seed(database)
    other = database.create_workspace("Other")["id"]
    session = start_session(client, workspace_id)
    question_id = session["current_question_id"]

    response = client.get(
        f"/workspaces/{other}/sessions/{session['id']}/questions/{question_id}"
    )
    assert response.status_code == 404
    assert "does not belong to this rehearsal session" in response.text


def test_answered_turn_returns_feedback_and_continue_session_link(rehearsal_client):
    client, database = rehearsal_client
    workspace_id = seed(database)
    session = start_session(client, workspace_id, max_turns=3)
    question_id = session["current_question_id"]

    submitted = client.post(
        f"/ui/workspaces/{workspace_id}/sessions/{session['id']}/questions/{question_id}/answers",
        data={"answer": "The server checks workspace ownership and stored provenance before using the evidence."},
    )
    assert submitted.status_code == 303
    assert f"/workspaces/{workspace_id}/sessions/{session['id']}/questions/{question_id}" in submitted.headers["location"]

    page = client.get(
        f"/workspaces/{workspace_id}/sessions/{session['id']}/questions/{question_id}"
    )
    assert page.status_code == 200
    assert "Feedback history" in page.text
    assert "Continue defense session" in page.text


def test_followup_web_action_redirects_directly_to_new_turn(rehearsal_client):
    client, database = rehearsal_client
    workspace_id = seed(database)
    session = start_session(client, workspace_id, max_turns=3)
    question_id = session["current_question_id"]
    client.post(
        f"/ui/workspaces/{workspace_id}/sessions/{session['id']}/questions/{question_id}/answers",
        data={"answer": "It validates provenance."},
    )

    response = client.post(f"/ui/workspaces/{workspace_id}/sessions/{session['id']}/follow-up")
    assert response.status_code == 303
    assert f"/workspaces/{workspace_id}/sessions/{session['id']}/questions/" in response.headers["location"]
    assert "Follow-up+turn+2+generated" in response.headers["location"]


def test_answering_last_allowed_turn_completes_session_without_provider_call(rehearsal_client):
    client, database = rehearsal_client
    workspace_id = seed(database)
    session = start_session(client, workspace_id, max_turns=1)
    question_id = session["current_question_id"]

    response = client.post(
        f"/ui/workspaces/{workspace_id}/sessions/{session['id']}/questions/{question_id}/answers",
        data={"answer": "The server validates ownership and provenance before trusting the evidence."},
    )
    assert response.status_code == 303
    assert "reached+its+turn+limit" in response.headers["location"]

    history = client.get(f"/api/workspaces/{workspace_id}/sessions/{session['id']}")
    assert history.status_code == 200
    assert history.json()["status"] == "complete"

    followup = client.post(f"/api/workspaces/{workspace_id}/sessions/{session['id']}/follow-up")
    assert followup.status_code == 422
    assert followup.json()["detail"] == "Session is complete"


def test_completion_reconciliation_is_idempotent(rehearsal_client):
    client, database = rehearsal_client
    workspace_id = seed(database)
    session = start_session(client, workspace_id, max_turns=1)
    question_id = session["current_question_id"]
    client.post(
        f"/ui/workspaces/{workspace_id}/sessions/{session['id']}/questions/{question_id}/answers",
        data={"answer": "The server checks ownership."},
    )
    first = reconcile_session_completion(database, workspace_id=workspace_id, session_id=session["id"])
    second = reconcile_session_completion(database, workspace_id=workspace_id, session_id=session["id"])
    assert first["status"] == "complete"
    assert second == {"status": "complete", "completed_now": False}
