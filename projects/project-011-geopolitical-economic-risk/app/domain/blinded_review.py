"""Blinding primitives for independent P003 claim review.

These functions prepare reviewer-facing identities without assigning support
labels or exposing baseline identity.
"""
from dataclasses import dataclass
from hashlib import sha256
from typing import Iterable


@dataclass(frozen=True)
class BlindedClaim:
    blind_id: str
    claim_text: str
    claim_type: str


def make_blind_id(experiment_salt: str, claim_id: str) -> str:
    if not experiment_salt.strip() or not claim_id.strip():
        raise ValueError("experiment_salt and claim_id are required")
    digest = sha256(f"{experiment_salt}:{claim_id}".encode("utf-8")).hexdigest()[:16]
    return f"BC-{digest}"


def blind_claims(claims: Iterable, experiment_salt: str) -> tuple[BlindedClaim, ...]:
    result = tuple(
        BlindedClaim(
            blind_id=make_blind_id(experiment_salt, c.claim_id),
            claim_text=c.text,
            claim_type=c.claim_type,
        )
        for c in claims
    )
    ids = [c.blind_id for c in result]
    if len(ids) != len(set(ids)):
        raise ValueError("Blinded claim identity collision")
    return result
