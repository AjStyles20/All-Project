"""Append/read persistence for P001 audit events."""
from datetime import datetime

from app.domain.audit import AuditEvent, AuditEventType
from .database import Database


class AuditRepository:
    def __init__(self, database: Database):
        self.database = database

    def append(self, event: AuditEvent) -> None:
        with self.database.connect() as connection:
            connection.execute(
                """INSERT INTO audit_events
                   (event_id, case_id, event_type, recorded_at, actor_type,
                    rationale, claim_id, gap_type, probe_id, evidence_id,
                    from_state, to_state, decision, method_version)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    event.event_id, event.case_id, event.event_type.value,
                    event.recorded_at.isoformat(), event.actor_type,
                    event.rationale, event.claim_id, event.gap_type,
                    event.probe_id, event.evidence_id, event.from_state,
                    event.to_state, event.decision, event.method_version,
                ),
            )

    def list_for_case(self, case_id: str) -> list[AuditEvent]:
        with self.database.connect() as connection:
            rows = connection.execute(
                """SELECT * FROM audit_events
                   WHERE case_id = ?
                   ORDER BY audit_event_seq ASC""",
                (case_id,),
            ).fetchall()
        return [
            AuditEvent(
                event_id=row["event_id"],
                case_id=row["case_id"],
                event_type=AuditEventType(row["event_type"]),
                recorded_at=datetime.fromisoformat(row["recorded_at"]),
                actor_type=row["actor_type"],
                rationale=row["rationale"],
                claim_id=row["claim_id"],
                gap_type=row["gap_type"],
                probe_id=row["probe_id"],
                evidence_id=row["evidence_id"],
                from_state=row["from_state"],
                to_state=row["to_state"],
                decision=row["decision"],
                method_version=row["method_version"],
            )
            for row in rows
        ]
