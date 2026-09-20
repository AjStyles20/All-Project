import json

import pytest

from app.domain.enums import EvidenceState
from app.research.assessor_judgment import AssessorJudgment, DimensionJudgment
from app.research.assessor_response_io import (
    SCHEMA_VERSION, response_filename, serialize_judgment, write_new_response,
)


def response():
    return AssessorJudgment(
        "ASSESSOR-A", "CASE-PILOT-001", EvidenceState.UNRESOLVED,
        DimensionJudgment.CANNOT_DETERMINE,
        DimensionJudgment.CANNOT_DETERMINE,
        DimensionJudgment.CANNOT_DETERMINE,
        "No independent test-design response was shown.",
        True, None, True, "A candidate-authored test design response.",
        False, None, True,
    )


def test_serialized_response_is_versioned_and_contains_human_record():
    payload = json.loads(serialize_judgment(response()))
    assert payload["schema_version"] == SCHEMA_VERSION
    assert payload["judgment"]["state"] == "UNRESOLVED"
    assert payload["judgment"]["assessor_code"] == "ASSESSOR-A"


def test_filename_is_deterministic_and_non_identifying():
    assert response_filename(response()) == "CASE-PILOT-001__ASSESSOR-A.json"


def test_writer_refuses_to_overwrite_original_response(tmp_path):
    path = write_new_response(tmp_path, response())
    assert path.exists()
    with pytest.raises(FileExistsError, match="do not overwrite"):
        write_new_response(tmp_path, response())
