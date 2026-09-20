from app.domain.b2_prompt import SYSTEM_PROMPT_V1, serialize_packet_for_b2
from app.fixtures.candidate_a_packet import CANDIDATE_A_PACKET_V1
from app.fixtures.nc01_packet import NC01_PACKET_V1


def test_candidate_a_serialization_contains_packet_and_counterevidence_without_internal_transition_fields():
    s=serialize_packet_for_b2(CANDIDATE_A_PACKET_V1)
    assert CANDIDATE_A_PACKET_V1.packet_id in s
    assert "Foreign-exchange scarcity" in s
    assert "Later NBS outcome observations are excluded" in s
    # Frozen exclusions may legitimately mention strings such as T5/T6.
    # The prohibited leakage is B3's internal state/stopping decision.
    assert "TRANSITION_STATE:" not in s
    assert "STOPPING_TRANSITION:" not in s
    assert "PROHIBITED_OUTPUTS:" not in s
    assert "EXPECTED_B3_OUTPUT:" not in s


def test_nc01_serialization_preserves_nonzero_exposure_and_narrow_scope():
    s=serialize_packet_for_b2(NC01_PACKET_V1)
    assert "non-zero but negligible" in s
    assert "broader fertilizer shock" in s
    assert "direct Russian urea import dependence" in s


def test_system_prompt_prohibits_invention_and_allows_abstention():
    p=SYSTEM_PROMPT_V1.lower()
    assert "do not invent" in p
    assert "insufficient" in p
