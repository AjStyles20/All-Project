from __future__ import annotations

from dataclasses import dataclass
import json
import os
from typing import Any

import httpx

from .embeddings import embed_checked
from .evaluation import (
    FEEDBACK_CATEGORIES,
    FEEDBACK_STATUSES,
    EvaluationRequest,
    EvaluationResult,
    FeedbackItem,
)
from .questioning import QuestionGenerationRequest


OPENAI_API_BASE = "https://api.openai.com/v1"
DEFAULT_TEXT_MODEL = "gpt-5.6-luna"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_TIMEOUT_SECONDS = 20.0
MIN_TIMEOUT_SECONDS = 2.0
MAX_TIMEOUT_SECONDS = 60.0
MAX_MODEL_ID_CHARS = 200
MAX_EMBED_BATCH = 64
MAX_EMBED_TEXT_CHARS = 12000


class ProviderConfigurationError(ValueError):
    pass


class ProviderRequestError(RuntimeError):
    pass


@dataclass(frozen=True)
class OpenAIProviderSettings:
    api_key: str
    text_model: str = DEFAULT_TEXT_MODEL
    embedding_model: str = DEFAULT_EMBEDDING_MODEL
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS


def _bounded_model(value: str, *, field: str) -> str:
    cleaned = value.strip()
    if not cleaned or len(cleaned) > MAX_MODEL_ID_CHARS:
        raise ProviderConfigurationError(f"invalid {field}")
    return cleaned


