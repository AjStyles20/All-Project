from __future__ import annotations

import json

from .db import Database
from .evaluation import ensure_evaluation_schema
from .questioning import ensure_question_schema


MAX_UI_ROWS = 100


def list_workspaces(database: Database, *, limit: int = 50) -> list[dict]:
    safe_limit = max(1, min(int(limit), MAX_UI_ROWS))
    with database.connect() as connection:
        rows = connection.execute(
            "SELECT id, name, created_at FROM workspaces ORDER BY created_at DESC LIMIT ?",
            (safe_limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def get_workspace(database: Database, workspace_id: str) -> dict | None:
    with database.connect() as connection:
        row = connection.execute(
            "SELECT id, name, created_at FROM workspaces WHERE id = ?",
            (workspace_id,),
        ).fetchone()
    return dict(row) if row is not None else None


def list_documents(database: Database, *, workspace_id: str, limit: int = 50) -> list[dict]:
    safe_limit = max(1, min(int(limit), MAX_UI_ROWS))
    with database.connect() as connection:
        rows = connection.execute(
            """
            SELECT id, original_filename, extension, content_hash, extraction_status, created_at
            FROM source_documents
            WHERE workspace_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (workspace_id, safe_limit),
        ).fetchall()
    return [dict(row) for row in rows]


def list_questions(database: Database, *, workspace_id: str, limit: int = 25) -> list[dict]:
    ensure_question_schema(database)
    safe_limit = max(1, min(int(limit), MAX_UI_ROWS))
    with database.connect() as connection:
        rows = connection.execute(
            """
            SELECT id, reviewer_role, topic, question_text, retrieval_mode,
                   semantic_status, provider, model, model_version, created_at
            FROM generated_questions
            WHERE workspace_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (workspace_id, safe_limit),
        ).fetchall()
    return [dict(row) for row in rows]


def get_question(database: Database, *, workspace_id: str, question_id: str) -> dict | None:
    ensure_question_schema(database)
    with database.connect() as connection:
        row = connection.execute(
            """
            SELECT id, workspace_id, reviewer_role, topic, question_text, evidence_json,
                   retrieval_mode, semantic_status, provider, model, model_version, created_at
            FROM generated_questions
            WHERE id = ? AND workspace_id = ?
            """,
            (question_id, workspace_id),
        ).fetchone()
    if row is None:
        return None

    result = dict(row)
    try:
        snapshot = json.loads(result.pop("evidence_json"))
    except (TypeError, json.JSONDecodeError) as exc:
        raise ValueError("stored question evidence is malformed") from exc
    if not isinstance(snapshot, list) or len(snapshot) > 8:
        raise ValueError("stored question evidence is malformed")

    evidence: list[dict] = []
    with database.connect() as connection:
        for item in snapshot:
            if not isinstance(item, dict):
                raise ValueError("stored question evidence is malformed")
            chunk_id = str(item.get("chunk_id", ""))
            row = connection.execute(
                """
                SELECT dc.id AS chunk_id, dc.document_id, sd.original_filename AS filename,
                       dc.locator, dc.text
                FROM document_chunks AS dc
                JOIN source_documents AS sd ON sd.id = dc.document_id
                WHERE dc.id = ? AND sd.workspace_id = ?
                """,
                (chunk_id, workspace_id),
            ).fetchone()
            if row is None:
                raise ValueError("stored question evidence is outside workspace")
            current = dict(row)
            if str(item.get("document_id", "")) != current["document_id"]:
                raise ValueError("stored question document provenance mismatch")
            if str(item.get("filename", "")) != current["filename"]:
                raise ValueError("stored question filename provenance mismatch")
            if str(item.get("locator", "")) != current["locator"]:
                raise ValueError("stored question locator provenance mismatch")
            evidence.append(current)
    result["evidence"] = evidence
    return result


def list_evaluations(
    database: Database,
    *,
    workspace_id: str,
    question_id: str,
    limit: int = 20,
) -> list[dict]:
    ensure_evaluation_schema(database)
    safe_limit = max(1, min(int(limit), MAX_UI_ROWS))
    with database.connect() as connection:
        rows = connection.execute(
            """
            SELECT id, answer_text, summary, feedback_json, evidence_json,
                   policy_id, provider, model, model_version, created_at
            FROM answer_evaluations
            WHERE workspace_id = ? AND question_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (workspace_id, question_id, safe_limit),
        ).fetchall()

    results: list[dict] = []
    for row in rows:
        item = dict(row)
        try:
            feedback = json.loads(item.pop("feedback_json"))
            evidence = json.loads(item.pop("evidence_json"))
        except (TypeError, json.JSONDecodeError) as exc:
            raise ValueError("stored evaluation data is malformed") from exc
        if not isinstance(feedback, list) or not isinstance(evidence, list):
            raise ValueError("stored evaluation data is malformed")
        item["feedback"] = feedback
        item["evidence"] = evidence
        results.append(item)
    return results
