"""Immutable record primitives for real B2 LLM/RAG baseline runs.

This module records model output; it does not call an LLM.
"""
from dataclasses import dataclass
from hashlib import sha256
import json


@dataclass(frozen=True)
class B2RunRecord:
    run_id: str
    packet_id: str
    packet_hash: str
    provider: str
    model: str
    model_version: str
    executed_at: str
    system_prompt: str
    user_prompt: str
    temperature: str
    seed: str
    raw_response: str


@dataclass(frozen=True)
class AtomicClaim:
    claim_id: str
    run_id: str
    text: str
    claim_type: str
    source_span: str


def b2_run_hash(record: B2RunRecord) -> str:
    payload = record.__dict__
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256(canonical.encode("utf-8")).hexdigest()


def validate_claims(record: B2RunRecord, claims: tuple[AtomicClaim, ...]) -> None:
    seen = set()
    for claim in claims:
        if claim.run_id != record.run_id:
            raise ValueError("Atomic claim belongs to a different B2 run.")
        if not claim.text.strip():
            raise ValueError("Atomic claim text must not be blank.")
        if claim.claim_id in seen:
            raise ValueError("Duplicate atomic claim ID.")
        seen.add(claim.claim_id)
        if claim.source_span and claim.source_span not in record.raw_response:
            raise ValueError("Claim source span must occur verbatim in the preserved raw response.")
