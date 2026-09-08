from __future__ import annotations

from dataclasses import dataclass
import ipaddress
import os
from pathlib import Path


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
MIN_PORT = 1024
MAX_PORT = 65535


class LocalRuntimeConfigurationError(ValueError):
    pass


@dataclass(frozen=True)
class LocalRuntimeSettings:
    host: str
    port: int
    database_path: Path
    openai_enabled: bool


def _loopback_host(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise LocalRuntimeConfigurationError("local host is required")
    if cleaned.lower() == "localhost":
        return "localhost"
    try:
        address = ipaddress.ip_address(cleaned)
    except ValueError as exc:
        raise LocalRuntimeConfigurationError("local host must be localhost or a loopback IP address") from exc
    if not address.is_loopback:
        raise LocalRuntimeConfigurationError("local launcher refuses non-loopback bind addresses")
    return cleaned


def _port(value: str) -> int:
    try:
        port = int(value)
    except (TypeError, ValueError) as exc:
        raise LocalRuntimeConfigurationError("local port must be an integer") from exc
    if not MIN_PORT <= port <= MAX_PORT:
        raise LocalRuntimeConfigurationError(f"local port must be between {MIN_PORT} and {MAX_PORT}")
    return port


def _provider_enabled() -> bool:
    raw = os.getenv("P001_OPENAI_ENABLED", "0").strip()
    if raw not in {"0", "1"}:
        raise LocalRuntimeConfigurationError("P001_OPENAI_ENABLED must be 0 or 1")
    return raw == "1"


def load_local_runtime_settings() -> LocalRuntimeSettings:
    project_dir = Path(__file__).resolve().parent.parent
    default_db = project_dir / "data" / "project001.db"
    database_path = Path(os.getenv("P001_DATABASE_PATH", str(default_db))).expanduser().resolve()
    return LocalRuntimeSettings(
        host=_loopback_host(os.getenv("P001_LOCAL_HOST", DEFAULT_HOST)),
        port=_port(os.getenv("P001_LOCAL_PORT", str(DEFAULT_PORT))),
        database_path=database_path,
        openai_enabled=_provider_enabled(),
    )
