from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from .speech_output import SpeechSynthesizer, synthesize_checked


def build_speech_output_router(runtime, synthesizer: SpeechSynthesizer | None) -> APIRouter:
    router = APIRouter()

    @router.post("/api/workspaces/{workspace_id}/questions/{question_id}/speech")
    def synthesize_question(workspace_id: str, question_id: str):
        if not runtime.db.workspace_exists(workspace_id):
            raise HTTPException(status_code=404, detail="Workspace not found")
        try:
            question = runtime.get_question(runtime.db, workspace_id=workspace_id, question_id=question_id)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail="Question provenance could not be verified safely") from exc
        if question is None:
            raise HTTPException(status_code=404, detail="Question not found in workspace")
        if synthesizer is None:
            raise HTTPException(status_code=503, detail="Reviewer speech output is not configured")

        try:
            result = synthesize_checked(synthesizer, text=question.question_text)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail="Reviewer question could not be synthesized safely") from exc
        except Exception as exc:
            raise HTTPException(status_code=502, detail="Speech synthesis provider failed") from exc

        return Response(
            content=result.audio,
            media_type=result.media_type,
            headers={
                "Cache-Control": "no-store",
                "X-P001-Audio-Persisted": "false",
            },
        )

    return router
