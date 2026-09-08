from __future__ import annotations

from dataclasses import dataclass
import json
import os
from typing import Any

import httpx

from .evaluation import (
    FEEDBACK_CATEGORIES,
    FEEDBACK_STATUSES,
    EvaluationRequest,
    EvaluationResult,
    FeedbackItem,
)
from .questioning import QuestionGenerationRequest


GROQ_API_BASE = "https://api.groq.com/openai/v1"
DEFAULT_GROQ_TEXT_MODEL = "openai/gpt-oss-20b"
DEFAULT_TIMEOUT_SECONDS = 20.0
MIN_TIMEOUT_SECONDS = 2.0
MAX_TIMEOUT_SECONDS = 60.0
MAX_MODEL_ID_CHARS = 200


class GroqProviderConfigurationError(ValueError):
    pass


class GroqProviderRequestError(RuntimeError):
    pass


@dataclass(frozen=True)
class GroqProviderSettings:
    api_key: str
    text_model: str = DEFAULT_GROQ_TEXT_MODEL
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS


def _bounded_model(value: str) -> str:
    cleaned = value.strip()
    if not cleaned or len(cleaned) > MAX_MODEL_ID_CHARS:
        raise GroqProviderConfigurationError("invalid Groq text model")
    return cleaned


def load_groq_settings_from_env() -> GroqProviderSettings:
    api_key = os.getenv("P001_GROQ_API_KEY", "").strip()
    if not api_key:
        raise GroqProviderConfigurationError("Groq provider is selected but API key is missing")
    if len(api_key) > 4096:
        raise GroqProviderConfigurationError("Groq API key is invalid")

    text_model = _bounded_model(os.getenv("P001_GROQ_TEXT_MODEL", DEFAULT_GROQ_TEXT_MODEL))
    raw_timeout = os.getenv("P001_GROQ_TIMEOUT_SECONDS", str(DEFAULT_TIMEOUT_SECONDS)).strip()
    try:
        timeout = float(raw_timeout)
    except ValueError as exc:
        raise GroqProviderConfigurationError("Groq timeout must be numeric") from exc
    if timeout < MIN_TIMEOUT_SECONDS or timeout > MAX_TIMEOUT_SECONDS:
        raise GroqProviderConfigurationError(
            f"Groq timeout must be between {MIN_TIMEOUT_SECONDS:g} and {MAX_TIMEOUT_SECONDS:g} seconds"
        )

    return GroqProviderSettings(api_key=api_key, text_model=text_model, timeout_seconds=timeout)


