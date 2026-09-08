from __future__ import annotations

import os

import httpx

from .openai_provider import OPENAI_API_BASE, OpenAIProviderSettings, ProviderConfigurationError, ProviderRequestError
from .speech_output import SpeechSynthesisResult

DEFAULT_TTS_MODEL = "gpt-4o-mini-tts"
DEFAULT_TTS_VOICE = "alloy"
ALLOWED_TTS_VOICES = {"alloy", "ash", "ballad", "coral", "echo", "fable", "nova", "onyx", "sage", "shimmer"}
MAX_MODEL_ID_CHARS = 200


class OpenAISpeechSynthesizer:
    provider_name = "openai"
    model_version = None

    def __init__(
        self,
        settings: OpenAIProviderSettings,
        *,
        model_name: str | None = None,
        voice_name: str | None = None,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        model = (model_name or os.getenv("P001_OPENAI_TTS_MODEL", DEFAULT_TTS_MODEL)).strip()
        voice = (voice_name or os.getenv("P001_OPENAI_TTS_VOICE", DEFAULT_TTS_VOICE)).strip().lower()
        if not model or len(model) > MAX_MODEL_ID_CHARS:
            raise ProviderConfigurationError("invalid OpenAI TTS model")
        if voice not in ALLOWED_TTS_VOICES:
            raise ProviderConfigurationError("invalid OpenAI TTS voice")
        self.model_name = model
        self.voice_name = voice
        self._client = httpx.Client(
            base_url=OPENAI_API_BASE,
            headers={"Authorization": f"Bearer {settings.api_key}", "User-Agent": "project-001/0.10"},
            timeout=httpx.Timeout(settings.timeout_seconds),
            follow_redirects=False,
            transport=transport,
        )

    def close(self) -> None:
        self._client.close()

    def synthesize(self, *, text: str) -> SpeechSynthesisResult:
        try:
            response = self._client.post(
                "/audio/speech",
                json={
                    "model": self.model_name,
                    "voice": self.voice_name,
                    "input": text,
                    "response_format": "mp3",
                },
            )
        except httpx.TimeoutException as exc:
            raise ProviderRequestError("speech provider request timed out") from exc
        except httpx.RequestError as exc:
            raise ProviderRequestError("speech provider request failed") from exc
        if response.status_code < 200 or response.status_code >= 300:
            raise ProviderRequestError(f"speech provider returned HTTP {response.status_code}")
        return SpeechSynthesisResult(audio=response.content, media_type="audio/mpeg")
