import ast
from pathlib import Path

SCRIPT = Path(__file__).parents[2] / "scripts" / "run_b2_openai.py"


def _text():
    return SCRIPT.read_text(encoding="utf-8")


def test_b2_runner_parses():
    ast.parse(_text())


def test_b2_runner_uses_frozen_first_wave_fixtures_and_gate():
    text = _text()
    assert "B2_EXPERIMENT_MANIFEST_V1" in text
    assert "CANDIDATE_A_PACKET_V1" in text
    assert "NC01_PACKET_V1" in text
    assert "prepare_run" in text
    assert "packet_hash(packet)" in text


def test_b2_runner_does_not_hardcode_api_secret():
    text = _text()
    assert "OPENAI_API_KEY" in text
    assert "sk-" not in text


def test_b2_runner_records_required_provenance_fields():
    text = _text()
    for field in (
        "run_id",
        "packet_id",
        "packet_hash",
        "provider",
        "requested_model",
        "returned_model",
        "provider_response_id",
        "attempt_started_utc",
        "system_prompt",
        "user_prompt",
        "raw_response",
        "status",
    ):
        assert f'"{field}"' in text
