from app.domain.enums import EvidenceState
from app.services.cc3_response_evaluator import CC3ProbeResponse, CC3ResponseEvaluator


def response(*, relevant, correct, defensible):
    return CC3ProbeResponse(
        test_input="[1, 3, 5]",
        expected_result="[]",
        usefulness_reason="Checks the no-even-values boundary.",
        input_relevant=relevant,
        expected_result_correct=correct,
        reason_defensible=defensible,
    )


def test_complete_structured_cc3_response_is_supported():
    result = CC3ResponseEvaluator().evaluate(
        response(relevant=True, correct=True, defensible=True)
    )
    assert result.state is EvidenceState.SUPPORTED


def test_incomplete_but_relevant_cc3_response_is_partial():
    result = CC3ResponseEvaluator().evaluate(
        response(relevant=True, correct=True, defensible=False)
    )
    assert result.state is EvidenceState.PARTIAL


def test_response_with_no_satisfied_components_remains_unresolved():
    result = CC3ResponseEvaluator().evaluate(
        response(relevant=False, correct=False, defensible=False)
    )
    assert result.state is EvidenceState.UNRESOLVED
