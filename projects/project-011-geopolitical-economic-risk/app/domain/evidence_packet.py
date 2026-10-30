"""Frozen comparative evidence-packet primitives."""
from dataclasses import dataclass
from hashlib import sha256
import json


@dataclass(frozen=True)
class PacketEvidence:
    evidence_id: str
    transition: str
    authority_tier: int
    source_reference: str
    observed_or_published: str
    data_vintage: str
    geography: str
    economic_identifier: str
    summary: str


@dataclass(frozen=True)
class ComparativeEvidencePacket:
    packet_id: str
    schema_version: str
    case_id: str
    replay_mode: str
    information_boundary: str
    target: str
    horizon: str
    evidence: tuple[PacketEvidence, ...]
    counterevidence: tuple[str, ...]
    exclusions: tuple[str, ...]


def packet_hash(packet: ComparativeEvidencePacket) -> str:
    payload = {
        "packet_id": packet.packet_id,
        "schema_version": packet.schema_version,
        "case_id": packet.case_id,
        "replay_mode": packet.replay_mode,
        "information_boundary": packet.information_boundary,
        "target": packet.target,
        "horizon": packet.horizon,
        "evidence": [e.__dict__ for e in packet.evidence],
        "counterevidence": list(packet.counterevidence),
        "exclusions": list(packet.exclusions),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return sha256(canonical.encode("utf-8")).hexdigest()
