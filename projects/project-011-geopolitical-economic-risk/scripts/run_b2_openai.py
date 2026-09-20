"""Controlled external B2 runner.

This script executes only predeclared B2 runs after the repository's readiness
gate prepares the frozen prompts. It deliberately reads OPENAI_API_KEY from the
environment and never stores the key.

Run from the P003 project directory after installing the official OpenAI SDK:
    python -m pip install openai
    python scripts/run_b2_openai.py B2-A-001 --model <model-id>

A successful provider response is printed as JSON to stdout. Redirect it to a
file if desired. Do not edit the frozen prompt/packet/manifest to improve an
observed result.
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone

from openai import OpenAI

from app.domain.b2_execution_gate import prepare_run
from app.domain.evidence_packet import packet_hash
from app.fixtures.b2_experiment_manifest_v1 import B2_EXPERIMENT_MANIFEST_V1
from app.fixtures.candidate_a_packet import CANDIDATE_A_PACKET_V1
from app.fixtures.nc01_packet import NC01_PACKET_V1


def packet_for(run_id: str):
    if run_id.startswith("B2-A-"):
        return CANDIDATE_A_PACKET_V1
    if run_id.startswith("B2-NC01-"):
        return NC01_PACKET_V1
    raise ValueError("This runner is frozen to the six first-wave B2 run IDs.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_id")
    parser.add_argument("--model", required=True)
    args = parser.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set.")

    manifest = B2_EXPERIMENT_MANIFEST_V1
    packet = packet_for(args.run_id)
    prepared = prepare_run(manifest=manifest, run_id=args.run_id, packet=packet)

    client = OpenAI()
    started = datetime.now(timezone.utc).isoformat()
    try:
        response = client.responses.create(
            model=args.model,
            input=[
                {"role": "system", "content": prepared.system_prompt},
                {"role": "user", "content": prepared.user_prompt},
            ],
        )
    except Exception as exc:
        failure = {
            "run_id": args.run_id,
            "packet_id": packet.packet_id,
            "packet_hash": packet_hash(packet),
            "provider": "OpenAI",
            "requested_model": args.model,
            "attempt_started_utc": started,
            "status": "TECHNICAL_FAILURE",
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
        print(json.dumps(failure, indent=2, ensure_ascii=False))
        raise

    record = {
        "run_id": args.run_id,
        "packet_id": packet.packet_id,
        "packet_hash": packet.packet_hash,
        "provider": "OpenAI",
        "requested_model": args.model,
        "returned_model": getattr(response, "model", None),
        "provider_response_id": getattr(response, "id", None),
        "attempt_started_utc": started,
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "system_prompt": prepared.system_prompt,
        "user_prompt": prepared.user_prompt,
        "raw_response": response.output_text,
        "status": "SUCCESS",
    }
    print(json.dumps(record, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
