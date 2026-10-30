"""Repositories for M1 P001 domain objects."""
from datetime import datetime

from app.domain.enums import ClaimApplicability, EvidenceState, EvidenceType
from app.domain.models import (
    CaseClaim,
    ClaimEvidenceLink,
    CompetenceClaim,
    EvidenceItem,
    EvidenceStateRecord,
    ProgrammingCase,
)
from .database import Database


class P001Repository:
    def __init__(self, database: Database):
        self.database = database

    def add_case(self, case: ProgrammingCase) -> None:
        with self.database.connect() as connection:
            connection.execute(
                """INSERT INTO programming_cases
                   (case_id, title, task_description, language, version)
                   VALUES (?, ?, ?, ?, ?)""",
                (case.case_id, case.title, case.task_description, case.language, case.version),
            )

    def add_claim(self, claim: CompetenceClaim) -> None:
        with self.database.connect() as connection:
            connection.execute(
                """INSERT INTO competence_claim_definitions
                   (claim_id, name, definition, version)
                   VALUES (?, ?, ?, ?)""",
                (claim.claim_id, claim.name, claim.definition, claim.version),
            )

    def add_case_claim(self, case_claim: CaseClaim) -> None:
        with self.database.connect() as connection:
            connection.execute(
                """INSERT INTO case_claims (case_id, claim_id, applicability)
                   VALUES (?, ?, ?)""",
                (case_claim.case_id, case_claim.claim_id, case_claim.applicability.value),
            )

    def add_evidence(self, evidence: EvidenceItem) -> None:
        with self.database.connect() as connection:
            connection.execute(
                """INSERT INTO evidence_items
                   (evidence_id, case_id, evidence_type, content, source_type,
                    created_at, policy_version, assistance_context)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    evidence.evidence_id,
                    evidence.case_id,
                    evidence.evidence_type.value,
                    evidence.content,
                    evidence.source_type,
                    evidence.created_at.isoformat(),
                    evidence.policy_version,
                    evidence.assistance_context,
                ),
            )

    def link_evidence(self, link: ClaimEvidenceLink) -> None:
        with self.database.connect() as connection:
            connection.execute(
                """INSERT INTO claim_evidence_links
                   (case_id, claim_id, evidence_id, rationale)
                   VALUES (?, ?, ?, ?)""",
                (link.case_id, link.claim_id, link.evidence_id, link.rationale),
            )

    def append_evidence_state(self, record: EvidenceStateRecord) -> int:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """INSERT INTO evidence_state_history
                   (case_id, claim_id, state, rationale, recorded_at, source)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    record.case_id,
                    record.claim_id,
                    record.state.value,
                    record.rationale,
                    record.recorded_at.isoformat(),
                    record.source,
                ),
            )
            return int(cursor.lastrowid)

    def list_evidence_states(self, case_id: str, claim_id: str) -> list[EvidenceStateRecord]:
        with self.database.connect() as connection:
            rows = connection.execute(
                """SELECT case_id, claim_id, state, rationale, recorded_at, source
                   FROM evidence_state_history
                   WHERE case_id = ? AND claim_id = ?
                   ORDER BY state_record_id ASC""",
                (case_id, claim_id),
            ).fetchall()

        return [
            EvidenceStateRecord(
                case_id=row["case_id"],
                claim_id=row["claim_id"],
                state=EvidenceState(row["state"]),
                rationale=row["rationale"],
                recorded_at=datetime.fromisoformat(row["recorded_at"]),
                source=row["source"],
            )
            for row in rows
        ]

    def get_case_claims(self, case_id: str) -> list[CaseClaim]:
        with self.database.connect() as connection:
            rows = connection.execute(
                """SELECT case_id, claim_id, applicability
                   FROM case_claims
                   WHERE case_id = ?
                   ORDER BY claim_id""",
                (case_id,),
            ).fetchall()

        return [
            CaseClaim(
                case_id=row["case_id"],
                claim_id=row["claim_id"],
                applicability=ClaimApplicability(row["applicability"]),
            )
            for row in rows
        ]

    def get_evidence_for_claim(self, case_id: str, claim_id: str) -> list[EvidenceItem]:
        with self.database.connect() as connection:
            rows = connection.execute(
                """SELECT e.*
                   FROM evidence_items AS e
                   JOIN claim_evidence_links AS l
                     ON l.evidence_id = e.evidence_id
                   WHERE l.case_id = ? AND l.claim_id = ?
                   ORDER BY e.created_at, e.evidence_id""",
                (case_id, claim_id),
            ).fetchall()

        return [
            EvidenceItem(
                evidence_id=row["evidence_id"],
                case_id=row["case_id"],
                evidence_type=EvidenceType(row["evidence_type"]),
                content=row["content"],
                source_type=row["source_type"],
                created_at=datetime.fromisoformat(row["created_at"]),
                policy_version=row["policy_version"],
                assistance_context=row["assistance_context"],
            )
            for row in rows
        ]
