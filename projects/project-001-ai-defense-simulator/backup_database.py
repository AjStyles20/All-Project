from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import sqlite3
import sys

from app.local_runtime import LocalRuntimeConfigurationError, load_local_runtime_settings


def create_backup(source: Path, destination_dir: Path) -> Path:
    if not source.exists() or not source.is_file():
        raise FileNotFoundError("database file does not exist")
    destination_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    destination = destination_dir / f"project001-{stamp}.db"
    if destination.exists():
        raise FileExistsError("backup destination already exists")
    with sqlite3.connect(source) as source_db, sqlite3.connect(destination) as backup_db:
        source_db.backup(backup_db)
        result = backup_db.execute("PRAGMA integrity_check").fetchone()
        if result is None or result[0] != "ok":
            raise sqlite3.DatabaseError("backup integrity check failed")
    return destination


def main() -> int:
    try:
        settings = load_local_runtime_settings()
        project_dir = Path(__file__).resolve().parent
        destination = create_backup(settings.database_path, project_dir / "backups")
    except (LocalRuntimeConfigurationError, OSError, sqlite3.Error) as exc:
        print(f"Backup failed: {exc}", file=sys.stderr)
        return 2
    print(f"Backup created: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
