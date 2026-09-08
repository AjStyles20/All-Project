from __future__ import annotations

from fastapi import APIRouter, Form, HTTPException, Request

from .sessions import (
    FollowUpGenerator,
    attach_initial_question,
    create_session,
    ensure_session_schema,
    generate_follow_up,
    question_session_context,
    reconcile_session_completion,
)


def _session_snapshot(database, *, workspace_id: str, session_id: str) -> dict | None:
    ensure_session_schema(database)
    try:
        reconcile_session_completion(database, workspace_id=workspace_id, session_id=session_id)
    except ValueError:
        return None
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
    turns = [dict(row) for row in rows]
    turn_count = len(turns)
    answered_count = sum(1 for turn in turns if turn["answered"])
    current_turn = turns[-1] if turns else None
    for turn in turns:
        turn["is_current"] = bool(current_turn and turn["turn_index"] == current_turn["turn_index"])
    return {
        "id": session["id"],
        "workspace_id": session["workspace_id"],
        "reviewer_role": session["reviewer_role"],
        "topic": session["topic"],
        "status": session["status"],
        "max_turns": session["max_turns"],
        "created_at": session["created_at"],
        "completed_at": session["completed_at"],
        "turn_count": turn_count,
        "answered_count": answered_count,
        "current_turn_index": current_turn["turn_index"] if current_turn else None,
        "current_question_id": current_turn["question_id"] if current_turn else None,
        "turns": turns,
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
        snapshot = _session_snapshot(runtime.db, workspace_id=workspace_id, session_id=session_id)
        if snapshot is None:
            raise HTTPException(status_code=404, detail="Session not found in workspace")
        if snapshot["status"] == "complete":
            raise HTTPException(status_code=422, detail="Session is complete")
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
        question_id = session.get("current_question_id")
        if not question_id:
            return runtime._redirect(
                f"/workspaces/{workspace_id}/sessions/{session['id']}",
                error="Session has no active question.",
            )
        return runtime._redirect(
            f"/workspaces/{workspace_id}/sessions/{session['id']}/questions/{question_id}",
            message="Defense session started. Answer turn 1 when ready.",
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

    @router.get("/workspaces/{workspace_id}/sessions/{session_id}/questions/{question_id}")
    def web_session_question(
        request: Request,
        workspace_id: str,
        session_id: str,
        question_id: str,
        message: str | None = None,
        error: str | None = None,
    ):
        workspace = runtime.get_workspace(runtime.db, workspace_id)
        if workspace is None:
            return runtime._render_error(request, "Workspace not found.", status_code=404)
        try:
            session_context = question_session_context(
                runtime.db,
                workspace_id=workspace_id,
                session_id=session_id,
                question_id=question_id,
            )
            snapshot = _session_snapshot(runtime.db, workspace_id=workspace_id, session_id=session_id)
            question = runtime.get_question(runtime.db, workspace_id=workspace_id, question_id=question_id)
            if snapshot is None or question is None:
                raise ValueError("session question could not be loaded")
            evaluations = runtime.list_evaluations(runtime.db, workspace_id=workspace_id, question_id=question_id)
        except ValueError:
            return runtime._render_error(
                request,
                "Question does not belong to this rehearsal session in this workspace.",
                status_code=404,
                return_path=f"/workspaces/{workspace_id}/sessions/{session_id}",
            )
        session_context["status"] = snapshot["status"]
        session_context["answered"] = bool(evaluations)
        session_context["is_current"] = question_id == snapshot.get("current_question_id")
        return runtime.templates.TemplateResponse(
            request=request,
            name="question.html",
            context={
                "workspace": workspace,
                "question": question,
                "evaluations": evaluations,
                "evaluation_configured": runtime.answer_evaluator is not None,
                "session": session_context,
                "message": message,
                "error": error,
            },
        )

    @router.post("/ui/workspaces/{workspace_id}/sessions/{session_id}/questions/{question_id}/answers")
    def web_session_answer(
        workspace_id: str,
        session_id: str,
        question_id: str,
        answer: str = Form(...),
    ):
        try:
            question_session_context(
                runtime.db,
                workspace_id=workspace_id,
                session_id=session_id,
                question_id=question_id,
            )
            runtime.evaluate_answer(workspace_id, question_id, answer)
            completion = reconcile_session_completion(
                runtime.db,
                workspace_id=workspace_id,
                session_id=session_id,
            )
        except HTTPException as exc:
            return runtime._redirect(
                f"/workspaces/{workspace_id}/sessions/{session_id}/questions/{question_id}",
                error=str(exc.detail),
            )
        except ValueError:
            return runtime._redirect(
                f"/workspaces/{workspace_id}/sessions/{session_id}",
                error="Session/question association could not be verified safely.",
            )
        message = "Answer evaluated. This session has reached its turn limit." if completion["status"] == "complete" else "Answer evaluated and feedback recorded."
        return runtime._redirect(
            f"/workspaces/{workspace_id}/sessions/{session_id}/questions/{question_id}",
            message=message,
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
        if result.get("status") == "complete":
            return runtime._redirect(
                f"/workspaces/{workspace_id}/sessions/{session_id}",
                message="Session completed.",
            )
        question_id = result.get("question_id")
        if not question_id:
            return runtime._redirect(
                f"/workspaces/{workspace_id}/sessions/{session_id}",
                error="Follow-up was created without an actionable question.",
            )
        return runtime._redirect(
            f"/workspaces/{workspace_id}/sessions/{session_id}/questions/{question_id}",
            message=f"Follow-up turn {result.get('turn_index')} generated.",
        )

    return router
