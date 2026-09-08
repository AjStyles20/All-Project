from __future__ import annotations

import os
import sys

from app.db import Database
from app.local_runtime import LocalRuntimeConfigurationError, load_local_runtime_settings
from app.openai_provider import ProviderConfigurationError, load_openai_settings_from_env


def main() -> int:
    print("Project 001 local self-check")
    try:
        settings = load_local_runtime_settings()
    except LocalRuntimeConfigurationError as exc:
        print(f"FAIL runtime configuration: {exc}")
        return 2

    print(f"PASS loopback bind: {settings.host}:{settings.port}")
    print(f"INFO provider state: {'enabled' if settings.openai_enabled else 'disabled'}")

    db_path = settings.database_path
    try:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        probe = db_path.parent / ".p001-write-probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
    except OSError as exc:
        print(f"FAIL data directory is not writable: {exc}")
        return 3
    print(f"PASS writable data directory: {db_path.parent}")

    try:
        Database(db_path).initialize()
    except Exception as exc:
        print(f"FAIL SQLite initialization: {type(exc).__name__}")
        return 4
    print("PASS canonical SQLite initialization")

    try:
        provider = load_openai_settings_from_env()
    except ProviderConfigurationError as exc:
        print(f"FAIL provider configuration: {exc}")
        return 5
    if provider is None:
        print("PASS external provider remains disabled")
    else:
        print("PASS provider configuration is structurally valid; no external request was made")

    if os.getenv("P001_OPENAI_API_KEY"):
        print("INFO API key is present in the server process environment; value not displayed")

    print("SELF-CHECK PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
