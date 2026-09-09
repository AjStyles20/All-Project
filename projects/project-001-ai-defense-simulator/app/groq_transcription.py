from __future__ import annotations

import os

import httpx

from .groq_provider import GROQ_API_BASE, GroqProviderRequestError, GroqProviderSettings
from .speech import TranscriptionResult

DEFAULT_GROQ_TRANSCRIPTION_MODEL = "whisper-large-v3-turbo"
MAX_MODEL_ID_CHARS = 200


class GroqTranscriptionConfigurationError(ValueError):
    pass


def _transcription_model_from_env() -> str:
    configured = os.getenv(
        "P001_GROQ_TRANSCRIPTION_MODEL",
        DEFAULT_GROQ_TRANSCRIPTION_MODEL,
    ).strip()
    if not configured or len(configured) > MAX_MODEL_ID_CHARS:
        raise GroqTranscriptionConfigurationError("invalid Groq transcription model")
    return configured


class GroqTranscriber:
    provider_name = "groq"
    model_version = None

    def __init__(
        self,
        settings: GroqProviderSettings,
        *,
        model_name: str | None = None,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        configured = (model_name or _transcription_model_from_env()).strip()
        if not configured or len(configured) > MAX_MODEL_ID_CHARS:
            raise GroqTranscriptionConfigurationError("invalid Groq transcription model")
        self.model_name = configured
        self._client = httpx.Client(
            base_url=GROQ_API_BASE,
            headers={
                "Authorization": f"Bearer {settings.api_key}",
                "User-Agent": "project-001/1.3",
            },
            timeout=httpx.Timeout(settings.timeout_seconds),
            follow_redirects=False,
            transport=transport,
        )

    def close(self) -> None:
        self._client.close()

    def transcribe(self, *, audio: bytes, media_type: str) -> TranscriptionResult:
        extension = {
            "audio/webm": "webm",
            "audio/ogg": "ogg",
            "audio/mp4": "mp4",
            "audio/mpeg": "mp3",
            "audio/wav": "wav",
            "audio/x-wav": "wav",
        }.get(media_type)
        if extension is None:
            raise ValueError("unsupported audio media type")

        try:
            response = self._client.post(
                "/audio/transcriptions",
                data={
                    "model": self.model_name,
                    "response_format": "json",
                    "temperature": "0",
                },
                files={"file": (f"recording.{extension}", audio, media_type)},
            )
        except httpx.TimeoutException as exc:
            raise GroqProviderRequestError("transcription provider request timed out") from exc
        except httpx.RequestError as exc:
            raise GroqProviderRequestError("transcription provider request failed") from exc

        if response.status_code < 200 or response.status_code >= 300:
            raise GroqProviderRequestError(
                f"transcription provider returned HTTP {response.status_code}"
            )
        try:
            payload = response.json()
        except ValueError as exc:
            raise GroqProviderRequestError("transcription provider returned invalid JSON") from exc
        if not isinstance(payload, dict) or not isinstance(payload.get("text"), str):
            raise GroqProviderRequestError("transcription provider returned invalid transcript data")
        language = payload.get("language")
        if language is not None and not isinstance(language, str):
            language = None
        return TranscriptionResult(text=payload["text"], language=language)
