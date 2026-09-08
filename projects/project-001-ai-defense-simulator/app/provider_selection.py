from __future__ import annotations

from dataclasses import dataclass
import os

from .embeddings import EmbeddingProvider
from .evaluation import AnswerEvaluator
from .groq_provider import build_groq_text_providers_from_env
from .openai_provider import build_openai_providers_from_env
from .questioning import QuestionGenerator


SUPPORTED_AI_PROVIDERS = {"disabled", "openai", "groq"}


class AIProviderSelectionError(ValueError):
    pass


@dataclass(frozen=True)
class AIProviderBundle:
    selected_text_provider: str
    embedding_provider: EmbeddingProvider | None
    question_generator: QuestionGenerator | None
    answer_evaluator: AnswerEvaluator | None


def _selected_provider() -> str | None:
    raw = os.getenv("P001_AI_PROVIDER")
    if raw is None or not raw.strip():
        return None
    selected = raw.strip().lower()
    if selected not in SUPPORTED_AI_PROVIDERS:
        allowed = ", ".join(sorted(SUPPORTED_AI_PROVIDERS))
        raise AIProviderSelectionError(f"P001_AI_PROVIDER must be one of: {allowed}")
    return selected


def build_ai_provider_bundle_from_env() -> AIProviderBundle:
    """Build provider adapters without weakening legacy OpenAI configuration.

    If P001_AI_PROVIDER is unset, the existing P001_OPENAI_ENABLED behavior is preserved.
    Groq currently supplies text generation/evaluation only; semantic embeddings remain
    unavailable unless a separate embedding adapter is added later.
    """
    selected = _selected_provider()

    if selected is None:
        embedding, question, evaluator = build_openai_providers_from_env()
        return AIProviderBundle(
            selected_text_provider="openai" if question is not None else "disabled",
            embedding_provider=embedding,
            question_generator=question,
            answer_evaluator=evaluator,
        )

    if selected == "disabled":
        return AIProviderBundle("disabled", None, None, None)

    if selected == "openai":
        embedding, question, evaluator = build_openai_providers_from_env()
        if question is None or evaluator is None:
            raise AIProviderSelectionError(
                "OpenAI was selected but P001_OPENAI_ENABLED is not set to 1"
            )
        return AIProviderBundle("openai", embedding, question, evaluator)

    question, evaluator = build_groq_text_providers_from_env()
    return AIProviderBundle(
        selected_text_provider="groq",
        embedding_provider=None,
        question_generator=question,
        answer_evaluator=evaluator,
    )
