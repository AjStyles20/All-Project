import json

import httpx
import pytest

from app.openai_provider import OpenAIProviderSettings, ProviderRequestError
from app.openai_transcription import OpenAITranscriber
from app.speech import transcribe_checked


TEST_KEY = "sk-test-secret-never-log"


def settings():
    return OpenAIProviderSettings(api_key=TEST_KEY, timeout_seconds=5.0)


def test_openai_transcription_uses_fixed_endpoint_and_multipart_without_leaking_secret():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["url"] = str(request.url)
        seen["authorization"] = request.headers.get("authorization")
        seen["content_type"] = request.headers.get("content-type")
        seen["body"] = request.content
        return httpx.Response(200, json={"text": "Server-side transcript.", "language": "en"})

    provider = OpenAITranscriber(settings(), transport=httpx.MockTransport(handler))
    try:
        result = transcribe_checked(provider, audio=b"audio-bytes", media_type="audio/webm")
    finally:
        provider.close()

    assert seen["url"].endswith("/audio/transcriptions")
    assert seen["authorization"] == f"Bearer {TEST_KEY}"
    assert "multipart/form-data" in seen["content_type"]
    assert b"audio-bytes" in seen["body"]
    assert b"gpt-transcribe" in seen["body"]
    assert result.text == "Server-side transcript."


def test_provider_http_error_does_not_expose_raw_body_or_api_key():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(400, text=f"sensitive upstream details {TEST_KEY}")

    provider = OpenAITranscriber(settings(), transport=httpx.MockTransport(handler))
    try:
        with pytest.raises(ProviderRequestError) as exc:
            transcribe_checked(provider, audio=b"audio", media_type="audio/webm")
    finally:
        provider.close()
    message = str(exc.value)
    assert TEST_KEY not in message
    assert "sensitive upstream details" not in message
    assert "HTTP 400" in message


def test_provider_invalid_json_fails_closed():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=b"not-json", headers={"content-type": "application/json"})

    provider = OpenAITranscriber(settings(), transport=httpx.MockTransport(handler))
    try:
        with pytest.raises(ProviderRequestError):
            transcribe_checked(provider, audio=b"audio", media_type="audio/webm")
    finally:
        provider.close()
