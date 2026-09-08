from __future__ import annotations

from contextlib import contextmanager
import json
from pathlib import Path
import sqlite3
import uuid

from .embeddings import validate_vector


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS workspaces (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS source_documents (
    id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    original_filename TEXT NOT NULL,
    extension TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    extraction_status TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS document_chunks (
    id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    locator TEXT NOT NULL,
    text TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    FOREIGN KEY (document_id) REFERENCES source_documents(id) ON DELETE CASCADE,
    UNIQUE(document_id, chunk_index)
);

CREATE VIRTUAL TABLE IF NOT EXISTS document_chunks_fts USING fts5(
    chunk_id UNINDEXED,
    workspace_id UNINDEXED,
    document_id UNINDEXED,
    filename UNINDEXED,
    locator UNINDEXED,
    text
);

CREATE TABLE IF NOT EXISTS chunk_embeddings (
    chunk_id TEXT NOT NULL,
    workspace_id TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    model_version TEXT,
    dimension INTEGER NOT NULL CHECK (dimension > 0 AND dimension <= 4096),
    vector_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (chunk_id, provider, model),
    FOREIGN KEY (chunk_id) REFERENCES document_chunks(id) ON DELETE CASCADE,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_chunk_embeddings_workspace
ON chunk_embeddings(workspace_id, provider, model);
"""


class Database:
    def __init__(self, path: str | Path) -> None:
        self.path = str(path)

    @contextmanager
    def connect(self):
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(SCHEMA)

    def create_workspace(self, name: str) -> dict:
        workspace_id = str(uuid.uuid4())
        with self.connect() as connection:
            connection.execute(
                "INSERT INTO workspaces (id, name) VALUES (?, ?)",
                (workspace_id, name.strip()),
            )
        return {"id": workspace_id, "name": name.strip()}

    def workspace_exists(self, workspace_id: str) -> bool:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT 1 FROM workspaces WHERE id = ?",
                (workspace_id,),
            ).fetchone()
        return row is not None

    def store_document(
        self,
        *,
        workspace_id: str,
        original_filename: str,
        extension: str,
        content_hash: str,
        chunks,
    ) -> dict:
        document_id = str(uuid.uuid4())
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO source_documents
                    (id, workspace_id, original_filename, extension, content_hash, extraction_status)
                VALUES (?, ?, ?, ?, ?, 'EXTRACTED')
                """,
                (document_id, workspace_id, original_filename, extension, content_hash),
            )

            for chunk in chunks:
                chunk_id = str(uuid.uuid4())
                connection.execute(
                    """
                    INSERT INTO document_chunks
                        (id, document_id, chunk_index, locator, text, content_hash)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        chunk_id,
                        document_id,
                        chunk.index,
                        chunk.locator,
                        chunk.text,
                        chunk.content_hash,
                    ),
                )
                connection.execute(
                    """
                    INSERT INTO document_chunks_fts
                        (chunk_id, workspace_id, document_id, filename, locator, text)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        chunk_id,
                        workspace_id,
                        document_id,
                        original_filename,
                        chunk.locator,
                        chunk.text,
                    ),
                )

        return {
            "id": document_id,
            "workspace_id": workspace_id,
            "original_filename": original_filename,
            "content_hash": content_hash,
            "extraction_status": "EXTRACTED",
            "chunk_count": len(chunks),
        }

    def search(self, *, workspace_id: str, query: str, limit: int = 10) -> list[dict]:
        cleaned = query.strip()
        if not cleaned:
            return []

        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    chunk_id,
                    document_id,
                    filename,
                    locator,
                    text,
                    bm25(document_chunks_fts) AS rank
                FROM document_chunks_fts
                WHERE document_chunks_fts MATCH ?
                  AND workspace_id = ?
                ORDER BY rank ASC
                LIMIT ?
                """,
                (cleaned, workspace_id, limit),
            ).fetchall()

        return [dict(row) for row in rows]

    def list_workspace_chunks(self, *, workspace_id: str, limit: int = 5000) -> list[dict]:
        safe_limit = max(1, min(int(limit), 5000))
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    dc.id AS chunk_id,
                    dc.document_id,
                    sd.original_filename AS filename,
                    dc.locator,
                    dc.text,
                    dc.content_hash
                FROM document_chunks AS dc
                JOIN source_documents AS sd ON sd.id = dc.document_id
                WHERE sd.workspace_id = ?
                ORDER BY sd.created_at ASC, dc.chunk_index ASC
                LIMIT ?
                """,
                (workspace_id, safe_limit),
            ).fetchall()
        return [dict(row) for row in rows]

    def upsert_embedding(
        self,
        *,
        workspace_id: str,
        chunk_id: str,
        content_hash: str,
        provider: str,
        model: str,
        model_version: str | None,
        vector,
    ) -> None:
        values = validate_vector(vector)
        serialized = json.dumps(values, separators=(",", ":"), allow_nan=False)
        with self.connect() as connection:
            owned = connection.execute(
                """
                SELECT 1
                FROM document_chunks AS dc
                JOIN source_documents AS sd ON sd.id = dc.document_id
                WHERE dc.id = ? AND sd.workspace_id = ?
                """,
                (chunk_id, workspace_id),
            ).fetchone()
            if owned is None:
                raise ValueError("chunk does not belong to workspace")

            connection.execute(
                """
                INSERT INTO chunk_embeddings
                    (chunk_id, workspace_id, content_hash, provider, model, model_version,
                     dimension, vector_json, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(chunk_id, provider, model) DO UPDATE SET
                    workspace_id = excluded.workspace_id,
                    content_hash = excluded.content_hash,
                    model_version = excluded.model_version,
                    dimension = excluded.dimension,
                    vector_json = excluded.vector_json,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (
                    chunk_id,
                    workspace_id,
                    content_hash,
                    provider,
                    model,
                    model_version,
                    len(values),
                    serialized,
                ),
            )

    def get_embeddings(
        self,
        *,
        workspace_id: str,
        provider: str,
        model: str,
        limit: int = 5000,
    ) -> list[dict]:
        safe_limit = max(1, min(int(limit), 5000))
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    ce.chunk_id,
                    ce.content_hash AS embedding_content_hash,
                    ce.provider,
                    ce.model,
                    ce.model_version,
                    ce.dimension,
                    ce.vector_json,
                    dc.document_id,
                    sd.original_filename AS filename,
                    dc.locator,
                    dc.text,
                    dc.content_hash AS current_content_hash
                FROM chunk_embeddings AS ce
                JOIN document_chunks AS dc ON dc.id = ce.chunk_id
                JOIN source_documents AS sd ON sd.id = dc.document_id
                WHERE ce.workspace_id = ?
                  AND sd.workspace_id = ?
                  AND ce.provider = ?
                  AND ce.model = ?
                LIMIT ?
                """,
                (workspace_id, workspace_id, provider, model, safe_limit),
            ).fetchall()

        results: list[dict] = []
        for row in rows:
            item = dict(row)
            try:
                raw = json.loads(item.pop("vector_json"))
                item["vector"] = validate_vector(raw, expected_dimension=item["dimension"])
            except (TypeError, ValueError, json.JSONDecodeError) as exc:
                raise ValueError("stored embedding is malformed") from exc
            item["stale"] = item["embedding_content_hash"] != item["current_content_hash"]
            results.append(item)
        return results
