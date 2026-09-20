"""Development probe catalogue for P001.

These are development fixtures for CASE-DEV-003, not validated final probes.
"""
from .probe_selector import VerificationProbe


def cc3_development_probes() -> list[VerificationProbe]:
    return [
        VerificationProbe(
            probe_id="VP-CC3-01",
            name="Additional input only",
            prompt="Give one additional input you would test.",
            probe_type="TEST_DESIGN",
            applicable_claims=frozenset({"CC3"}),
            gap_types=frozenset({"EG-T3"}),
            potentially_sufficient_gap_types=frozenset(),
            burden_rank=1,
        ),
        VerificationProbe(
            probe_id="VP-CC3-02",
            name="Bounded independent test design",
            prompt=(
                "Give one important test not already supplied. State the input, "
                "the expected result, and why this test is useful."
            ),
            probe_type="TEST_DESIGN",
            applicable_claims=frozenset({"CC3"}),
            gap_types=frozenset({"EG-T3"}),
            potentially_sufficient_gap_types=frozenset({"EG-T3"}),
            burden_rank=2,
            executable=True,
        ),
        VerificationProbe(
            probe_id="VP-CC3-03",
            name="Comprehensive test suite",
            prompt=(
                "Design a comprehensive test suite, give expected results, and "
                "justify the coverage of each test."
            ),
            probe_type="TEST_DESIGN",
            applicable_claims=frozenset({"CC3"}),
            gap_types=frozenset({"EG-T3"}),
            potentially_sufficient_gap_types=frozenset({"EG-T3"}),
            burden_rank=3,
        ),
    ]
