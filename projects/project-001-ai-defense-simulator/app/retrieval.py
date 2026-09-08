from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .db import Database
from .embeddings import EmbeddingProvider, cosine_similarity, embed_checked, provider_identity


RRF_K = 60
DEFAULT_LEXICAL_WEIGHT = 0.55
DEFAULT_SEMANTIC_WEIGHT = 0.45
MAX_SEMANTIC_CHUNKS = 1000


@dataclass(frozen=True)
class RetrievalStatus:
    requested_mode: str
    effective_mode: str
    semantic_status: str
    provider: str | None = None
    model: str | None = None


def _validate_weights(lexical_weight: float, semantic_weight: float) -> tuple[float, float]:
    lexical = float(lexical_weight)
    semantic = float(semantic_weight)
    if lexical < 0 or semantic < 0 or lexical + semantic <= 0:
        raise ValueError("retrieval weights must be non-negative and not both zero")
    total = lexical + semantic
    return lexical / total, semantic / total


def ensure_workspace_embeddings(
    database: Database,
    *,
    workspace_id: str,
    provider: EmbeddingProvider,
) -> int:
    identity = provider_identity(provider)
    if not identity.provider or not identity.model:
        raise ValueError("embedding provider identity is incomplete")

    chunks = database.list_workspace_chunks(workspace_id=workspace_id, limit=MAX_SEMANTIC_CHUNKS)
    existing = database.get_embeddings(
        workspace_id=workspace_id,
        provider=identity.provider,
        model=identity.model,
        limit=MAX_SEMANTIC_CHUNKS,
    )
    by_chunk = {item["chunk_id"]: item for item in existing}

    pending = [
        chunk for chunk in chunks
        if chunk["chunk_id"] not in by_chunk
        or by_chunk[chunk["chunk_id"]]["stale"]
        or by_chunk[chunk["chunk_id"]]["model_version"] != identity.version
    ]
    if not pending:
        return 0

    vectors = embed_checked(provider, [chunk["text"] for chunk in pending])
    for chunk, vector in zip(pending, vectors):
        database.upsert_embedding(
            workspace_id=workspace_id,
            chunk_id=chunk["chunk_id"],
            content_hash=chunk["content_hash"],
            provider=identity.provider,
            model=identity.model,
            model_version=identity.version,
            vector=vector,
        )
    return len(pending)


def semantic_search(
    database: Database,
    *,
    workspace_id: str,
    query: str,
    provider: EmbeddingProvider,
    limit: int = 10,
) -> list[dict[str, Any]]:
    identity = provider_identity(provider)
    ensure_workspace_embeddings(database, workspace_id=workspace_id, provider=provider)
    query_vector = embed_checked(provider, [query])[0]
    rows = database.get_embeddings(
        workspace_id=workspace_id,
        provider=identity.provider,
        model=identity.model,
        limit=MAX_SEMANTIC_CHUNKS,
    )

    scored: list[dict[str, Any]] = []
    for row in rows:
        if row["stale"] or row["model_version"] != identity.version:
            continue
        similarity = cosine_similarity(query_vector, row["vector"])
        scored.append(
            {
                "chunk_id": row["chunk_id"],
                "document_id": row["document_id"],
                "filename": row["filename"],
                "locator": row["locator"],
                "text": row["text"],
                "semantic_similarity": similarity,
            }
        )
    scored.sort(key=lambda item: item["semantic_similarity"], reverse=True)
    return scored[: max(1, min(int(limit), 50))]


def hybrid_search(
    database: Database,
    *,
    workspace_id: str,
    query: str,
    provider: EmbeddingProvider | None,
    limit: int = 10,
    lexical_weight: float = DEFAULT_LEXICAL_WEIGHT,
    semantic_weight: float = DEFAULT_SEMANTIC_WEIGHT,
) -> tuple[list[dict[str, Any]], RetrievalStatus]:
    safe_limit = max(1, min(int(limit), 50))
    if provider is None:
        lexical = database.search(workspace_id=workspace_id, query=query, limit=safe_limit)
        for position, item in enumerate(lexical, start=1):
            item["lexical_position"] = position
            item["semantic_similarity"] = None
            item["semantic_position"] = None
            item["hybrid_score"] = None
        return lexical, RetrievalStatus(
            requested_mode="hybrid",
            effective_mode="lexical",
            semantic_status="not configured",
        )

    lexical_weight, semantic_weight = _validate_weights(lexical_weight, semantic_weight)
    candidate_limit = min(50, max(safe_limit * 4, 20))
    lexical = database.search(workspace_id=workspace_id, query=query, limit=candidate_limit)
    semantic = semantic_search(
        database,
        workspace_id=workspace_id,
        query=query,
        provider=provider,
        limit=candidate_limit,
    )

    merged: dict[str, dict[str, Any]] = {}
    for position, item in enumerate(lexical, start=1):
        result = dict(item)
        result["lexical_position"] = position
        result["semantic_similarity"] = None
        result["semantic_position"] = None
        result["hybrid_score"] = lexical_weight / (RRF_K + position)
        merged[item["chunk_id"]] = result

    for position, item in enumerate(semantic, start=1):
        existing = merged.get(item["chunk_id"])
        if existing is None:
            existing = dict(item)
            existing["rank"] = None
            existing["lexical_position"] = None
            existing["hybrid_score"] = 0.0
            merged[item["chunk_id"]] = existing
        existing["semantic_similarity"] = item["semantic_similarity"]
        existing["semantic_position"] = position
        existing["hybrid_score"] += semantic_weight / (RRF_K + position)

    results = sorted(merged.values(), key=lambda item: item["hybrid_score"], reverse=True)[:safe_limit]
    identity = provider_identity(provider)
    return results, RetrievalStatus(
        requested_mode="hybrid",
        effective_mode="hybrid",
        semantic_status="configured",
        provider=identity.provider,
        model=identity.model,
    )
