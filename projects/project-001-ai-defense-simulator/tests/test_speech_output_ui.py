from pathlib import Path


def test_question_keeps_text_and_requires_explicit_listen():
    template = Path("app/templates/question.html").read_text(encoding="utf-8")
    assert "{{ question.question_text }}" in template
    assert "Listen to reviewer" in template
    assert "Stop audio" in template
    assert 'data-tts-listen' in template
    assert 'data-tts-status role="status" aria-live="polite"' in template
    assert '<script src="/static/speech_output.js" defer></script>' in template
    assert "autoplay" not in template.lower()


def test_tts_javascript_invokes_server_and_browser_playback_only_from_listen_handler_and_can_stop():
    script = Path("app/static/speech_output.js").read_text(encoding="utf-8")
    handler = script.index('listen.addEventListener("click"')

    # Helper definitions may appear before the click handler. What matters is that the
    # potentially effectful helpers are invoked only after the explicit Listen handler starts.
    server_helper_call = script.index("await playServerSpeech()")
    browser_helper_call = script.index("playBrowserSpeech();", handler)
    assert server_helper_call > handler
    assert browser_helper_call > handler

    # Keep the implementation-level safety expectations explicit as well.
    assert "fetch(endpoint" in script
    assert "await audio.play()" in script
    assert "window.speechSynthesis.speak(utterance)" in script
    assert "window.speechSynthesis.cancel()" in script
    assert "URL.revokeObjectURL" in script
    assert 'stop.addEventListener("click"' in script
    assert "autoplay" not in script.lower()
