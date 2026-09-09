from pathlib import Path


def test_question_template_keeps_written_question_authoritative_and_enables_local_tts_fallback():
    template = Path("app/templates/question.html").read_text(encoding="utf-8")
    assert "{{ question.question_text }}" in template
    assert 'data-question-text="{{ question.question_text | e }}"' in template
    assert 'data-server-configured=' in template
    assert "Listen to reviewer" in template
    assert "local reviewer speech" in template
    assert "does not send the question to a Project 001 TTS provider" in template


def test_browser_tts_requires_explicit_listen_and_preserves_server_tts_path():
    script = Path("app/static/speech_output.js").read_text(encoding="utf-8")
    listen_handler = script.index('listen.addEventListener("click"')
    speak_call = script.index("window.speechSynthesis.speak(utterance)")
    server_fetch = script.index("fetch(endpoint")

    assert speak_call < listen_handler  # helper definition may appear earlier
    assert "playBrowserSpeech();" in script[listen_handler:]
    assert server_fetch < listen_handler  # server helper is defined before click handler
    assert "await playServerSpeech();" in script[listen_handler:]
    assert "serverConfigured" in script


def test_browser_tts_has_stop_cancel_and_no_autoplay_side_effect():
    script = Path("app/static/speech_output.js").read_text(encoding="utf-8")
    assert 'stop.addEventListener("click"' in script
    assert "window.speechSynthesis.cancel()" in script
    assert "new window.SpeechSynthesisUtterance(questionText)" in script
    assert "autoplay" not in script.lower()
    # The only browser speak invocation must be reached through playBrowserSpeech,
    # which is itself called by the explicit Listen handler.
    assert script.count("speechSynthesis.speak(") == 1


def test_browser_tts_fails_closed_when_browser_has_no_local_speech_engine():
    script = Path("app/static/speech_output.js").read_text(encoding="utf-8")
    assert '"speechSynthesis" in window' in script
    assert "listen.disabled = true" in script
    assert "Reviewer speech is unavailable in this browser" in script
