import pytest

from app.groq_provider import DEFAULT_GROQ_TEXT_MODEL
from app.provider_selection import (
    AIProviderSelectionError,
    build_ai_provider_bundle_from_env,
)


OPENAI_TEST_KEY = "sk-test-secret"
GROQ_TEST_KEY = "gsk-test-secret"


def clear_provider_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "P001_AI_PROVIDER",
        "P001_OPENAI_ENABLED",
        "P001_OPENAI_API_KEY",
        "P001_GROQ_API_KEY",
        "P001_GROQ_TEXT_MODEL",
        "P001_GROQ_TIMEOUT_SECONDS",
    ):
        monkeypatch.delenv(name, raising=False)


def test_unset_selector_preserves_disabled_legacy_default(monkeypatch: pytest.MonkeyPatch):
    clear_provider_env(monkeypatch)
    bundle = build_ai_provider_bundle_from_env()
    assert bundle.selected_text_provider == "disabled"
    assert bundle.embedding_provider is None
    assert bundle.question_generator is None
    assert bundle.answer_evaluator is None
    assert bundle.follow_up_generator is None


def test_unset_selector_preserves_existing_openai_enablement(monkeypatch: pytest.MonkeyPatch):
    clear_provider_env(monkeypatch)
    monkeypatch.setenv("P001_OPENAI_ENABLED", "1")
    monkeypatch.setenv("P001_OPENAI_API_KEY", OPENAI_TEST_KEY)
    bundle = build_ai_provider_bundle_from_env()
    assert bundle.selected_text_provider == "openai"
    assert bundle.embedding_provider is not None
    assert bundle.question_generator is not None
    assert bundle.answer_evaluator is not None
    assert bundle.follow_up_generator is not None
    assert bundle.question_generator.provider_name == "openai"
    assert bundle.follow_up_generator.provider_name == "openai"


def test_explicit_disabled_overrides_legacy_openai_setting(monkeypatch: pytest.MonkeyPatch):
    clear_provider_env(monkeypatch)
    monkeypatch.setenv("P001_AI_PROVIDER", "disabled")
    monkeypatch.setenv("P001_OPENAI_ENABLED", "1")
    monkeypatch.setenv("P001_OPENAI_API_KEY", OPENAI_TEST_KEY)
    bundle = build_ai_provider_bundle_from_env()
    assert bundle.selected_text_provider == "disabled"
    assert bundle.question_generator is None
    assert bundle.follow_up_generator is None


def test_explicit_openai_requires_existing_openai_enablement(monkeypatch: pytest.MonkeyPatch):
    clear_provider_env(monkeypatch)
    monkeypatch.setenv("P001_AI_PROVIDER", "openai")
    with pytest.raises(AIProviderSelectionError):
        build_ai_provider_bundle_from_env()


def test_groq_selection_builds_text_and_followup_providers_without_claiming_embeddings(monkeypatch: pytest.MonkeyPatch):
    clear_provider_env(monkeypatch)
    monkeypatch.setenv("P001_AI_PROVIDER", "groq")
    monkeypatch.setenv("P001_GROQ_API_KEY", GROQ_TEST_KEY)
    bundle = build_ai_provider_bundle_from_env()
    assert bundle.selected_text_provider == "groq"
    assert bundle.embedding_provider is None
    assert bundle.question_generator is not None
    assert bundle.answer_evaluator is not None
    assert bundle.follow_up_generator is not None
    assert bundle.question_generator.provider_name == "groq"
    assert bundle.question_generator.model_name == DEFAULT_GROQ_TEXT_MODEL
    assert bundle.follow_up_generator.provider_name == "groq"
    assert bundle.follow_up_generator.model_name == DEFAULT_GROQ_TEXT_MODEL


def test_invalid_provider_name_fails_closed(monkeypatch: pytest.MonkeyPatch):
    clear_provider_env(monkeypatch)
    monkeypatch.setenv("P001_AI_PROVIDER", "https://evil.example")
    with pytest.raises(AIProviderSelectionError):
        build_ai_provider_bundle_from_env()
