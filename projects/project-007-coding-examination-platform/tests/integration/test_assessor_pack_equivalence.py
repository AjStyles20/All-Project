from dataclasses import asdict

from app.research.assessor_package import build_assessor_package
from app.research.pilot_cases import case_pilot_001, case_pilot_003


def test_case_001_machine_package_contains_frozen_human_evidence():
    package = build_assessor_package(case_pilot_001())
    assert package.task_version == package.case_version == "1.0"
    text = " ".join(item.content for item in package.evidence)
    assert "def count_even(values):" in text
    assert "[1, 2, 3, 4] -> 2 PASS" in text
    assert "[2, 4, 6] -> 3 PASS" in text
    assert "[1, 3, 5] -> 0 PASS" in text


def test_case_003_machine_package_freezes_exact_assessor_response():
    package = build_assessor_package(case_pilot_003())
    text = " ".join(item.content for item in package.evidence)
    expected = "Input: [2, 3]. Expected output: 2. Reason: this checks that the function can handle both an even and an odd number."
    assert expected in text
    assert "should return 1" not in text


def test_machine_package_remains_blinded_after_evidence_alignment():
    serialized = repr(asdict(build_assessor_package(case_pilot_001())))
    for forbidden in (
        "construction_expectation", "expected_state", "reference_state",
        "UNRESOLVED development expectation",
    ):
        assert forbidden not in serialized
