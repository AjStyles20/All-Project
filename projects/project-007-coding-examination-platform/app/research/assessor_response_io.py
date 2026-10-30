"""Versioned, non-destructive serialization for M8 assessor responses.

Files produced here are research records supplied by humans; the module does
not create judgments. Existing records are never overwritten.
"""
import json
from dataclasses import asdict
from pathlib import Path

from app.research.assessor_judgment import AssessorJudgment


SCHEMA_VERSION = "M8-ASSESSOR-RESPONSE-v1"


def serialize_judgment(judgment: AssessorJudgment) -> str:
    judgment.validate()
    payload = asdict(judgment)
    payload["state"] = judgment.state.value
    payload["relevant_input"] = judgment.relevant_input.value
    payload["correct_expected_outcome"] = judgment.correct_expected_outcome.value
    payload["defensible_reason"] = judgment.defensible_reason.value
    return json.dumps(
        {"schema_version": SCHEMA_VERSION, "judgment": payload},
        sort_keys=True, indent=2,
    )


def response_filename(judgment: AssessorJudgment) -> str:
    judgment.validate()
    safe_assessor = "".join(c for c in judgment.assessor_code if c.isalnum() or c in "-_")
    safe_case = "".join(c for c in judgment.case_id if c.isalnum() or c in "-_")
    if not safe_assessor or not safe_case:
        raise ValueError("assessor_code and case_id must yield safe identifiers")
    return f"{safe_case}__{safe_assessor}.json"


def write_new_response(directory: Path, judgment: AssessorJudgment) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / response_filename(judgment)
    if target.exists():
        raise FileExistsError("assessor response already exists; do not overwrite original")
    target.write_text(serialize_judgment(judgment), encoding="utf-8")
    return target
