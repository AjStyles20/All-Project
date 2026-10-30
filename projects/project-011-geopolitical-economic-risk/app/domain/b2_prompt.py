"""Deterministic B2 prompt serialization from a frozen evidence packet."""
from app.domain.evidence_packet import ComparativeEvidencePacket

SYSTEM_PROMPT_V1 = """You are an economic-risk analyst. Use only the supplied frozen evidence packet. Assess the stated Nigeria target over the stated horizon. Distinguish facts, uncertainty, counterevidence, and inference. Do not invent missing evidence, numerical magnitudes, probabilities, causal certainty, or sources. If the packet is insufficient for a downstream claim, say so. Return a concise evidence-grounded assessment."""

def serialize_packet_for_b2(packet: ComparativeEvidencePacket) -> str:
    lines = [
        f"PACKET_ID: {packet.packet_id}",
        f"SCHEMA_VERSION: {packet.schema_version}",
        f"CASE_ID: {packet.case_id}",
        f"REPLAY_MODE: {packet.replay_mode}",
        f"INFORMATION_BOUNDARY: {packet.information_boundary}",
        f"TARGET: {packet.target}",
        f"HORIZON: {packet.horizon}",
        "",
        "EVIDENCE:",
    ]
    for e in packet.evidence:
        lines.extend([
            f"- EVIDENCE_ID: {e.evidence_id}",
            f"  AUTHORITY_TIER: {e.authority_tier}",
            f"  SOURCE_REFERENCE: {e.source_reference}",
            f"  OBSERVED_OR_PUBLISHED: {e.observed_or_published}",
            f"  DATA_VINTAGE: {e.data_vintage}",
            f"  GEOGRAPHY: {e.geography}",
            f"  ECONOMIC_IDENTIFIER: {e.economic_identifier}",
            f"  SUMMARY: {e.summary}",
        ])
    lines.append("")
    lines.append("COUNTEREVIDENCE:")
    lines.extend(f"- {x}" for x in packet.counterevidence)
    lines.append("")
    lines.append("EXCLUSIONS_AND_UNKNOWNS:")
    lines.extend(f"- {x}" for x in packet.exclusions)
    lines.extend([
        "",
        "TASK:",
        "Assess the TARGET using only this packet. State the strongest downstream conclusion the evidence supports and what remains unsupported or uncertain. Do not refer to ETEC, transition labels, baseline identities, reviewer labels, or later outcome data.",
    ])
    return "\n".join(lines)
