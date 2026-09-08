from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import sqlite3
import uuid


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
