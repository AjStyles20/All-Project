"""Application entrypoint that wires optional external providers from trusted environment config.

Run `uvicorn app.configured_app:app` when provider configuration should be applied.
The underlying `app.main` remains provider-neutral and testable without secrets.
"""

from . import main as runtime
from .openai_provider import build_openai_providers_from_env


embedding_provider, question_generator, answer_evaluator = build_openai_providers_from_env()
runtime.embedding_provider = embedding_provider
runtime.question_generator = question_generator
runtime.answer_evaluator = answer_evaluator

app = runtime.app