def load_openai_settings_from_env() -> OpenAIProviderSettings | None:
    enabled = os.getenv("P001_OPENAI_ENABLED", "0").strip()
    if enabled not in {"0", "1"}:
        raise ProviderConfigurationError("P001_OPENAI_ENABLED must be 0 or 1")
    if enabled != "1":
        return None

    api_key = os.getenv("P001_OPENAI_API_KEY", "").strip()
    if not api_key:
        raise ProviderConfigurationError("OpenAI provider is enabled but API key is missing")
    if len(api_key) > 4096:
        raise ProviderConfigurationError("OpenAI API key is invalid")

    text_model = _bounded_model(
        os.getenv("P001_OPENAI_TEXT_MODEL", DEFAULT_TEXT_MODEL),
        field="OpenAI text model",
    )
    embedding_model = _bounded_model(
        os.getenv("P001_OPENAI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL),
        field="OpenAI embedding model",
    )
    raw_timeout = os.getenv("P001_OPENAI_TIMEOUT_SECONDS", str(DEFAULT_TIMEOUT_SECONDS)).strip()
    try:
        timeout = float(raw_timeout)
    except ValueError as exc:
        raise ProviderConfigurationError("OpenAI timeout must be numeric") from exc
    if timeout < MIN_TIMEOUT_SECONDS or timeout > MAX_TIMEOUT_SECONDS:
        raise ProviderConfigurationError(
            f"OpenAI timeout must be between {MIN_TIMEOUT_SECONDS:g} and {MAX_TIMEOUT_SECONDS:g} seconds"
        )

    return OpenAIProviderSettings(
        api_key=api_key,
        text_model=text_model,
        embedding_model=embedding_model,
        timeout_seconds=timeout,
    )


class _OpenAIHTTPClient:
    def __init__(
        self,
        settings: OpenAIProviderSettings,
        *,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._settings = settings
        self._client = httpx.Client(
            base_url=OPENAI_API_BASE,
            headers={
                "Authorization": f"Bearer {settings.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "project-001/0.7",
            },
            timeout=httpx.Timeout(settings.timeout_seconds),
            transport=transport,
            follow_redirects=False,
        )

    def close(self) -> None:
        self._client.close()

    def post_json(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        if path not in {"/responses", "/embeddings"}:
            raise ProviderRequestError("provider endpoint is not allowed")
        try:
            response = self._client.post(path, json=payload)
        except httpx.TimeoutException as exc:
            raise ProviderRequestError("provider request timed out") from exc
        except httpx.RequestError as exc:
            raise ProviderRequestError("provider request failed") from exc

        if response.status_code < 200 or response.status_code >= 300:
            # Do not include response bodies, request headers, or credentials in the exception.
            raise ProviderRequestError(f"provider returned HTTP {response.status_code}")
        try:
            data = response.json()
        except ValueError as exc:
            raise ProviderRequestError("provider returned invalid JSON") from exc
        if not isinstance(data, dict):
            raise ProviderRequestError("provider returned an invalid response object")
        return data


class OpenAIEmbeddingProvider:
    provider_name = "openai"
    model_version = None

    def __init__(
        self,
        settings: OpenAIProviderSettings,
        *,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.model_name = settings.embedding_model
        self._http = _OpenAIHTTPClient(settings, transport=transport)

    def close(self) -> None:
        self._http.close()

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        if len(texts) > MAX_EMBED_BATCH:
            raise ValueError("embedding batch exceeds maximum size")
        normalized: list[str] = []
        for text in texts:
            if not isinstance(text, str):
                raise ValueError("embedding input must be text")
            cleaned = text.strip()
            if not cleaned or len(cleaned) > MAX_EMBED_TEXT_CHARS:
                raise ValueError("embedding input is empty or too long")
            normalized.append(cleaned)

        payload = {
            "model": self.model_name,
            "input": normalized,
            "encoding_format": "float",
        }
        data = self._http.post_json("/embeddings", payload)
        rows = data.get("data")
        if not isinstance(rows, list) or len(rows) != len(normalized):
            raise ProviderRequestError("embedding provider returned unexpected result count")

        ordered: list[list[float] | None] = [None] * len(normalized)
        for row in rows:
            if not isinstance(row, dict):
                raise ProviderRequestError("embedding provider returned malformed data")
            index = row.get("index")
            vector = row.get("embedding")
            if not isinstance(index, int) or index < 0 or index >= len(ordered):
                raise ProviderRequestError("embedding provider returned invalid index")
            if ordered[index] is not None or not isinstance(vector, list):
                raise ProviderRequestError("embedding provider returned malformed vector")
            ordered[index] = vector
        if any(vector is None for vector in ordered):
            raise ProviderRequestError("embedding provider returned incomplete data")
        return [list(vector) for vector in ordered if vector is not None]


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


def _extract_output_text(data: dict[str, Any]) -> str:
    value = data.get("output_text")
    if isinstance(value, str) and value.strip():
        return value

    output = data.get("output")
    if not isinstance(output, list):
        raise ProviderRequestError("provider response contains no output text")
    pieces: list[str] = []
    for item in output:
        if not isinstance(item, dict) or item.get("type") != "message":
            continue
        content = item.get("content")
        if not isinstance(content, list):
            continue
        for part in content:
            if isinstance(part, dict) and part.get("type") == "output_text" and isinstance(part.get("text"), str):
                pieces.append(part["text"])
    text = "\n".join(pieces).strip()
    if not text:
        raise ProviderRequestError("provider response contains no output text")
    return text


class OpenAIQuestionGenerator:
    provider_name = "openai"
    model_version = None

    def __init__(
        self,
        settings: OpenAIProviderSettings,
        *,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.model_name = settings.text_model
        self._http = _OpenAIHTTPClient(settings, transport=transport)

    def close(self) -> None:
        self._http.close()

    def generate(self, request: QuestionGenerationRequest) -> str:
        payload = {
            "model": self.model_name,
            "instructions": request.trusted_policy,
            "input": _question_input(request),
            "max_output_tokens": 300,
            "store": False,
            "tools": [],
            "tool_choice": "none",
        }
        return _extract_output_text(self._http.post_json("/responses", payload))


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


class OpenAIAnswerEvaluator:
    provider_name = "openai"
    model_version = None

    def __init__(
        self,
        settings: OpenAIProviderSettings,
        *,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.model_name = settings.text_model
        self._http = _OpenAIHTTPClient(settings, transport=transport)

    def close(self) -> None:
        self._http.close()

    def evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        payload = {
            "model": self.model_name,
            "instructions": request.trusted_policy,
            "input": _evaluation_input(request),
            "max_output_tokens": 1800,
            "store": False,
            "tools": [],
            "tool_choice": "none",
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "project001_answer_evaluation",
                    "strict": True,
                    "schema": _EVALUATION_SCHEMA,
                }
            },
        }
        output_text = _extract_output_text(self._http.post_json("/responses", payload))
        try:
            parsed = json.loads(output_text)
        except json.JSONDecodeError as exc:
            raise ProviderRequestError("provider returned invalid structured evaluation JSON") from exc
        if not isinstance(parsed, dict):
            raise ProviderRequestError("provider returned invalid structured evaluation")
        summary = parsed.get("summary")
        feedback_raw = parsed.get("feedback")
        if not isinstance(summary, str) or not isinstance(feedback_raw, list):
            raise ProviderRequestError("provider returned invalid structured evaluation")
        feedback: list[FeedbackItem] = []
        for item in feedback_raw:
            if not isinstance(item, dict):
                raise ProviderRequestError("provider returned malformed feedback item")
            refs = item.get("evidence_chunk_ids")
            if not isinstance(refs, list) or not all(isinstance(ref, str) for ref in refs):
                raise ProviderRequestError("provider returned malformed evidence references")
            feedback.append(
                FeedbackItem(
                    category=str(item.get("category", "")),
                    status=str(item.get("status", "")),
                    explanation=str(item.get("explanation", "")),
                    evidence_chunk_ids=tuple(refs),
                )
            )
        return EvaluationResult(summary=summary, feedback=tuple(feedback))


def build_openai_providers_from_env() -> tuple[
    OpenAIEmbeddingProvider | None,
    OpenAIQuestionGenerator | None,
    OpenAIAnswerEvaluator | None,
]:
    settings = load_openai_settings_from_env()
    if settings is None:
        return None, None, None
    return (
        OpenAIEmbeddingProvider(settings),
        OpenAIQuestionGenerator(settings),
        OpenAIAnswerEvaluator(settings),
    )
