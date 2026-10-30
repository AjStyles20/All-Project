from dataclasses import asdict
from app.research.assessor_package import build_assessor_package
from app.research.pilot_cases import case_pilot_001, case_pilot_003

def test_assessor_package_does_not_expose_construction_expectation():
    serialized = repr(asdict(build_assessor_package(case_pilot_001())))
    assert 'construction_expectation' not in serialized
    assert 'UNRESOLVED development expectation' not in serialized

def test_case_003_package_contains_literal_response_but_not_hidden_interpretation():
    serialized = repr(asdict(build_assessor_package(case_pilot_003())))
    assert 'Expected output: 2' in serialized
    assert 'PARTIAL development expectation' not in serialized
    assert 'should return 1' not in serialized

def test_assessor_package_has_no_method_outputs_or_reference_answer_fields():
    fields = set(asdict(build_assessor_package(case_pilot_001())))
    forbidden = {'construction_expectation','b0_state','b1_state','b2_state','b3_state','b4_state','reference_state','expected_state'}
    assert not fields.intersection(forbidden)
