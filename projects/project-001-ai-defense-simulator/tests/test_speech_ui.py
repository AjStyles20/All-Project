from pathlib import Path


def test_question_template_requires_separate_transcribe_action_and_keeps_text_answer():
    template = Path("app/templates/question.html").read_text(encoding="utf-8")
    assert 'textarea id="answer"' in template
    assert "Start recording" in template
    assert "Stop recording" in template
    assert "Cancel recording" in template
    assert "Transcribe recording" in template
    assert "only when you select <strong>Transcribe recording</strong>" in template
    assert '<script src="/static/speech.js" defer></script>' in template


def test_speech_javascript_only_requests_microphone_from_start_click_and_never_submits_form():
    script = Path("app/static/speech.js").read_text(encoding="utf-8")
    start_handler = script.index('start.addEventListener("click"')
    microphone_request = script.index("navigator.mediaDevices.getUserMedia")
    assert microphone_request > start_handler
    assert 'transcribe.addEventListener("click"' in script
    assert "fetch(endpoint" in script
    assert "answer.value = payload.transcript" in script
    assert ".submit(" not in script
    assert "requestSubmit" not in script
    assert "MAX_RECORDING_MS = 120000" in script
    assert "discardOnStop" in script


def test_base_template_uses_external_script_block_not_inline_microphone_code():
    base = Path("app/templates/base.html").read_text(encoding="utf-8")
    assert "{% block scripts %}" in base
    assert "getUserMedia" not in base
