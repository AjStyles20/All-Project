import httpx
import pytest

from app.groq_provider import GroqProviderRequestError, GroqProviderSettings
from app.groq_transcription import GroqTranscriber
from app.speech import transcribe_checked


TEST_KEY = "gsk-test-secret-never-log"


def settings():
    return GroqProviderSettings(api_key=TEST_KEY, timeout_seconds=5.0)


def test_groq_transcription_uses_fixed_endpoint_and_multipart_without_leaking_secret():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        seen["authorization"] = request.headers.get("authorization")
        seen["content_type"] = request.headers.get("content-type")
        seen["body"] = request.content
        return httpx.Response(200, json={"text": "TCP uses acknowledgments."})

    provider = GroqTranscriber(settings(), transport=httpx.MockTransport(handler))
    try:
        result = transcribe_checked(provider, audio=b"audio-bytes", media_type="audio/webm")
    finally:
        provider.close()

    assert seen["url"] == "https://api.groq.com/openai/v1/audio/transcriptions"
    assert seen["authorization"] == f"Bearer {TEST_KEY}"
    assert "multipart/form-data" in seen["content_type"]
    assert b"audio-bytes" in seen["body"]
    assert b"whisper-large-v3-turbo" in seen["body"]
    assert result.text == "TCP uses acknowledgments."


def test_groq_transcription_http_error_does_not_expose_raw_body_or_key():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, text=f"sensitive upstream details {TEST_KEY}")

    provider = GroqTranscriber(settings(), transport=httpx.MockTransport(handler))
    try:
        with pytest.raises(GroqProviderRequestError) as exc:
            transcribe_checked(provider, audio=b"audio", media_type="audio/webm")
    finally:
        provider.close()

    message = str(exc.value)
    assert "HTTP 429" in message
    assert TEST_KEY not in message
    assert "sensitive upstream details" not in message


def test_groq_transcription_invalid_json_fails_closed():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b"not-json", headers={"content-type": "application/json"})

    provider = GroqTranscriber(settings(), transport=httpx.MockTransport(handler))
    try:
        with pytest.raises(GroqProviderRequestError):
            transcribe_checked(provider, audio=b"audio", media_type="audio/webm")
    finally:
        provider.close()


def test_groq_transcription_respects_provider_neutral_media_type_guard():
    provider = GroqTranscriber(settings(), transport=httpx.MockTransport(lambda request: httpx.Response(500)))
    try:
        with pytest.raises(ValueError, match="unsupported audio media type"):
            transcribe_checked(provider, audio=b"audio", media_type="application/octet-stream")
    finally:
        provider.close()
