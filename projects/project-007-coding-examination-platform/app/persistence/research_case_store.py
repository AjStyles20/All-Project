"""SQLite research-store adapter for the FD-06 evidence bridge.

The bridge spans two databases (MySQL operational, SQLite research) that cannot
share a transaction. Each bridged case is therefore written here in ONE SQLite
transaction with INSERT OR IGNORE and deterministic ids, so a re-run after a
partial failure converges instead of duplicating or erroring.
"""
from app.domain.enums import ClaimApplicability
from app.domain.models import CaseClaim, ClaimEvidenceLink, EvidenceItem, ProgrammingCase
from app.persistence.database import Database


class ResearchCaseStore:
    def __init__(self, database: Database):
        self.database = database

    def get_case(self, case_id: str) -> ProgrammingCase | None:
        with self.database.connect() as connection:
            row = connection.execute("SELECT * FROM programming_cases WHERE case_id = ?", (case_id,)).fetchone()
        return None if row is None else ProgrammingCase(row["case_id"], row["title"], row["task_description"],
                                                        row["language"], row["version"])

    def get_case_claims(self, case_id: str) -> list[CaseClaim]:
        with self.database.connect() as connection:
            rows = connection.execute("SELECT * FROM case_claims WHERE case_id = ? ORDER BY claim_id",
                                      (case_id,)).fetchall()
        return [CaseClaim(r["case_id"], r["claim_id"], ClaimApplicability(r["applicability"])) for r in rows]

    def materialise(self, case: ProgrammingCase, case_claims: list[CaseClaim],
                    evidence: list[EvidenceItem], links: list[ClaimEvidenceLink]) -> None:
        with self.database.connect() as connection:
            connection.execute(
                "INSERT OR IGNORE INTO programming_cases (case_id, title, task_description, language, version) "
                "VALUES (?, ?, ?, ?, ?)",
                (case.case_id, case.title, case.task_description, case.language, case.version))
            connection.executemany(
                "INSERT OR IGNORE INTO case_claims (case_id, claim_id, applicability) VALUES (?, ?, ?)",
                [(c.case_id, c.claim_id, c.applicability.value) for c in case_claims])
            connection.executemany(
                "INSERT OR IGNORE INTO evidence_items (evidence_id, case_id, evidence_type, content, source_type, "
                "created_at, policy_version, assistance_context) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                [(e.evidence_id, e.case_id, e.evidence_type.value, e.content, e.source_type,
                  e.created_at.isoformat(), e.policy_version, e.assistance_context) for e in evidence])
            connection.executemany(
                "INSERT OR IGNORE INTO claim_evidence_links (case_id, claim_id, evidence_id, rationale) "
                "VALUES (?, ?, ?, ?)",
                [(l.case_id, l.claim_id, l.evidence_id, l.rationale) for l in links])
