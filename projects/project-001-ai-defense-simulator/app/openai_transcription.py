from __future__ import annotations

import os

import httpx

from .openai_provider import (
    OPENAI_API_BASE,
    OpenAIProviderSettings,
    ProviderConfigurationError,
    ProviderRequestError,
)
from .speech import TranscriptionResult

DEFAULT_TRANSCRIPTION_MODEL = "gpt-transcribe"
MAX_MODEL_ID_CHARS = 200


class OpenAITranscriber:
    provider_name = "openai"
    model_version = None

    def __init__(
        self,
        settings: OpenAIProviderSettings,
        *,
        model_name: str | None = None,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        configured = (model_name or os.getenv("P001_OPENAI_TRANSCRIPTION_MODEL", DEFAULT_TRANSCRIPTION_MODEL)).strip()
        if not configured or len(configured) > MAX_MODEL_ID_CHARS:
            raise ProviderConfigurationError("invalid OpenAI transcription model")
        self.model_name = configured
        self._client = httpx.Client(
            base_url=OPENAI_API_BASE,
            headers={
                "Authorization": f"Bearer {settings.api_key}",
                "User-Agent": "project-001/0.9",
            },
            timeout=httpx.Timeout(settings.timeout_seconds),
            follow_redirects=False,
            transport=transport,
        )

    def close(self) -> None:
        self._client.close()

    def transcribe(self, *, audio: bytes, media_type: str) -> TranscriptionResult:
        # Input size/type validation is performed by the provider-neutral speech layer before this call.
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
                data={"model": self.model_name, "response_format": "json"},
                files={"file": (f"recording.{extension}", audio, media_type)},
            )
        except httpx.TimeoutException as exc:
            raise ProviderRequestError("transcription provider request timed out") from exc
        except httpx.RequestError as exc:
            raise ProviderRequestError("transcription provider request failed") from exc

        if response.status_code < 200 or response.status_code >= 300:
            # Never propagate raw provider bodies; they can contain sensitive operational details.
            raise ProviderRequestError(f"transcription provider returned HTTP {response.status_code}")
        try:
            payload = response.json()
        except ValueError as exc:
            raise ProviderRequestError("transcription provider returned invalid JSON") from exc
        if not isinstance(payload, dict) or not isinstance(payload.get("text"), str):
            raise ProviderRequestError("transcription provider returned invalid transcript data")
        language = payload.get("language")
        if language is not None and not isinstance(language, str):
            language = None
        return TranscriptionResult(text=payload["text"], language=language)
