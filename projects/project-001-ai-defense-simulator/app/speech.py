from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


MAX_AUDIO_BYTES = 10 * 1024 * 1024
MAX_TRANSCRIPT_CHARS = 8000
ALLOWED_AUDIO_TYPES = {
    "audio/webm",
    "audio/ogg",
    "audio/mp4",
    "audio/mpeg",
    "audio/wav",
    "audio/x-wav",
}


@dataclass(frozen=True)
class TranscriptionResult:
    text: str
    language: str | None = None


class SpeechTranscriber(Protocol):
    provider_name: str
    model_name: str
    model_version: str | None

    def transcribe(self, *, audio: bytes, media_type: str) -> TranscriptionResult:
        """Return plain-text transcription for bounded untrusted audio bytes."""


def validate_audio_input(audio: bytes, *, media_type: str) -> tuple[bytes, str]:
    if not isinstance(audio, (bytes, bytearray)):
        raise ValueError("audio payload must be bytes")
    payload = bytes(audio)
    if not payload:
        raise ValueError("audio payload is empty")
    if len(payload) > MAX_AUDIO_BYTES:
        raise ValueError("audio payload exceeds maximum size")
    cleaned_type = str(media_type).split(";", 1)[0].strip().lower()
    if cleaned_type not in ALLOWED_AUDIO_TYPES:
        raise ValueError("unsupported audio media type")
    return payload, cleaned_type


def validate_transcription_result(result: object) -> TranscriptionResult:
    if not isinstance(result, TranscriptionResult):
        raise ValueError("transcriber returned invalid result type")
    if not isinstance(result.text, str):
        raise ValueError("transcription must be text")
    cleaned = " ".join(result.text.split()).strip()
    if not cleaned:
        raise ValueError("transcription is empty")
    if len(cleaned) > MAX_TRANSCRIPT_CHARS:
        raise ValueError("transcription exceeds maximum length")
    language = None
    if result.language is not None:
        if not isinstance(result.language, str):
            raise ValueError("transcription language must be text")
        language = result.language.strip()
        if not language or len(language) > 32:
            raise ValueError("transcription language is invalid")
    return TranscriptionResult(text=cleaned, language=language)


def transcribe_checked(
    provider: SpeechTranscriber,
    *,
    audio: bytes,
    media_type: str,
) -> TranscriptionResult:
    payload, cleaned_type = validate_audio_input(audio, media_type=media_type)
    return validate_transcription_result(
        provider.transcribe(audio=payload, media_type=cleaned_type)
    )
