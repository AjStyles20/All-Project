from datetime import datetime, timezone

import pytest

from app.domain.audit import build_audit_trace
from app.domain.enums import OutputClass
from app.domain.persistence import (
    build_replay_record,
    read_replay_record,
    record_sha256,
    write_replay_record,
)
from app.fixtures.f1_missing_link import CASE_F1_001, F1_ASSESSMENTS, F1_EVIDENCE


STAMP = datetime(2026, 1, 1, tzinfo=timezone.utc)


def record():
    decision, trace = build_audit_trace(
        CASE_F1_001, F1_EVIDENCE, F1_ASSESSMENTS, generated_at=STAMP
    )
    return build_replay_record(
        CASE_F1_001, F1_EVIDENCE, F1_ASSESSMENTS, decision, trace
    )


def test_same_frozen_inputs_produce_same_record_hash():
    assert record_sha256(record()) == record_sha256(record())


def test_replay_record_preserves_information_cutoff_and_decision():
    r = record()
    assert r["case"]["information_cutoff"] == "2026-01-01T00:00:00+00:00"
    assert r["decision"]["output_class"] == OutputClass.EXPOSURE_IDENTIFIED.value
    assert r["decision"]["stopping_transition"] == "T3_DOMESTIC_TRANSMISSION"


def test_written_record_round_trips_with_integrity_hash(tmp_path):
    path = tmp_path / "CASE-F1-001.replay.json"
    r = record()
    digest = write_replay_record(path, r)
    loaded = read_replay_record(path, expected_sha256=digest)
    assert loaded == r


def test_tampered_replay_record_is_rejected(tmp_path):
    path = tmp_path / "CASE-F1-001.replay.json"
    r = record()
    digest = write_replay_record(path, r)
    path.write_text('{"tampered":true}', encoding="utf-8")
    with pytest.raises(ValueError, match="integrity check failed"):
        read_replay_record(path, expected_sha256=digest)
