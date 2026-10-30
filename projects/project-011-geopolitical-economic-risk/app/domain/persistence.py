"""Deterministic JSON persistence for reproducible ETEC decision records."""
import hashlib
import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from .audit import AuditTrace
from .models import EconomicCase, EvidenceItem, TransitionAssessment
from .progression import ProgressionDecision


def _jsonable(value):
    if isinstance(value, datetime):
        return value.isoformat()
    if hasattr(value, "value"):
        return value.value
    if isinstance(value, tuple):
        return [_jsonable(v) for v in value]
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {k: _jsonable(v) for k, v in value.items()}
    return value


def build_replay_record(
    case: EconomicCase,
    evidence: tuple[EvidenceItem, ...],
    assessments: tuple[TransitionAssessment, ...],
    decision: ProgressionDecision,
    trace: AuditTrace,
) -> dict:
    return {
        "schema_version": "p003-replay-v1",
        "case": _jsonable(asdict(case)),
        "evidence": [_jsonable(asdict(item)) for item in evidence],
        "assessments": [_jsonable(asdict(item)) for item in assessments],
        "decision": _jsonable(asdict(decision)),
        "audit_trace": _jsonable(asdict(trace)),
    }


def canonical_bytes(record: dict) -> bytes:
    return json.dumps(
        record, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def record_sha256(record: dict) -> str:
    return hashlib.sha256(canonical_bytes(record)).hexdigest()


def write_replay_record(path: Path, record: dict) -> str:
    payload = canonical_bytes(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return hashlib.sha256(payload).hexdigest()


def read_replay_record(path: Path, expected_sha256: str | None = None) -> dict:
    payload = path.read_bytes()
    actual = hashlib.sha256(payload).hexdigest()
    if expected_sha256 is not None and actual != expected_sha256:
        raise ValueError("replay record integrity check failed")
    return json.loads(payload.decode("utf-8"))
