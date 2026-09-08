from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile

from .speech import MAX_AUDIO_BYTES, SpeechTranscriber, transcribe_checked


def build_speech_router(runtime, transcriber: SpeechTranscriber | None) -> APIRouter:
    router = APIRouter()

    @router.post("/api/workspaces/{workspace_id}/questions/{question_id}/transcriptions")
    async def transcribe_answer(
        workspace_id: str,
        question_id: str,
        audio: UploadFile = File(...),
    ) -> dict:
        if not runtime.db.workspace_exists(workspace_id):
            raise HTTPException(status_code=404, detail="Workspace not found")
        try:
            question = runtime.get_question(runtime.db, workspace_id=workspace_id, question_id=question_id)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail="Question provenance could not be verified safely") from exc
        if question is None:
            raise HTTPException(status_code=404, detail="Question not found in workspace")
        if transcriber is None:
            raise HTTPException(status_code=503, detail="Speech transcription is not configured")

        content_type = (audio.content_type or "").strip().lower()
        data = await audio.read(MAX_AUDIO_BYTES + 1)
        if len(data) > MAX_AUDIO_BYTES:
            raise HTTPException(status_code=413, detail="Audio exceeds configured upload limit")

        try:
            result = transcribe_checked(transcriber, audio=data, media_type=content_type)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail="Audio could not be transcribed safely") from exc
        except Exception as exc:
            raise HTTPException(status_code=502, detail="Speech transcription provider failed") from exc

        return {
            "workspace_id": workspace_id,
            "question_id": question_id,
            "transcript": result.text,
            "language": result.language,
            "provider": {
                "name": str(transcriber.provider_name),
                "model": str(transcriber.model_name),
            },
            "submitted_as_answer": False,
            "audio_persisted": False,
        }

    return router
