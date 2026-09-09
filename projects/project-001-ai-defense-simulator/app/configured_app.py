"""Application entrypoint that wires optional external providers from trusted environment config.

Run `uvicorn app.configured_app:app` when provider configuration should be applied.
The underlying `app.main` remains provider-neutral and testable without secrets.
"""

from . import main as runtime
from .openai_provider import load_openai_settings_from_env
from .openai_speech_output import OpenAISpeechSynthesizer
from .provider_selection import build_ai_provider_bundle_from_env
from .session_routes import build_session_router
from .speech_output_routes import build_speech_output_router
from .speech_provider_selection import build_speech_transcriber_from_env
from .speech_routes import build_speech_router


_ai_bundle = build_ai_provider_bundle_from_env()
runtime.embedding_provider = _ai_bundle.embedding_provider
runtime.question_generator = _ai_bundle.question_generator
runtime.answer_evaluator = _ai_bundle.answer_evaluator
follow_up_generator = _ai_bundle.follow_up_generator

speech_transcriber = build_speech_transcriber_from_env(
    selected_text_provider=_ai_bundle.selected_text_provider
)

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
    response.headers["Permissions-Policy"] = "camera=(), microphone=(self), geolocation=()"
    return response


@runtime.app.middleware("http")
async def normalize_null_origin_for_same_origin_navigation(request, call_next):
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
