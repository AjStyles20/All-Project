from app.fixtures.candidate_a_packet import CANDIDATE_A_PACKET_V1, CANDIDATE_A_PACKET_V1_HASH
from app.domain.evidence_packet import packet_hash


def test_candidate_a_packet_hash_is_reproducible():
    assert packet_hash(CANDIDATE_A_PACKET_V1) == CANDIDATE_A_PACKET_V1_HASH


def test_candidate_a_packet_is_explicitly_r2():
    assert CANDIDATE_A_PACKET_V1.replay_mode == "R2"
    assert "not established" in CANDIDATE_A_PACKET_V1.exclusions[-1]


def test_candidate_a_packet_excludes_later_outcome_from_baseline_input():
    joined = " ".join(CANDIDATE_A_PACKET_V1.exclusions)
    assert "Later NBS outcome observations are excluded" in joined
