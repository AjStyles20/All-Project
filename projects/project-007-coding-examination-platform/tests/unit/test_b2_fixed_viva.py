from app.domain.enums import EvidenceState
from app.services.b2_fixed_viva import B2FixedViva
from app.services.cc3_response_evaluator import CC3ProbeResponse


def test_b2_administers_same_fixed_family_order_for_different_cases():
    viva = B2FixedViva()
    a = viva.administer("CASE-A")
    b = viva.administer("CASE-B")
    expected = ("EXPLAIN", "PREDICT_TRACE", "TEST_DESIGN", "MODIFY")
    assert tuple(q.family for q in a.questions) == expected
    assert tuple(q.family for q in b.questions) == expected
    assert tuple(q.prompt for q in a.questions) == tuple(q.prompt for q in b.questions)


def test_b2_cc3_uses_shared_structured_dimensions_for_fair_comparison():
    result = B2FixedViva().evaluate_cc3(CC3ProbeResponse(
        test_input="[1, 3, 5]", expected_result="[]",
        usefulness_reason="Checks the no-even-values boundary.",
        input_relevant=True, expected_result_correct=True, reason_defensible=True,
    ))
    assert result.state is EvidenceState.SUPPORTED
    assert "non-adaptive" in result.rationale


def test_b2_cc3_partial_response_remains_partial():
    result = B2FixedViva().evaluate_cc3(CC3ProbeResponse(
        test_input="[1, 3, 5]", expected_result="[2]",
        usefulness_reason="No clear reason.",
        input_relevant=True, expected_result_correct=False, reason_defensible=False,
    ))
    assert result.state is EvidenceState.PARTIAL
