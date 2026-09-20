from app.domain.candidate_d_packet import CANDIDATE_D_PACKET_V1
from app.domain.evidence_packet import packet_hash

def test_candidate_d_packet_identity_and_boundary():
    p=CANDIDATE_D_PACKET_V1
    assert p.packet_id=="P003-D-R2-PKT-v1"
    assert p.replay_mode=="R2"
    assert "Post-boundary outcome observations are excluded from this packet." in p.exclusions

def test_candidate_d_packet_has_t1_t2_t3_evidence():
    assert {e.transition for e in CANDIDATE_D_PACKET_V1.evidence}=={"T1","T2","T3"}

def test_candidate_d_packet_preserves_counterchannels_and_classification_limit():
    text=" ".join(CANDIDATE_D_PACKET_V1.counterevidence).lower()
    assert "crude" in text and "foreign-exchange" in text
    assert any("broader than pms" in x.lower() for x in CANDIDATE_D_PACKET_V1.counterevidence)

def test_candidate_d_packet_hash_is_deterministic():
    h1=packet_hash(CANDIDATE_D_PACKET_V1); h2=packet_hash(CANDIDATE_D_PACKET_V1)
    assert h1==h2 and len(h1)==64
