from app.domain.b2_manifest import validate_manifest
from app.domain.b2_second_wave_manifest import P003_B2_SECOND_WAVE_MANIFEST_V1
from app.domain.candidate_d_packet import CANDIDATE_D_PACKET_V1
from app.domain.evidence_packet import packet_hash

def test_second_wave_is_candidate_d_only_and_three_runs():
    m=P003_B2_SECOND_WAVE_MANIFEST_V1
    assert [r.run_id for r in m.runs]==["B2-D-001","B2-D-002","B2-D-003"]
    assert {r.packet_id for r in m.runs}=={CANDIDATE_D_PACKET_V1.packet_id}

def test_second_wave_hash_binds_frozen_candidate_d_packet():
    expected=packet_hash(CANDIDATE_D_PACKET_V1)
    assert all(r.packet_hash==expected for r in P003_B2_SECOND_WAVE_MANIFEST_V1.runs)

def test_second_wave_manifest_validates():
    validate_manifest(P003_B2_SECOND_WAVE_MANIFEST_V1)