class _GroqHTTPClient:
    def __init__(
        self,
        settings: GroqProviderSettings,
        *,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._client = httpx.Client(
            base_url=GROQ_API_BASE,
            headers={
                "Authorization": f"Bearer {settings.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "project-001/0.8",
            },
            timeout=httpx.Timeout(settings.timeout_seconds),
            transport=transport,
            follow_redirects=False,
        )

    def close(self) -> None:
        self._client.close()

    def post_json(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        if path != "/chat/completions":
            raise GroqProviderRequestError("provider endpoint is not allowed")
        try:
            response = self._client.post(path, json=payload)
        except httpx.TimeoutException as exc:
            raise GroqProviderRequestError("provider request timed out") from exc
        except httpx.RequestError as exc:
            raise GroqProviderRequestError("provider request failed") from exc

        if response.status_code < 200 or response.status_code >= 300:
            # Never surface response bodies, request headers, or credentials.
            raise GroqProviderRequestError(f"provider returned HTTP {response.status_code}")
        try:
            data = response.json()
        except ValueError as exc:
            raise GroqProviderRequestError("provider returned invalid JSON") from exc
        if not isinstance(data, dict):
            raise GroqProviderRequestError("provider returned an invalid response object")
        return data


def _question_input(request: QuestionGenerationRequest) -> str:
    data = {
        "reviewer_role": request.reviewer_role,
        "topic": request.topic,
        "evidence": [
            {
                "chunk_id": item.chunk_id,
                "document_id": item.document_id,
                "filename": item.filename,
                "locator": item.locator,
                "text": item.text,
            }
            for item in request.evidence
        ],
    }
    return "UNTRUSTED_REVIEW_CONTEXT_JSON:\n" + json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def _evaluation_input(request: EvaluationRequest) -> str:
    data = {
        "question_id": request.question_id,
        "reviewer_role": request.reviewer_role,
        "topic": request.topic,
        "question": request.question_text,
        "answer": request.answer,
        "evidence": [
            {
                "chunk_id": item.chunk_id,
                "document_id": item.document_id,
                "filename": item.filename,
                "locator": item.locator,
                "text": item.text,
            }
            for item in request.evidence
        ],
    }
    return "UNTRUSTED_EVALUATION_CONTEXT_JSON:\n" + json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def _extract_chat_text(data: dict[str, Any]) -> str:
    choices = data.get("choices")
    if not isinstance(choices, list) or not choices:
        raise GroqProviderRequestError("provider response contains no completion choice")
    first = choices[0]
    if not isinstance(first, dict):
        raise GroqProviderRequestError("provider response contains malformed completion data")
    message = first.get("message")
    if not isinstance(message, dict):
        raise GroqProviderRequestError("provider response contains malformed message data")
    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        raise GroqProviderRequestError("provider response contains no output text")
    return content.strip()


class GroqQuestionGenerator:
    provider_name = "groq"
    model_version = None

    def __init__(
        self,
        settings: GroqProviderSettings,
        *,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.model_name = settings.text_model
        self._http = _GroqHTTPClient(settings, transport=transport)

    def close(self) -> None:
        self._http.close()

    def generate(self, request: QuestionGenerationRequest) -> str:
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": request.trusted_policy},
                {"role": "user", "content": _question_input(request)},
            ],
            "max_completion_tokens": 300,
            "temperature": 0.2,
        }
        return _extract_chat_text(self._http.post_json("/chat/completions", payload))


_EVALUATION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["summary", "feedback"],
    "properties": {
        "summary": {"type": "string"},
        "feedback": {
            "type": "array",
            "minItems": len(FEEDBACK_CATEGORIES),
            "maxItems": len(FEEDBACK_CATEGORIES),
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["category", "status", "explanation", "evidence_chunk_ids"],
                "properties": {
                    "category": {"type": "string", "enum": list(FEEDBACK_CATEGORIES)},
                    "status": {"type": "string", "enum": sorted(FEEDBACK_STATUSES)},
                    "explanation": {"type": "string"},
                    "evidence_chunk_ids": {
                        "type": "array",
                        "maxItems": 8,
                        "items": {"type": "string"},
                    },
                },
            },
        },
    },
}


class GroqAnswerEvaluator:
    provider_name = "groq"
    model_version = None

    def __init__(
        self,
        settings: GroqProviderSettings,
        *,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.model_name = settings.text_model
        self._http = _GroqHTTPClient(settings, transport=transport)

    def close(self) -> None:
        self._http.close()

    def evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": request.trusted_policy},
                {"role": "user", "content": _evaluation_input(request)},
            ],
            "max_completion_tokens": 1800,
            "temperature": 0,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "project001_answer_evaluation",
                    "strict": True,
                    "schema": _EVALUATION_SCHEMA,
                },
            },
        }
        output_text = _extract_chat_text(self._http.post_json("/chat/completions", payload))
        try:
            parsed = json.loads(output_text)
        except json.JSONDecodeError as exc:
            raise GroqProviderRequestError("provider returned invalid structured evaluation JSON") from exc
        if not isinstance(parsed, dict):
            raise GroqProviderRequestError("provider returned invalid structured evaluation")
        summary = parsed.get("summary")
        feedback_raw = parsed.get("feedback")
        if not isinstance(summary, str) or not isinstance(feedback_raw, list):
            raise GroqProviderRequestError("provider returned invalid structured evaluation")

        feedback: list[FeedbackItem] = []
        for item in feedback_raw:
            if not isinstance(item, dict):
                raise GroqProviderRequestError("provider returned malformed feedback item")
            refs = item.get("evidence_chunk_ids")
            if not isinstance(refs, list) or not all(isinstance(ref, str) for ref in refs):
                raise GroqProviderRequestError("provider returned malformed evidence references")
            feedback.append(
                FeedbackItem(
                    category=str(item.get("category", "")),
                    status=str(item.get("status", "")),
                    explanation=str(item.get("explanation", "")),
                    evidence_chunk_ids=tuple(refs),
                )
            )
        return EvaluationResult(summary=summary, feedback=tuple(feedback))


def build_groq_text_providers_from_env() -> tuple[GroqQuestionGenerator, GroqAnswerEvaluator]:
    settings = load_groq_settings_from_env()
    return GroqQuestionGenerator(settings), GroqAnswerEvaluator(settings)
