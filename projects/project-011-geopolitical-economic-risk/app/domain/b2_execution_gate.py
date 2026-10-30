"""Readiness gate for the first real B2 experimental wave.

This module does not execute an LLM. It verifies that the predeclared manifest,
frozen packets, and deterministic prompt serialization still agree.
"""
from dataclasses import dataclass
from app.domain.b2_manifest import B2ExperimentManifest, validate_manifest
from app.domain.b2_prompt import SYSTEM_PROMPT_V1, serialize_packet_for_b2
from app.domain.evidence_packet import ComparativeEvidencePacket, packet_hash


@dataclass(frozen=True)
class B2RunPreparation:
    run_id: str
    packet_id: str
    packet_hash: str
    system_prompt: str
    user_prompt: str


def prepare_run(manifest: B2ExperimentManifest, run_id: str, packet: ComparativeEvidencePacket) -> B2RunPreparation:
    validate_manifest(manifest)
    matches = [r for r in manifest.runs if r.run_id == run_id]
    if len(matches) != 1:
        raise ValueError("Run ID is not uniquely predeclared in the manifest.")
    planned = matches[0]
    actual_hash = packet_hash(packet)
    if planned.packet_id != packet.packet_id:
        raise ValueError("Run is bound to a different packet ID.")
    if planned.packet_hash != actual_hash:
        raise ValueError("Frozen packet hash no longer matches the manifest.")
    return B2RunPreparation(
        run_id=run_id,
        packet_id=packet.packet_id,
        packet_hash=actual_hash,
        system_prompt=SYSTEM_PROMPT_V1,
        user_prompt=serialize_packet_for_b2(packet),
    )
