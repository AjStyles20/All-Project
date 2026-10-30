"""Predeclared B2 experimental manifest.

The manifest fixes which real B2 generations are required before any output is
seen. It does not execute an LLM.
"""
from dataclasses import dataclass
from app.domain.evidence_packet import ComparativeEvidencePacket, packet_hash


@dataclass(frozen=True)
class PlannedB2Run:
    run_id: str
    packet_id: str
    packet_hash: str
    generation_index: int


@dataclass(frozen=True)
class B2ExperimentManifest:
    manifest_id: str
    protocol_version: str
    runs: tuple[PlannedB2Run, ...]


def plan_case_runs(packet: ComparativeEvidencePacket, prefix: str, count: int = 3) -> tuple[PlannedB2Run, ...]:
    if count < 1:
        raise ValueError("At least one run must be predeclared.")
    h = packet_hash(packet)
    return tuple(
        PlannedB2Run(
            run_id=f"{prefix}-{i:03d}",
            packet_id=packet.packet_id,
            packet_hash=h,
            generation_index=i,
        )
        for i in range(1, count + 1)
    )


def validate_manifest(manifest: B2ExperimentManifest) -> None:
    ids = [r.run_id for r in manifest.runs]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate predeclared B2 run ID.")
    if not manifest.runs:
        raise ValueError("Manifest must contain at least one run.")
