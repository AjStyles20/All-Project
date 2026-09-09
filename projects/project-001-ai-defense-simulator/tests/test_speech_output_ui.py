from pathlib import Path


def test_question_keeps_text_and_requires_explicit_playback():
    template = Path("app/templates/question.html").read_text(encoding="utf-8")
    assert "{{ question.question_text }}" in template
    assert "Play / Replay" in template
    assert "Pause" in template
    assert "Resume" in template
    assert "Stop" in template
    assert "0.75×" in template
    assert "1.25×" in template
    assert "1.5×" in template
    assert 'data-tts-listen' in template
    assert 'data-tts-pause' in template
    assert 'data-tts-resume' in template
    assert 'data-tts-rate' in template
    assert 'data-tts-status role="status" aria-live="polite"' in template
    assert '<script src="/static/speech_output.js" defer></script>' in template
    assert "autoplay" not in template.lower()


def test_tts_javascript_playback_controls_remain_explicit_and_bounded():
    script = Path("app/static/speech_output.js").read_text(encoding="utf-8")
    handler = script.index('listen.addEventListener("click"')

    server_helper_call = script.index("await playServerSpeech()")
    browser_helper_call = script.index("playBrowserSpeech();", handler)
    assert server_helper_call > handler
    assert browser_helper_call > handler

    assert "fetch(endpoint" in script
    assert "await audio.play()" in script
    assert "window.speechSynthesis.speak(utterance)" in script
    assert "window.speechSynthesis.cancel()" in script
    assert "window.speechSynthesis.pause()" in script
    assert "window.speechSynthesis.resume()" in script
    assert "audio.playbackRate = selectedRate()" in script
    assert "utterance.rate = selectedRate()" in script
    assert "[0.75, 1, 1.25, 1.5]" in script
    assert "URL.revokeObjectURL" in script
    assert 'pause.addEventListener("click"' in script
    assert 'resume.addEventListener("click"' in script
    assert 'rate.addEventListener("change"' in script
    assert 'stop.addEventListener("click"' in script
    assert "autoplay" not in script.lower()


def test_session_review_navigation_does_not_replace_followup_gate():
    template = Path("app/templates/session.html").read_text(encoding="utf-8")
    assert 'id="turn-{{ turn.turn_index }}"' in template
    assert "← Previous turn" in template
    assert "Next turn →" in template
    assert "only moves among turns that already exist" in template
    assert "does not skip an unanswered examiner question or generate a new turn" in template
    assert "Generate evidence-grounded follow-up" in template
    assert "Answer the current question before requesting a follow-up." in template
