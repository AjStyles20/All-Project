import httpx
import pytest

from app.openai_provider import OpenAIProviderSettings, ProviderConfigurationError, ProviderRequestError
from app.openai_speech_output import OpenAISpeechSynthesizer


def settings():
    return OpenAIProviderSettings(api_key="secret-test-key", timeout_seconds=5.0)


def test_openai_tts_uses_fixed_audio_speech_endpoint_and_server_voice():
    seen = {}

    def handler(request: httpx.Request):
        seen["url"] = str(request.url)
        seen["body"] = request.content.decode()
        seen["auth"] = request.headers.get("authorization")
        return httpx.Response(200, content=b"ID3audio", headers={"content-type": "audio/mpeg"})

    provider = OpenAISpeechSynthesizer(settings(), transport=httpx.MockTransport(handler), voice_name="alloy")
    result = provider.synthesize(text="Explain your method.")
    assert seen["url"] == "https://api.openai.com/v1/audio/speech"
    assert '"voice":"alloy"' in seen["body"]
    assert '"input":"Explain your method."' in seen["body"]
    assert seen["auth"] == "Bearer secret-test-key"
    assert result.audio == b"ID3audio"
    assert result.media_type == "audio/mpeg"


def test_openai_tts_rejects_unapproved_voice():
    with pytest.raises(ProviderConfigurationError):
        OpenAISpeechSynthesizer(settings(), voice_name="custom-user-voice")


def test_openai_tts_does_not_expose_provider_error_body():
    def handler(_request: httpx.Request):
        return httpx.Response(500, text="secret-test-key upstream internal detail")

    provider = OpenAISpeechSynthesizer(settings(), transport=httpx.MockTransport(handler))
    with pytest.raises(ProviderRequestError) as exc:
        provider.synthesize(text="Question")
    assert "secret-test-key" not in str(exc.value)
    assert "internal detail" not in str(exc.value)
