from pathlib import Path

import pytest

from app.db import Database
from app.embeddings import cosine_similarity, embed_checked, validate_vector
from app.ingestion import chunk_text, sha256_bytes
from app.retrieval import hybrid_search


class FakeEmbeddingProvider:
    provider_name = "test-only"
    model_name = "keyword-space"
    model_version = "1"

    def embed(self, texts: list[str]) -> list[list[float]]:
        vectors = []
        for text in texts:
            lowered = text.lower()
            vectors.append([
                float(lowered.count("flood") + lowered.count("rainfall")),
                float(lowered.count("chess") + lowered.count("engine")),
                float(lowered.count("presentation") + lowered.count("defense")),
            ])
        return vectors


class BadDimensionProvider(FakeEmbeddingProvider):
    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[1.0, 2.0] if index == 0 else [1.0, 2.0, 3.0] for index, _ in enumerate(texts)]


def seed(database: Database, workspace_id: str, filename: str, text: str) -> None:
    database.store_document(
        workspace_id=workspace_id,
        original_filename=filename,
        extension=".md",
        content_hash=sha256_bytes(text.encode()),
        chunks=chunk_text(text),
    )


def test_vector_validation_rejects_nonfinite_and_mismatched_dimensions():
    with pytest.raises(ValueError):
        validate_vector([1.0, float("nan")])
    with pytest.raises(ValueError):
        validate_vector([1.0, 2.0], expected_dimension=3)


def test_cosine_similarity_is_bounded_and_dimension_checked():
    assert cosine_similarity([1.0, 0.0], [1.0, 0.0]) == pytest.approx(1.0)
    with pytest.raises(ValueError):
        cosine_similarity([1.0], [1.0, 2.0])


def test_provider_output_dimension_mismatch_fails_safely():
    with pytest.raises(ValueError):
        embed_checked(BadDimensionProvider(), ["a", "b"])


def test_hybrid_search_orders_semantically_related_content_and_exposes_scores(tmp_path: Path):
    database = Database(tmp_path / "hybrid.db")
    database.initialize()
    workspace = database.create_workspace("A")
    seed(database, workspace["id"], "flood.md", "Flood rainfall monitoring and river evidence.")
    seed(database, workspace["id"], "chess.md", "Chess engine search and board evaluation.")

    results, status = hybrid_search(
        database,
        workspace_id=workspace["id"],
        query="flood risk",
        provider=FakeEmbeddingProvider(),
        limit=2,
    )

    assert status.effective_mode == "hybrid"
    assert status.provider == "test-only"
    assert results[0]["filename"] == "flood.md"
    assert results[0]["semantic_similarity"] is not None
    assert results[0]["semantic_position"] == 1
    assert results[0]["hybrid_score"] > 0
    assert results[0]["chunk_id"]
    assert results[0]["document_id"]
    assert results[0]["locator"]


def test_semantic_index_is_workspace_scoped(tmp_path: Path):
    database = Database(tmp_path / "isolation.db")
    database.initialize()
    workspace_a = database.create_workspace("A")
    workspace_b = database.create_workspace("B")
    seed(database, workspace_a["id"], "a.md", "Flood rainfall evidence.")
    seed(database, workspace_b["id"], "b.md", "Flood secret from another workspace.")

    results, _ = hybrid_search(
        database,
        workspace_id=workspace_a["id"],
        query="flood",
        provider=FakeEmbeddingProvider(),
        limit=10,
    )

    assert {item["filename"] for item in results} == {"a.md"}


def test_stale_embedding_is_recomputed_when_content_hash_changes(tmp_path: Path):
    database = Database(tmp_path / "stale.db")
    database.initialize()
    workspace = database.create_workspace("A")
    seed(database, workspace["id"], "a.md", "Flood rainfall evidence.")
    provider = FakeEmbeddingProvider()

    hybrid_search(database, workspace_id=workspace["id"], query="flood", provider=provider)
    identity_rows = database.get_embeddings(
        workspace_id=workspace["id"], provider=provider.provider_name, model=provider.model_name
    )
    assert len(identity_rows) == 1
    chunk_id = identity_rows[0]["chunk_id"]

    with database.connect() as connection:
        connection.execute(
            "UPDATE document_chunks SET text = ?, content_hash = ? WHERE id = ?",
            ("Chess engine evidence.", "changed-hash", chunk_id),
        )

    hybrid_search(database, workspace_id=workspace["id"], query="chess", provider=provider)
    refreshed = database.get_embeddings(
        workspace_id=workspace["id"], provider=provider.provider_name, model=provider.model_name
    )[0]
    assert refreshed["stale"] is False
    assert refreshed["embedding_content_hash"] == "changed-hash"


def test_cross_workspace_embedding_write_is_rejected(tmp_path: Path):
    database = Database(tmp_path / "ownership.db")
    database.initialize()
    workspace_a = database.create_workspace("A")
    workspace_b = database.create_workspace("B")
    seed(database, workspace_a["id"], "a.md", "Flood evidence.")
    chunk = database.list_workspace_chunks(workspace_id=workspace_a["id"])[0]

    with pytest.raises(ValueError):
        database.upsert_embedding(
            workspace_id=workspace_b["id"],
            chunk_id=chunk["chunk_id"],
            content_hash=chunk["content_hash"],
            provider="test-only",
            model="keyword-space",
            model_version="1",
            vector=[1.0, 0.0, 0.0],
        )
