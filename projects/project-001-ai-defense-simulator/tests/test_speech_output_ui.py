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


def test_tts_javascript_fetches_only_inside_listen_handler_and_revokes_blob_urls():
    script = Path("app/static/speech_output.js").read_text(encoding="utf-8")
    handler = script.index('listen.addEventListener("click"')
    fetch_call = script.index("fetch(endpoint")
    play_call = script.index("audio.play()")
    assert fetch_call > handler
    assert play_call > handler
    assert "URL.revokeObjectURL" in script
    assert 'stop.addEventListener("click"' in script
    assert "autoplay" not in script.lower()
