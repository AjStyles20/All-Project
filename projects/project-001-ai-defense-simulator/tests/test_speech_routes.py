from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from app import main as runtime
from app.db import Database
from app.ingestion import chunk_text, sha256_bytes
from app.questioning import generate_and_store_question
from app.speech import MAX_AUDIO_BYTES, TranscriptionResult
from app.speech_routes import build_speech_router


class QuestionProvider:
    provider_name = "test"
    model_name = "question"
    model_version = "1"

    def generate(self, request):
        return "How is provenance preserved?"


class SpeechProvider:
    provider_name = "test"
    model_name = "speech"
    model_version = "1"

    def __init__(self):
        self.calls = []

    def transcribe(self, *, audio: bytes, media_type: str):
        self.calls.append((audio, media_type))
        return TranscriptionResult("This transcript must be reviewed before submission.", "en")


def seed(database: Database) -> tuple[str, str]:
    workspace = database.create_workspace("Speech")
    source = "Provenance is revalidated before persistence."
    database.store_document(
        workspace_id=workspace["id"],
        original_filename="source.md",
        extension=".md",
        content_hash=sha256_bytes(source.encode()),
        chunks=chunk_text(source),
    )
    evidence = database.search(workspace_id=workspace["id"], query="provenance", limit=4)
    question = generate_and_store_question(
        database,
        workspace_id=workspace["id"],
        reviewer_role="technical",
        topic="provenance",
        evidence_rows=evidence,
        retrieval_mode="lexical",
        semantic_status="not requested",
        provider=QuestionProvider(),
    )
    return workspace["id"], question["id"]


def make_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, provider):
    database = Database(tmp_path / "speech-routes.db")
    database.initialize()
    monkeypatch.setattr(runtime, "db", database)
    app = FastAPI()
    app.include_router(build_speech_router(runtime, provider))
    return TestClient(app), database


def test_transcription_is_explicitly_unavailable_without_provider(tmp_path, monkeypatch):
    client, database = make_client(tmp_path, monkeypatch, None)
    workspace_id, question_id = seed(database)
    response = client.post(
        f"/api/workspaces/{workspace_id}/questions/{question_id}/transcriptions",
        files={"audio": ("answer.webm", b"audio", "audio/webm")},
    )
    assert response.status_code == 503
    assert response.json()["detail"] == "Speech transcription is not configured"


def test_transcription_returns_reviewable_text_without_submitting_answer_or_audio(tmp_path, monkeypatch):
    provider = SpeechProvider()
    client, database = make_client(tmp_path, monkeypatch, provider)
    workspace_id, question_id = seed(database)

    response = client.post(
        f"/api/workspaces/{workspace_id}/questions/{question_id}/transcriptions",
        files={"audio": ("answer.webm", b"audio", "audio/webm; codecs=opus")},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["transcript"].startswith("This transcript")
    assert payload["submitted_as_answer"] is False
    assert payload["audio_persisted"] is False
    assert provider.calls == [(b"audio", "audio/webm")]

    with database.connect() as connection:
        # Transcription must not create an answer/evaluation row or any audio-storage table.
        eval_table = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='answer_evaluations'"
        ).fetchone()
        if eval_table is not None:
            assert connection.execute("SELECT COUNT(*) FROM answer_evaluations").fetchone()[0] == 0
        assert connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%audio%'"
        ).fetchall() == []


def test_transcription_rejects_wrong_workspace_and_unsupported_type(tmp_path, monkeypatch):
    provider = SpeechProvider()
    client, database = make_client(tmp_path, monkeypatch, provider)
    workspace_id, question_id = seed(database)
    other_id = database.create_workspace("Other")["id"]

    cross = client.post(
        f"/api/workspaces/{other_id}/questions/{question_id}/transcriptions",
        files={"audio": ("answer.webm", b"audio", "audio/webm")},
    )
    assert cross.status_code == 404

    wrong_type = client.post(
        f"/api/workspaces/{workspace_id}/questions/{question_id}/transcriptions",
        files={"audio": ("answer.bin", b"audio", "application/octet-stream")},
    )
    assert wrong_type.status_code == 422
    assert provider.calls == []


def test_transcription_upload_is_bounded_before_provider_call(tmp_path, monkeypatch):
    provider = SpeechProvider()
    client, database = make_client(tmp_path, monkeypatch, provider)
    workspace_id, question_id = seed(database)
    response = client.post(
        f"/api/workspaces/{workspace_id}/questions/{question_id}/transcriptions",
        files={"audio": ("answer.webm", b"x" * (MAX_AUDIO_BYTES + 1), "audio/webm")},
    )
    assert response.status_code == 413
    assert provider.calls == []
