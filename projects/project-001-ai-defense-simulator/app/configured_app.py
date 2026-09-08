"""Application entrypoint that wires optional external providers from trusted environment config.

Run `uvicorn app.configured_app:app` when provider configuration should be applied.
The underlying `app.main` remains provider-neutral and testable without secrets.
"""

from . import main as runtime
from .openai_followup import OpenAIFollowUpGenerator
from .openai_provider import build_openai_providers_from_env, load_openai_settings_from_env
from .openai_speech_output import OpenAISpeechSynthesizer
from .openai_transcription import OpenAITranscriber
from .session_routes import build_session_router
from .speech_output_routes import build_speech_output_router
from .speech_routes import build_speech_router


embedding_provider, question_generator, answer_evaluator = build_openai_providers_from_env()
runtime.embedding_provider = embedding_provider
runtime.question_generator = question_generator
runtime.answer_evaluator = answer_evaluator

_openai_settings = load_openai_settings_from_env()
follow_up_generator = OpenAIFollowUpGenerator(_openai_settings) if _openai_settings is not None else None
speech_transcriber = OpenAITranscriber(_openai_settings) if _openai_settings is not None else None
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
