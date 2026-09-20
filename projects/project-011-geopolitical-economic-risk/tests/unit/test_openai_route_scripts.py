import ast
from pathlib import Path

SCRIPT = Path(__file__).parents[2] / "scripts" / "qualify_openai_b2_route.py"


def test_qualification_script_is_non_experimental():
    text = SCRIPT.read_text(encoding="utf-8")
    assert "B2-A-001" not in text
    assert "B2-NC01-001" not in text
    assert "CANDIDATE_A_PACKET" not in text
    assert "NC01_PACKET" not in text
    assert "prepare_run" not in text


def test_qualification_script_has_no_hardcoded_secret():
    text = SCRIPT.read_text(encoding="utf-8")
    assert "OPENAI_API_KEY" in text
    assert "sk-" not in text


def test_qualification_script_parses():
    ast.parse(SCRIPT.read_text(encoding="utf-8"))
