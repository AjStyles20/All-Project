from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


MAX_SPEECH_TEXT_CHARS = 1200
MAX_SYNTHESIZED_AUDIO_BYTES = 5 * 1024 * 1024
ALLOWED_SYNTHESIZED_MEDIA_TYPES = {"audio/mpeg"}


@dataclass(frozen=True)
class SpeechSynthesisResult:
    audio: bytes
    media_type: str


class SpeechSynthesizer(Protocol):
    provider_name: str
    model_name: str
    model_version: str | None
    voice_name: str

    def synthesize(self, *, text: str) -> SpeechSynthesisResult:
        """Return bounded speech audio for authoritative stored question text."""


def validate_speech_text(text: object) -> str:
    if not isinstance(text, str):
        raise ValueError("speech text must be text")
    cleaned = " ".join(text.split()).strip()
    if not cleaned:
        raise ValueError("speech text is empty")
    if len(cleaned) > MAX_SPEECH_TEXT_CHARS:
        raise ValueError("speech text exceeds maximum length")
    return cleaned


def validate_synthesis_result(result: object) -> SpeechSynthesisResult:
    if not isinstance(result, SpeechSynthesisResult):
        raise ValueError("synthesizer returned invalid result type")
    if not isinstance(result.audio, (bytes, bytearray)):
        raise ValueError("synthesized audio must be bytes")
    audio = bytes(result.audio)
    if not audio:
        raise ValueError("synthesized audio is empty")
    if len(audio) > MAX_SYNTHESIZED_AUDIO_BYTES:
        raise ValueError("synthesized audio exceeds maximum size")
    media_type = str(result.media_type).split(";", 1)[0].strip().lower()
    if media_type not in ALLOWED_SYNTHESIZED_MEDIA_TYPES:
        raise ValueError("unsupported synthesized audio media type")
    return SpeechSynthesisResult(audio=audio, media_type=media_type)


def synthesize_checked(provider: SpeechSynthesizer, *, text: str) -> SpeechSynthesisResult:
    authoritative_text = validate_speech_text(text)
    return validate_synthesis_result(provider.synthesize(text=authoritative_text))
