from app.domain.evidence_packet import packet_hash
from app.fixtures.nc01_packet import NC01_PACKET_V1, NC01_PACKET_V1_HASH


def test_nc01_packet_hash_is_reproducible():
    assert packet_hash(NC01_PACKET_V1) == NC01_PACKET_V1_HASH


def test_nc01_packet_target_is_narrow_direct_urea_dependence():
    assert "direct Russian urea import dependence" in NC01_PACKET_V1.target
    assert NC01_PACKET_V1.replay_mode == "R2"


def test_nc01_packet_preserves_nonzero_mirror_exposure_and_broader_exclusions():
    summaries = " ".join(e.summary for e in NC01_PACKET_V1.evidence)
    exclusions = " ".join(NC01_PACKET_V1.exclusions)
    assert "non-zero but negligible" in summaries
    assert "broader fertilizer shock" in exclusions
    assert "global-price" in exclusions
