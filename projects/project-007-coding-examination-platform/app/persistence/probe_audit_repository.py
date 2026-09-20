"""Persistence for candidate-by-candidate probe-selection audit evidence."""
from dataclasses import dataclass

from app.persistence.database import Database
from app.services.probe_selector import ProbeCandidateDisposition


@dataclass(frozen=True)
class StoredProbeCandidateDisposition:
    event_id: str
    case_id: str
    claim_id: str
    gap_type: str
    disposition: ProbeCandidateDisposition


class ProbeAuditRepository:
    def __init__(self, database: Database):
        self.database = database

    def append_selection_candidates(
        self, *, event_id: str, case_id: str, claim_id: str, gap_type: str,
        candidates: tuple[ProbeCandidateDisposition, ...],
    ) -> None:
        with self.database.connect() as connection:
            for item in candidates:
                connection.execute(
                    """INSERT INTO probe_candidate_audit
                       (event_id, case_id, claim_id, gap_type, probe_id,
                        admissible, potentially_sufficient, burden_rank,
                        disposition, rationale)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        event_id, case_id, claim_id, gap_type, item.probe_id,
                        int(item.admissible), int(item.potentially_sufficient),
                        item.burden_rank, item.disposition, item.rationale,
                    ),
                )

    def list_for_event(self, event_id: str) -> list[StoredProbeCandidateDisposition]:
        with self.database.connect() as connection:
            rows = connection.execute(
                """SELECT * FROM probe_candidate_audit
                   WHERE event_id = ?
                   ORDER BY candidate_audit_seq""", (event_id,)
            ).fetchall()
        return [
            StoredProbeCandidateDisposition(
                event_id=row["event_id"], case_id=row["case_id"],
                claim_id=row["claim_id"], gap_type=row["gap_type"],
                disposition=ProbeCandidateDisposition(
                    probe_id=row["probe_id"], admissible=bool(row["admissible"]),
                    potentially_sufficient=bool(row["potentially_sufficient"]),
                    burden_rank=row["burden_rank"], disposition=row["disposition"],
                    rationale=row["rationale"],
                ),
            )
            for row in rows
        ]
