from __future__ import annotations

import json
from typing import Any

import httpx

from .openai_provider import (
    OpenAIProviderSettings,
    ProviderRequestError,
    _OpenAIHTTPClient,
    _extract_output_text,
)
from .sessions import FOLLOW_UP_TYPES, FollowUpRequest, FollowUpResult


_FOLLOWUP_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["follow_up_type", "rationale", "question"],
    "properties": {
        "follow_up_type": {"type": "string", "enum": sorted(FOLLOW_UP_TYPES)},
        "rationale": {"type": "string"},
        "question": {"type": ["string", "null"]},
    },
}


def _followup_input(request: FollowUpRequest) -> str:
    data = {
        "session_id": request.session_id,
        "turn_index": request.turn_index,
        "reviewer_role": request.reviewer_role,
        "topic": request.topic,
        "prior_question_id": request.prior_question_id,
        "prior_question": request.prior_question,
        "prior_answer": request.prior_answer,
        "feedback": list(request.feedback),
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
    return "UNTRUSTED_FOLLOWUP_CONTEXT_JSON:\n" + json.dumps(
        data, ensure_ascii=False, separators=(",", ":")
    )


class OpenAIFollowUpGenerator:
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

    def generate_follow_up(self, request: FollowUpRequest) -> FollowUpResult:
        payload = {
            "model": self.model_name,
            "instructions": request.trusted_policy,
            "input": _followup_input(request),
            "max_output_tokens": 700,
            "store": False,
            "tools": [],
            "tool_choice": "none",
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "project001_defense_followup",
                    "strict": True,
                    "schema": _FOLLOWUP_SCHEMA,
                }
            },
        }
        output_text = _extract_output_text(self._http.post_json("/responses", payload))
        try:
            parsed = json.loads(output_text)
        except json.JSONDecodeError as exc:
            raise ProviderRequestError("provider returned invalid structured follow-up JSON") from exc
        if not isinstance(parsed, dict):
            raise ProviderRequestError("provider returned invalid structured follow-up")

        follow_up_type = parsed.get("follow_up_type")
        rationale = parsed.get("rationale")
        question = parsed.get("question")
        if not isinstance(follow_up_type, str) or not isinstance(rationale, str):
            raise ProviderRequestError("provider returned malformed follow-up fields")
        if question is not None and not isinstance(question, str):
            raise ProviderRequestError("provider returned malformed follow-up question")

        return FollowUpResult(
            follow_up_type=follow_up_type,
            rationale=rationale,
            question=question,
        )
