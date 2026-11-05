"""SQLite store: documents, chunks (with FTS5 search), sessions, questions, answers.

Uploaded content lives only in the database; file names are kept as labels, never used as paths.
"""
import hashlib
import json
import sqlite3
import time
import uuid
from contextlib import contextmanager

SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (id TEXT PRIMARY KEY, name TEXT NOT NULL, sha256 TEXT NOT NULL, uploaded_at REAL NOT NULL);
CREATE TABLE IF NOT EXISTS chunks (id TEXT PRIMARY KEY, document_id TEXT NOT NULL REFERENCES documents ON DELETE CASCADE,
    seq INTEGER NOT NULL, locator TEXT NOT NULL, text TEXT NOT NULL);
CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(text, content='chunks', content_rowid='rowid');
CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, roles TEXT NOT NULL, created_at REAL NOT NULL);
CREATE TABLE IF NOT EXISTS questions (id TEXT PRIMARY KEY, session_id TEXT NOT NULL REFERENCES sessions ON DELETE CASCADE,
    seq INTEGER NOT NULL, role TEXT NOT NULL, category TEXT NOT NULL, text TEXT NOT NULL, chunk_ids TEXT NOT NULL,
    quote TEXT NOT NULL, grounded INTEGER NOT NULL, answer TEXT, feedback TEXT, answered_at REAL);
"""


class Store:
    def __init__(self, path):
        self.path = str(path)
        with self._db() as db:
            db.executescript(SCHEMA)

    @contextmanager
    def _db(self):
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")
        try:
            with db:
                yield db
        finally:
            db.close()

    def add_document(self, name, data: bytes, pieces) -> str:
        doc_id = uuid.uuid4().hex[:12]
        with self._db() as db:
            db.execute("INSERT INTO documents VALUES (?, ?, ?, ?)", (doc_id, name[:200], hashlib.sha256(data).hexdigest(), time.time()))
            for seq, p in enumerate(pieces):
                cid = f"{doc_id}-{seq}"
                cur = db.execute("INSERT INTO chunks (id, document_id, seq, locator, text) VALUES (?, ?, ?, ?, ?)",
                                 (cid, doc_id, seq, p.locator, p.text))
                db.execute("INSERT INTO chunks_fts (rowid, text) VALUES (?, ?)", (cur.lastrowid, p.text))
        return doc_id

    def delete_document(self, doc_id) -> bool:
        with self._db() as db:
            rows = db.execute("SELECT rowid, text FROM chunks WHERE document_id = ?", (doc_id,)).fetchall()
            for r in rows:
                db.execute("INSERT INTO chunks_fts (chunks_fts, rowid, text) VALUES ('delete', ?, ?)", (r["rowid"], r["text"]))
            return db.execute("DELETE FROM documents WHERE id = ?", (doc_id,)).rowcount == 1

    def documents(self):
        with self._db() as db:
            return [dict(r) | {"chunks": db.execute("SELECT COUNT(*) FROM chunks WHERE document_id = ?", (r["id"],)).fetchone()[0]}
                    for r in db.execute("SELECT * FROM documents ORDER BY uploaded_at")]

    def chunks(self):
        with self._db() as db:
            return [dict(r) for r in db.execute(
                "SELECT c.id, c.locator, c.text, d.name AS document FROM chunks c JOIN documents d ON d.id = c.document_id "
                "ORDER BY d.uploaded_at, c.seq")]

    def chunk(self, cid):
        with self._db() as db:
            r = db.execute("SELECT c.id, c.locator, c.text, d.name AS document FROM chunks c "
                           "JOIN documents d ON d.id = c.document_id WHERE c.id = ?", (cid,)).fetchone()
            return dict(r) if r else None

    def search(self, query, limit=10):
        terms = " ".join('"' + t.replace('"', "") + '"' for t in query.split()[:10] if t.strip('"'))
        if not terms:
            return []
        with self._db() as db:
            return [dict(r) for r in db.execute(
                "SELECT c.id, c.locator, d.name AS document, snippet(chunks_fts, 0, '[', ']', ' … ', 12) AS snippet "
                "FROM chunks_fts JOIN chunks c ON c.rowid = chunks_fts.rowid JOIN documents d ON d.id = c.document_id "
                "WHERE chunks_fts MATCH ? ORDER BY bm25(chunks_fts) LIMIT ?", (terms, limit))]

    def create_session(self, roles, questions) -> str:
        sid = uuid.uuid4().hex[:12]
        with self._db() as db:
            db.execute("INSERT INTO sessions VALUES (?, ?, ?)", (sid, json.dumps(roles), time.time()))
            for seq, q in enumerate(questions):
                db.execute("INSERT INTO questions (id, session_id, seq, role, category, text, chunk_ids, quote, grounded) "
                           "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (f"{sid}-{seq}", sid, seq, q.role, q.category, q.text, json.dumps(list(q.chunk_ids)), q.quote, int(q.grounded)))
        return sid

    def session(self, sid):
        with self._db() as db:
            s = db.execute("SELECT * FROM sessions WHERE id = ?", (sid,)).fetchone()
            if not s:
                return None
            qs = [dict(r) | {"chunk_ids": json.loads(r["chunk_ids"]), "feedback": json.loads(r["feedback"] or "[]"),
                             "grounded": bool(r["grounded"])}
                  for r in db.execute("SELECT * FROM questions WHERE session_id = ? ORDER BY seq", (sid,))]
            return {"id": sid, "roles": json.loads(s["roles"]), "created_at": s["created_at"], "questions": qs}

    def sessions(self):
        with self._db() as db:
            return [dict(r) for r in db.execute(
                "SELECT s.id, s.roles, s.created_at, COUNT(q.id) AS questions, COUNT(q.answer) AS answered "
                "FROM sessions s LEFT JOIN questions q ON q.session_id = s.id GROUP BY s.id ORDER BY s.created_at DESC")]

    def question(self, qid):
        with self._db() as db:
            r = db.execute("SELECT * FROM questions WHERE id = ?", (qid,)).fetchone()
            return dict(r) | {"chunk_ids": json.loads(r["chunk_ids"])} if r else None

    def answer(self, qid, text, feedback):
        with self._db() as db:
            db.execute("UPDATE questions SET answer = ?, feedback = ?, answered_at = ? WHERE id = ?",
                       (text, json.dumps(feedback), time.time(), qid))
