"""Non-experimental qualification test for the OpenAI B2 execution route.

This command MUST NOT use a B2 run ID, evidence packet, frozen B2 prompt, or
experimental case. Its only purpose is to establish that the provider route can
return a response with the provenance fields required before experimental runs
are consumed.
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone

from openai import OpenAI


QUALIFICATION_INPUT = (
    "This is a non-experimental connectivity and provenance qualification. "
    "Reply with exactly: P003_ROUTE_OK"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set.")

    client = OpenAI()
    started = datetime.now(timezone.utc).isoformat()
    try:
        response = client.responses.create(model=args.model, input=QUALIFICATION_INPUT)
    except Exception as exc:
        print(json.dumps({
            "qualification": "P003_OPENAI_ROUTE_V1",
            "experimental_run_consumed": False,
            "provider": "OpenAI",
            "requested_model": args.model,
            "attempt_started_utc": started,
            "status": "FAILED",
            "error_type": type(exc).__name__,
            "error": str(exc),
        }, indent=2, ensure_ascii=False))
        raise

    raw = response.output_text
    record = {
        "qualification": "P003_OPENAI_ROUTE_V1",
        "experimental_run_consumed": False,
        "provider": "OpenAI",
        "requested_model": args.model,
        "returned_model": getattr(response, "model", None),
        "provider_response_id": getattr(response, "id", None),
        "attempt_started_utc": started,
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "qualification_input": QUALIFICATION_INPUT,
        "raw_response": raw,
        "expected_exact_response": "P003_ROUTE_OK",
        "response_matches_expected": raw.strip() == "P003_ROUTE_OK",
        "status": "QUALIFIED" if (
            getattr(response, "id", None)
            and getattr(response, "model", None)
            and raw.strip() == "P003_ROUTE_OK"
        ) else "NOT_QUALIFIED",
    }
    print(json.dumps(record, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
