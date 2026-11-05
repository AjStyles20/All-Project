"""Local store: SQLite metadata plus one encrypted image file per kept frame.

Images are encrypted with the injected protector before they touch disk. Every delete path
removes the database row and the file together.
"""
import os
import sqlite3
import threading
import time
import uuid
from contextlib import contextmanager
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS frames (
    frame_id TEXT PRIMARY KEY, captured_at REAL NOT NULL, app TEXT NOT NULL, title TEXT NOT NULL,
    text TEXT NOT NULL DEFAULT '', size_bytes INTEGER NOT NULL, departure INTEGER NOT NULL DEFAULT 0);
CREATE INDEX IF NOT EXISTS frames_time ON frames (captured_at);
CREATE TABLE IF NOT EXISTS counters (name TEXT PRIMARY KEY, value INTEGER NOT NULL);
"""

DAY = 86400


class Store:
    def __init__(self, folder, protector, retention_days=7, max_bytes=2 * 1024 ** 3):
        self.folder = Path(folder)
        self.images = self.folder / "frames"
        self.images.mkdir(parents=True, exist_ok=True)
        self.db_path = self.folder / "memory.sqlite3"
        self.protector = protector
        self.retention_days = retention_days
        self.max_bytes = max_bytes
        self._lock = threading.Lock()
        with self._connect() as db:
            db.executescript(SCHEMA)

    @contextmanager
    def _connect(self):
        db = sqlite3.connect(self.db_path)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    # ---- writing ----

    def add(self, image_bytes: bytes, app: str, title: str, captured_at: float, text: str = "",
            departure: bool = False) -> str:
        frame_id = uuid.uuid4().hex
        sealed = self.protector.protect(image_bytes)
        path = self.images / f"{frame_id}.bin"
        with self._lock:
            path.write_bytes(sealed)
            try:
                with self._connect() as db:
                    db.execute("INSERT INTO frames VALUES (?, ?, ?, ?, ?, ?, ?)",
                               (frame_id, captured_at, app, title, text, len(sealed), int(departure)))
            except Exception:
                path.unlink(missing_ok=True)
                raise
        return frame_id

    def count_skip(self, name: str) -> None:
        with self._connect() as db:
            db.execute("INSERT INTO counters VALUES (?, 1) ON CONFLICT DO UPDATE SET value = value + 1", (name,))

    # ---- reading ----

    def image(self, frame_id: str) -> bytes | None:
        if not _is_id(frame_id):
            return None
        path = self.images / f"{frame_id}.bin"
        if not path.exists():
            return None
        return self.protector.unprotect(path.read_bytes())

    def search(self, query: str = "", limit: int = 200) -> list[dict]:
        with self._connect() as db:
            if query:
                like = "%" + query.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"
                rows = db.execute("SELECT * FROM frames WHERE title LIKE ? ESCAPE '\\' OR app LIKE ? ESCAPE '\\' "
                                  "OR text LIKE ? ESCAPE '\\' ORDER BY captured_at DESC LIMIT ?",
                                  (like, like, like, limit))
            else:
                rows = db.execute("SELECT * FROM frames ORDER BY captured_at DESC LIMIT ?", (limit,))
            return [dict(r) for r in rows]

    def stats(self) -> dict:
        with self._connect() as db:
            n, size = db.execute("SELECT COUNT(*), COALESCE(SUM(size_bytes), 0) FROM frames").fetchone()
            skipped = {r["name"]: r["value"] for r in db.execute("SELECT * FROM counters")}
        return {"frames": n, "bytes": size, "skipped": skipped,
                "retention_days": self.retention_days, "max_bytes": self.max_bytes}

    # ---- deleting ----

    def _delete_where(self, where: str, params=()) -> int:
        with self._lock:
            with self._connect() as db:
                ids = [r[0] for r in db.execute(f"SELECT frame_id FROM frames WHERE {where}", params)]
                db.executemany("DELETE FROM frames WHERE frame_id = ?", [(i,) for i in ids])
            for i in ids:
                (self.images / f"{i}.bin").unlink(missing_ok=True)
        return len(ids)

    def delete(self, frame_id: str) -> int:
        return self._delete_where("frame_id = ?", (frame_id,)) if _is_id(frame_id) else 0

    def delete_since(self, seconds: float, now: float | None = None) -> int:
        return self._delete_where("captured_at >= ?", ((now or time.time()) - seconds,))

    def delete_all(self) -> int:
        removed = self._delete_where("1 = 1")
        # Also catch any file left behind by a crash between file write and row insert.
        for leftover in self.images.glob("*.bin"):
            leftover.unlink(missing_ok=True)
        with self._connect() as db:
            db.execute("DELETE FROM counters")
        return removed

    def enforce_limits(self, now: float | None = None) -> int:
        now = now or time.time()
        removed = self._delete_where("captured_at < ?", (now - self.retention_days * DAY,))
        with self._connect() as db:
            rows = db.execute("SELECT frame_id, size_bytes FROM frames ORDER BY captured_at DESC").fetchall()
        total, over = 0, []
        for r in rows:
            total += r["size_bytes"]
            if total > self.max_bytes:
                over.append(r["frame_id"])
        for frame_id in over:
            removed += self.delete(frame_id)
        return removed


def _is_id(value: str) -> bool:
    # Frame ids are uuid4 hex; anything else could be a path trick.
    return len(value) == 32 and all(c in "0123456789abcdef" for c in value)


def default_folder() -> Path:
    base = os.environ.get("LOCALAPPDATA") or str(Path.home() / ".local" / "share")
    return Path(base) / "P009ScreenMemory"
