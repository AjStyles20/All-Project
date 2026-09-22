import pytest

from app.research.pilot_measurement import (
    DeviationType, PilotDeviation, PilotTimingRecord,
)


def test_pilot_timing_preserves_missing_time_instead_of_zero():
    record = PilotTimingRecord("EXP-1", "B2", 1, None, ("LOW",))
    assert record.verification_seconds is None

    with pytest.raises(ValueError, match="zero seconds"):
        PilotTimingRecord("EXP-1", "B2", 1, 0.0, ("LOW",))


def test_pilot_timing_requires_one_complexity_per_question():
    with pytest.raises(ValueError, match="one entry"):
        PilotTimingRecord("EXP-1", "B4", 2, 20.0, ("LOW",))


def test_deviation_records_analysis_impact_explicitly():
    deviation = PilotDeviation(
        "DEV-001", "EXP-1", DeviationType.MISSING_TIMING,
        "Timer failed after prompt presentation.", ("time_burden",),
    )
    assert deviation.invalidates_analysis == ("time_burden",)
    assert deviation.deviation_type is DeviationType.MISSING_TIMING
