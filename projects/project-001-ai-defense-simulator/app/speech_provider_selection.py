from __future__ import annotations

import os

from .groq_provider import load_groq_settings_from_env
from .groq_transcription import GroqTranscriber
from .openai_provider import load_openai_settings_from_env
from .openai_transcription import OpenAITranscriber


SUPPORTED_SPEECH_PROVIDERS = {"auto", "disabled", "openai", "groq"}


class SpeechProviderSelectionError(ValueError):
    pass


def build_speech_transcriber_from_env(*, selected_text_provider: str):
    selected = os.getenv("P001_SPEECH_PROVIDER", "auto").strip().lower()
    if selected not in SUPPORTED_SPEECH_PROVIDERS:
        allowed = ", ".join(sorted(SUPPORTED_SPEECH_PROVIDERS))
        raise SpeechProviderSelectionError(
            f"P001_SPEECH_PROVIDER must be one of: {allowed}"
        )
    if selected == "disabled":
        return None
    if selected == "groq" or (selected == "auto" and selected_text_provider == "groq"):
        return GroqTranscriber(load_groq_settings_from_env())

    openai_settings = load_openai_settings_from_env()
    if selected == "openai":
        if openai_settings is None:
            raise SpeechProviderSelectionError(
                "OpenAI speech was selected but P001_OPENAI_ENABLED is not set to 1"
            )
        return OpenAITranscriber(openai_settings)
    return OpenAITranscriber(openai_settings) if openai_settings is not None else None
