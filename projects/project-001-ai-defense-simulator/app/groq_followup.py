from __future__ import annotations

import json
from typing import Any

import httpx

from .groq_provider import (
    GroqProviderRequestError,
    GroqProviderSettings,
    _GroqHTTPClient,
    _extract_chat_text,
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

GROQ_FOLLOWUP_GROUNDING_GUARD = (
    "Do not infer a categorical negative or exclusion merely because the evidence omits an item or "
    "places concepts under separate headings. When the evidence only distinguishes or separately labels "
    "concepts, ask the user to compare or distinguish those concepts rather than asserting that one is not "
    "part of another. A negative premise in a follow-up question must itself be directly supported by the evidence."
)


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


class GroqFollowUpGenerator:
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

    def generate_follow_up(self, request: FollowUpRequest) -> FollowUpResult:
        system_policy = f"{request.trusted_policy} {GROQ_FOLLOWUP_GROUNDING_GUARD}"
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_policy},
                {"role": "user", "content": _followup_input(request)},
            ],
            "max_completion_tokens": 700,
            "temperature": 0,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "project001_defense_followup",
                    "strict": True,
                    "schema": _FOLLOWUP_SCHEMA,
                },
            },
        }
        output_text = _extract_chat_text(self._http.post_json("/chat/completions", payload))
        try:
            parsed = json.loads(output_text)
        except json.JSONDecodeError as exc:
            raise GroqProviderRequestError("provider returned invalid structured follow-up JSON") from exc
        if not isinstance(parsed, dict):
            raise GroqProviderRequestError("provider returned invalid structured follow-up")

        follow_up_type = parsed.get("follow_up_type")
        rationale = parsed.get("rationale")
        question = parsed.get("question")
        if not isinstance(follow_up_type, str) or not isinstance(rationale, str):
            raise GroqProviderRequestError("provider returned malformed follow-up fields")
        if question is not None and not isinstance(question, str):
            raise GroqProviderRequestError("provider returned malformed follow-up question")

        return FollowUpResult(
            follow_up_type=follow_up_type,
            rationale=rationale,
            question=question,
        )
