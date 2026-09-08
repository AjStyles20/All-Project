from pathlib import Path


def test_rehearsal_contract_keeps_written_and_bounded_flow_visible():
    contract = Path("docs/technical/FEATURE_011_REHEARSAL_EXPERIENCE_CONTRACT.md").read_text(encoding="utf-8")
    assert "Maximum turns remain hard-bounded to 10" in contract
    assert "Speech remains opt-in and non-autoplay" in contract
    assert "No new authentication claim is introduced" in contract
    assert "Session state transitions are server authoritative" in contract


def test_session_template_exposes_current_action_and_non_color_status():
    template = Path("app/templates/session.html").read_text(encoding="utf-8")
    assert "Current turn" in template
    assert "Awaiting answer" in template
    assert "Answered" in template
    assert "Generate next reviewer challenge" in template
    assert "This session is complete" in template
