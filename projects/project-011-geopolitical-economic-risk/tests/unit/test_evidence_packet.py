from dataclasses import replace
from app.domain.evidence_packet import ComparativeEvidencePacket, PacketEvidence, packet_hash


def sample():
    return ComparativeEvidencePacket(
        "PKT-1","1","CASE-1","R2","2022-02-24","frozen target","3-6 months",
        (PacketEvidence("E1","T1",1,"source","2022-02-24","v1","Nigeria","HS-X","summary"),),
        ("counter",),("unknown inventory",),
    )


def test_same_packet_has_same_hash():
    assert packet_hash(sample()) == packet_hash(sample())


def test_material_packet_change_changes_hash():
    p = sample()
    assert packet_hash(p) != packet_hash(replace(p, target="changed target"))


def test_evidence_order_and_content_are_part_of_frozen_packet():
    p = sample()
    extra = PacketEvidence("E2","T2",2,"source2","2022-01-01","v1","Nigeria","HS-Y","exposure")
    assert packet_hash(p) != packet_hash(replace(p, evidence=p.evidence + (extra,)))
