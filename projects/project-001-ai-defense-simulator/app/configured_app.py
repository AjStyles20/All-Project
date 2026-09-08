"""Application entrypoint that wires optional external providers from trusted environment config.

Run `uvicorn app.configured_app:app` when provider configuration should be applied.
The underlying `app.main` remains provider-neutral and testable without secrets.
"""

from . import main as runtime
from .openai_followup import OpenAIFollowUpGenerator
from .openai_provider import build_openai_providers_from_env, load_openai_settings_from_env
from .session_routes import build_session_router


embedding_provider, question_generator, answer_evaluator = build_openai_providers_from_env()
runtime.embedding_provider = embedding_provider
runtime.question_generator = question_generator
runtime.answer_evaluator = answer_evaluator

_openai_settings = load_openai_settings_from_env()
follow_up_generator = OpenAIFollowUpGenerator(_openai_settings) if _openai_settings is not None else None
runtime.app.include_router(build_session_router(runtime, follow_up_generator))

app = runtime.app
