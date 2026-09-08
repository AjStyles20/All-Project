from __future__ import annotations

from fastapi import APIRouter, Form, HTTPException, Request

from .sessions import (
    FollowUpGenerator,
    attach_initial_question,
    create_session,
    ensure_session_schema,
    generate_follow_up,
)


def _session_snapshot(database, *, workspace_id: str, session_id: str) -> dict | None:
    ensure_session_schema(database)
    with database.connect() as connection:
        session = connection.execute(
            "SELECT id, workspace_id, reviewer_role, topic, status, max_turns, created_at, completed_at "
            "FROM practice_sessions WHERE id = ? AND workspace_id = ?",
            (session_id, workspace_id),
        ).fetchone()
        if session is None:
            return None
        rows = connection.execute(
            """
            SELECT pst.turn_index, pst.question_id, pst.parent_question_id, pst.follow_up_type,
                   pst.rationale, pst.created_at, gq.question_text,
                   EXISTS(
                       SELECT 1 FROM answer_evaluations ae
                       WHERE ae.question_id = gq.id AND ae.workspace_id = ?
                   ) AS answered
            FROM practice_session_turns pst
            JOIN generated_questions gq ON gq.id = pst.question_id
            WHERE pst.session_id = ? AND gq.workspace_id = ?
            ORDER BY pst.turn_index ASC
            """,
            (workspace_id, session_id, workspace_id),
        ).fetchall()
    return {
        "id": session["id"],
        "workspace_id": session["workspace_id"],
        "reviewer_role": session["reviewer_role"],
        "topic": session["topic"],
        "status": session["status"],
        "max_turns": session["max_turns"],
        "created_at": session["created_at"],
        "completed_at": session["completed_at"],
        "turns": [dict(row) for row in rows],
    }


def build_session_router(runtime, follow_up_generator: FollowUpGenerator | None) -> APIRouter:
    router = APIRouter()

    @router.post("/api/workspaces/{workspace_id}/sessions")
    def api_create_session(
        workspace_id: str,
        topic: str = Form(...),
        reviewer_role: str = Form(...),
        retrieval_mode: str = Form("hybrid"),
        max_turns: int = Form(5),
    ) -> dict:
        if not runtime.db.workspace_exists(workspace_id):
            raise HTTPException(status_code=404, detail="Workspace not found")
        if runtime.question_generator is None:
            raise HTTPException(status_code=503, detail="Question generation is not configured")
        try:
            session = create_session(
                runtime.db,
                workspace_id=workspace_id,
                reviewer_role=reviewer_role,
                topic=topic,
                max_turns=max_turns,
            )
            initial = runtime.create_grounded_question(
                workspace_id,
                topic,
                reviewer_role,
                retrieval_mode,
            )
            attach_initial_question(
                runtime.db,
                session_id=session["id"],
                workspace_id=workspace_id,
                question_id=initial["id"],
            )
            snapshot = _session_snapshot(runtime.db, workspace_id=workspace_id, session_id=session["id"])
            if snapshot is None:
                raise ValueError("session could not be reloaded")
            return snapshot
        except HTTPException:
            raise
        except ValueError as exc:
            raise HTTPException(status_code=422, detail="Session could not be created safely") from exc
        except Exception as exc:
            raise HTTPException(status_code=502, detail="Session question provider failed") from exc

    @router.get("/api/workspaces/{workspace_id}/sessions/{session_id}")
    def api_get_session(workspace_id: str, session_id: str) -> dict:
        if not runtime.db.workspace_exists(workspace_id):
            raise HTTPException(status_code=404, detail="Workspace not found")
        snapshot = _session_snapshot(runtime.db, workspace_id=workspace_id, session_id=session_id)
        if snapshot is None:
            raise HTTPException(status_code=404, detail="Session not found in workspace")
        return snapshot

    @router.post("/api/workspaces/{workspace_id}/sessions/{session_id}/follow-up")
    def api_follow_up(workspace_id: str, session_id: str) -> dict:
        if not runtime.db.workspace_exists(workspace_id):
            raise HTTPException(status_code=404, detail="Workspace not found")
        if follow_up_generator is None:
            raise HTTPException(status_code=503, detail="Follow-up generation is not configured")
        try:
            return generate_follow_up(
                runtime.db,
                session_id=session_id,
                workspace_id=workspace_id,
                provider=follow_up_generator,
            )
        except ValueError as exc:
            raise HTTPException(status_code=422, detail="Follow-up could not be generated safely") from exc
        except Exception as exc:
            raise HTTPException(status_code=502, detail="Follow-up provider failed") from exc

    @router.post("/ui/workspaces/{workspace_id}/sessions")
    def web_create_session(
        workspace_id: str,
        topic: str = Form(...),
        reviewer_role: str = Form(...),
        retrieval_mode: str = Form("hybrid"),
        max_turns: int = Form(5),
    ):
        try:
            session = api_create_session(workspace_id, topic, reviewer_role, retrieval_mode, max_turns)
        except HTTPException as exc:
            return runtime._redirect(f"/workspaces/{workspace_id}", error=str(exc.detail))
        return runtime._redirect(
            f"/workspaces/{workspace_id}/sessions/{session['id']}",
            message="Defense session started.",
        )

    @router.get("/workspaces/{workspace_id}/sessions/{session_id}")
    def web_session(
        request: Request,
        workspace_id: str,
        session_id: str,
        message: str | None = None,
        error: str | None = None,
    ):
        workspace = runtime.get_workspace(runtime.db, workspace_id)
        if workspace is None:
            return runtime._render_error(request, "Workspace not found.", status_code=404)
        snapshot = _session_snapshot(runtime.db, workspace_id=workspace_id, session_id=session_id)
        if snapshot is None:
            return runtime._render_error(
                request,
                "Session not found in this workspace.",
                status_code=404,
                return_path=f"/workspaces/{workspace_id}",
            )
        return runtime.templates.TemplateResponse(
            request=request,
            name="session.html",
            context={
                "workspace": workspace,
                "session": snapshot,
                "followup_configured": follow_up_generator is not None,
                "message": message,
                "error": error,
            },
        )

    @router.post("/ui/workspaces/{workspace_id}/sessions/{session_id}/follow-up")
    def web_follow_up(workspace_id: str, session_id: str):
        try:
            result = api_follow_up(workspace_id, session_id)
        except HTTPException as exc:
            return runtime._redirect(
                f"/workspaces/{workspace_id}/sessions/{session_id}",
                error=str(exc.detail),
            )
        message = "Session completed." if result.get("status") == "complete" else "Follow-up question generated."
        return runtime._redirect(
            f"/workspaces/{workspace_id}/sessions/{session_id}",
            message=message,
        )

    return router
