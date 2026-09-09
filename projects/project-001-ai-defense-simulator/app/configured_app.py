"""Application entrypoint that wires optional external providers from trusted environment config.

Run `uvicorn app.configured_app:app` when provider configuration should be applied.
The underlying `app.main` remains provider-neutral and testable without secrets.
"""

import os

from . import main as runtime
from .groq_provider import load_groq_settings_from_env
from .groq_transcription import GroqTranscriber
from .openai_provider import load_openai_settings_from_env
from .openai_speech_output import OpenAISpeechSynthesizer
from .openai_transcription import OpenAITranscriber
from .provider_selection import build_ai_provider_bundle_from_env
from .session_routes import build_session_router
from .speech_output_routes import build_speech_output_router
from .speech_routes import build_speech_router


_ai_bundle = build_ai_provider_bundle_from_env()
runtime.embedding_provider = _ai_bundle.embedding_provider
runtime.question_generator = _ai_bundle.question_generator
runtime.answer_evaluator = _ai_bundle.answer_evaluator
follow_up_generator = _ai_bundle.follow_up_generator


def _build_speech_transcriber():
    selected = os.getenv("P001_SPEECH_PROVIDER", "auto").strip().lower()
    if selected not in {"auto", "disabled", "openai", "groq"}:
        raise ValueError("P001_SPEECH_PROVIDER must be one of: auto, disabled, groq, openai")
    if selected == "disabled":
        return None
    if selected == "groq" or (selected == "auto" and _ai_bundle.selected_text_provider == "groq"):
        return GroqTranscriber(load_groq_settings_from_env())

    openai_settings = load_openai_settings_from_env()
    if selected == "openai":
        if openai_settings is None:
            raise ValueError("OpenAI speech was selected but P001_OPENAI_ENABLED is not set to 1")
        return OpenAITranscriber(openai_settings)
    return OpenAITranscriber(openai_settings) if openai_settings is not None else None


speech_transcriber = _build_speech_transcriber()

# Feature 010 TTS remains independently OpenAI-backed. Feature 013 changes STT only.
_openai_settings = load_openai_settings_from_env()
speech_synthesizer = OpenAISpeechSynthesizer(_openai_settings) if _openai_settings is not None else None

# Template disclosure is intentionally provider identity only; no credential/config internals are exposed.
runtime.templates.env.globals["speech_provider_name"] = (
    str(speech_transcriber.provider_name) if speech_transcriber is not None else None
)
runtime.templates.env.globals["speech_model_name"] = (
    str(speech_transcriber.model_name) if speech_transcriber is not None else None
)
runtime.templates.env.globals["tts_provider_name"] = (
    str(speech_synthesizer.provider_name) if speech_synthesizer is not None else None
)
runtime.templates.env.globals["tts_model_name"] = (
    str(speech_synthesizer.model_name) if speech_synthesizer is not None else None
)
runtime.templates.env.globals["tts_voice_name"] = (
    str(speech_synthesizer.voice_name) if speech_synthesizer is not None else None
)

runtime.app.include_router(build_session_router(runtime, follow_up_generator))
runtime.app.include_router(build_speech_router(runtime, speech_transcriber))
runtime.app.include_router(build_speech_output_router(runtime, speech_synthesizer))


@runtime.app.middleware("http")
async def same_origin_microphone_policy(request, call_next):
    response = await call_next(request)
    # Feature 006 denied microphone globally. Feature 009 relaxes only microphone to same-origin;
    # camera/geolocation remain disabled and browser permission is still required per recording.
    response.headers["Permissions-Policy"] = "camera=(), microphone=(self), geolocation=()"
    return response


@runtime.app.middleware("http")
async def normalize_null_origin_for_same_origin_navigation(request, call_next):
    """Handle browsers that emit ``Origin: null`` for a verified same-origin form navigation.

    The underlying security guard still rejects ``Sec-Fetch-Site: cross-site`` and explicit
    non-null origin/host mismatches. We only remove the opaque ``null`` origin when the browser
    independently reports the request as same-origin.
    """
    if request.method.upper() in {"POST", "PUT", "PATCH", "DELETE"}:
        fetch_site = request.headers.get("sec-fetch-site", "").lower()
        origin = request.headers.get("origin", "").lower()
        if fetch_site == "same-origin" and origin == "null":
            request.scope["headers"] = [
                (name, value)
                for name, value in request.scope.get("headers", [])
                if name.lower() != b"origin"
            ]

    return await call_next(request)


app = runtime.app
