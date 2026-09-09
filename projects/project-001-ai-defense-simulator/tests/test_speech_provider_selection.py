import pytest

from app.speech_provider_selection import (
    SpeechProviderSelectionError,
    build_speech_transcriber_from_env,
)


OPENAI_TEST_KEY = "sk-test-secret"
GROQ_TEST_KEY = "gsk-test-secret"


def clear_env(monkeypatch: pytest.MonkeyPatch):
    for name in (
        "P001_SPEECH_PROVIDER",
        "P001_GROQ_API_KEY",
        "P001_GROQ_TRANSCRIPTION_MODEL",
        "P001_GROQ_TIMEOUT_SECONDS",
        "P001_OPENAI_ENABLED",
        "P001_OPENAI_API_KEY",
        "P001_OPENAI_TRANSCRIPTION_MODEL",
    ):
        monkeypatch.delenv(name, raising=False)


def test_auto_uses_groq_when_groq_is_selected_text_provider(monkeypatch: pytest.MonkeyPatch):
    clear_env(monkeypatch)
    monkeypatch.setenv("P001_GROQ_API_KEY", GROQ_TEST_KEY)
    provider = build_speech_transcriber_from_env(selected_text_provider="groq")
    try:
        assert provider.provider_name == "groq"
        assert provider.model_name == "whisper-large-v3-turbo"
    finally:
        provider.close()


def test_explicit_disabled_returns_none(monkeypatch: pytest.MonkeyPatch):
    clear_env(monkeypatch)
    monkeypatch.setenv("P001_SPEECH_PROVIDER", "disabled")
    assert build_speech_transcriber_from_env(selected_text_provider="groq") is None


def test_explicit_openai_preserves_existing_openai_stt(monkeypatch: pytest.MonkeyPatch):
    clear_env(monkeypatch)
    monkeypatch.setenv("P001_SPEECH_PROVIDER", "openai")
    monkeypatch.setenv("P001_OPENAI_ENABLED", "1")
    monkeypatch.setenv("P001_OPENAI_API_KEY", OPENAI_TEST_KEY)
    provider = build_speech_transcriber_from_env(selected_text_provider="groq")
    try:
        assert provider.provider_name == "openai"
    finally:
        provider.close()


def test_explicit_groq_works_independently_of_text_provider(monkeypatch: pytest.MonkeyPatch):
    clear_env(monkeypatch)
    monkeypatch.setenv("P001_SPEECH_PROVIDER", "groq")
    monkeypatch.setenv("P001_GROQ_API_KEY", GROQ_TEST_KEY)
    monkeypatch.setenv("P001_GROQ_TRANSCRIPTION_MODEL", "whisper-large-v3")
    provider = build_speech_transcriber_from_env(selected_text_provider="disabled")
    try:
        assert provider.provider_name == "groq"
        assert provider.model_name == "whisper-large-v3"
    finally:
        provider.close()


def test_invalid_speech_provider_fails_closed(monkeypatch: pytest.MonkeyPatch):
    clear_env(monkeypatch)
    monkeypatch.setenv("P001_SPEECH_PROVIDER", "https://evil.example")
    with pytest.raises(SpeechProviderSelectionError):
        build_speech_transcriber_from_env(selected_text_provider="disabled")
