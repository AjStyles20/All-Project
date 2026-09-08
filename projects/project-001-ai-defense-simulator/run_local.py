from __future__ import annotations

import sys

import uvicorn

from app.local_runtime import LocalRuntimeConfigurationError, load_local_runtime_settings


def main() -> int:
    try:
        settings = load_local_runtime_settings()
    except LocalRuntimeConfigurationError as exc:
        print(f"Local configuration error: {exc}", file=sys.stderr)
        return 2

    print(f"Starting Project 001 locally at http://{settings.host}:{settings.port}")
    print("Network boundary: loopback-only local prototype.")
    print(f"External AI providers: {'enabled by server environment' if settings.openai_enabled else 'disabled'}")
    uvicorn.run(
        "app.configured_app:app",
        host=settings.host,
        port=settings.port,
        reload=False,
        access_log=False,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
