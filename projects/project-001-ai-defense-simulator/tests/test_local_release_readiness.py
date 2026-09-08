from __future__ import annotations

from pathlib import Path
import sqlite3

import pytest

from app.db import Database
from app.local_runtime import LocalRuntimeConfigurationError, load_local_runtime_settings
from backup_database import create_backup
import self_check


def clear_local_env(monkeypatch):
    for name in (
        "P001_LOCAL_HOST",
        "P001_LOCAL_PORT",
        "P001_DATABASE_PATH",
        "P001_OPENAI_ENABLED",
        "P001_OPENAI_API_KEY",
    ):
        monkeypatch.delenv(name, raising=False)


def test_local_runtime_defaults_to_loopback_and_provider_disabled(monkeypatch):
    clear_local_env(monkeypatch)
    settings = load_local_runtime_settings()
    assert settings.host == "127.0.0.1"
    assert settings.port == 8000
    assert settings.openai_enabled is False


@pytest.mark.parametrize("host", ["0.0.0.0", "192.168.1.20", "8.8.8.8", "example.com"])
def test_local_launcher_rejects_non_loopback_host(monkeypatch, host):
    clear_local_env(monkeypatch)
    monkeypatch.setenv("P001_LOCAL_HOST", host)
    with pytest.raises(LocalRuntimeConfigurationError):
        load_local_runtime_settings()


@pytest.mark.parametrize("host", ["127.0.0.1", "127.0.0.2", "::1", "localhost"])
def test_local_launcher_accepts_loopback_hosts(monkeypatch, host):
    clear_local_env(monkeypatch)
    monkeypatch.setenv("P001_LOCAL_HOST", host)
    assert load_local_runtime_settings().host == host


@pytest.mark.parametrize("port", ["0", "80", "1023", "65536", "abc"])
def test_local_launcher_rejects_unsafe_or_invalid_ports(monkeypatch, port):
    clear_local_env(monkeypatch)
    monkeypatch.setenv("P001_LOCAL_PORT", port)
    with pytest.raises(LocalRuntimeConfigurationError):
        load_local_runtime_settings()


def test_invalid_provider_toggle_fails_closed(monkeypatch):
    clear_local_env(monkeypatch)
    monkeypatch.setenv("P001_OPENAI_ENABLED", "yes")
    with pytest.raises(LocalRuntimeConfigurationError):
        load_local_runtime_settings()


def test_self_check_does_not_print_api_key(monkeypatch, tmp_path, capsys):
    clear_local_env(monkeypatch)
    secret = "sk-test-secret-never-print-this"
    monkeypatch.setenv("P001_DATABASE_PATH", str(tmp_path / "local.db"))
    monkeypatch.setenv("P001_OPENAI_ENABLED", "1")
    monkeypatch.setenv("P001_OPENAI_API_KEY", secret)
    assert self_check.main() == 0
    output = capsys.readouterr().out
    assert secret not in output
    assert "no external request was made" in output
    assert "SELF-CHECK PASS" in output


def test_self_check_initializes_canonical_database_without_probe_table(monkeypatch, tmp_path):
    clear_local_env(monkeypatch)
    db_path = tmp_path / "local.db"
    monkeypatch.setenv("P001_DATABASE_PATH", str(db_path))
    assert self_check.main() == 0
    with sqlite3.connect(db_path) as connection:
        names = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert "workspaces" in names
    assert "local_self_check" not in names


def test_backup_uses_valid_sqlite_copy(tmp_path):
    source = tmp_path / "source.db"
    database = Database(source)
    database.initialize()
    workspace = database.create_workspace("Backup me")

    destination = create_backup(source, tmp_path / "backups")
    assert destination.exists()
    assert destination != source
    with sqlite3.connect(destination) as connection:
        row = connection.execute("SELECT name FROM workspaces WHERE id = ?", (workspace["id"],)).fetchone()
        integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
    assert row[0] == "Backup me"
    assert integrity == "ok"


def test_secret_and_runtime_artifacts_are_gitignored():
    ignore = Path(".gitignore").read_text(encoding="utf-8")
    assert ".env\n" in ignore
    assert "!.env.example" in ignore
    assert "*.db" in ignore
    assert "backups/" in ignore
    assert "data/" in ignore


def test_environment_example_contains_no_credential():
    example = Path(".env.example").read_text(encoding="utf-8")
    assert "P001_OPENAI_ENABLED=0" in example
    assert "P001_LOCAL_HOST=127.0.0.1" in example
    assert "P001_OPENAI_API_KEY=" in example
    assert "sk-" not in example


def test_supported_launcher_has_no_reload_and_no_public_bind():
    script = Path("run_local.py").read_text(encoding="utf-8")
    assert "reload=False" in script
    assert 'host=settings.host' in script
    assert '"0.0.0.0"' not in script
