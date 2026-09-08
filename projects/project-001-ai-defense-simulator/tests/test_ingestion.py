from pathlib import Path

from app.db import Database
from app.ingestion import chunk_text, sha256_bytes


def test_chunking_is_deterministic_and_hashed():
    text = "Alpha paragraph.\n\nBeta paragraph.\n\nGamma paragraph."
    first = chunk_text(text, target_chars=40, overlap_chars=5)
    second = chunk_text(text, target_chars=40, overlap_chars=5)

    assert first == second
    assert first
    assert [chunk.index for chunk in first] == list(range(len(first)))
    assert all(len(chunk.content_hash) == 64 for chunk in first)
    assert all(chunk.locator for chunk in first)


def test_same_bytes_have_same_hash():
    data = b"same source material"
    assert sha256_bytes(data) == sha256_bytes(data)


def test_database_initialization_is_idempotent(tmp_path: Path):
    database = Database(tmp_path / "test.db")
    database.initialize()
    database.initialize()


def test_retrieval_is_workspace_scoped_and_preserves_provenance(tmp_path: Path):
    database = Database(tmp_path / "test.db")
    database.initialize()

    workspace_a = database.create_workspace("A")
    workspace_b = database.create_workspace("B")

    chunks_a = chunk_text("Flood forecasting uses rainfall and river-level evidence.")
    chunks_b = chunk_text("Chess engines search game trees and evaluate positions.")

    database.store_document(
        workspace_id=workspace_a["id"],
        original_filename="flood.md",
        extension=".md",
        content_hash=sha256_bytes(b"a"),
        chunks=chunks_a,
    )
    database.store_document(
        workspace_id=workspace_b["id"],
        original_filename="chess.md",
        extension=".md",
        content_hash=sha256_bytes(b"b"),
        chunks=chunks_b,
    )

    results = database.search(workspace_id=workspace_a["id"], query="rainfall")

    assert len(results) == 1
    result = results[0]
    assert result["filename"] == "flood.md"
    assert result["locator"]
    assert result["document_id"]
    assert "rainfall" in result["text"].lower()

    assert database.search(workspace_id=workspace_a["id"], query="chess") == []
