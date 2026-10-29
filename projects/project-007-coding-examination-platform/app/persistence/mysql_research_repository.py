"""MySQL repository for FD-06 research links, consent, identities and bridge records."""
import json

from mysql.connector import errors as mysql_errors

from app.domain.examination import ExaminationConflictError
from app.domain.research_bridge import BridgeOutcome, BridgeRecord, ConsentStatus, ResearchLink
from app.persistence.mysql_database import MySQLDatabase


def _link(row) -> ResearchLink:
    claims = row["claim_ids"]
    claims = json.loads(claims) if isinstance(claims, (str, bytes, bytearray)) else claims
    return ResearchLink(row["link_id"], row["examination_id"], row["question_id"], row["template_case_id"],
                        tuple(claims), row["ethics_reference"], row["created_by_user_id"], row["created_at"])


def _record(row) -> BridgeRecord:
    return BridgeRecord(row["session_id"], row["question_id"], row["link_id"], BridgeOutcome(row["outcome"]),
                        row["research_case_id"], row["response_revision"], row["policy_version"],
                        row["bridged_at"])


class MySQLResearchRepository:
    def __init__(self, database: MySQLDatabase):
        self.database = database

    def _fetch(self, sql: str, params: tuple, many: bool = False):
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, params)
            result = cursor.fetchall() if many else cursor.fetchone()
            cursor.close()
        return result

    def _execute(self, sql: str, params: tuple, conflict: str) -> None:
        try:
            with self.database.connect() as connection:
                cursor = connection.cursor()
                cursor.execute(sql, params)
                cursor.close()
        except mysql_errors.IntegrityError as exc:
            raise ExaminationConflictError(conflict) from exc

    # Links

    def create_link(self, link: ResearchLink) -> None:
        link.validate()
        self._execute(
            "INSERT INTO research_links (link_id,examination_id,question_id,template_case_id,claim_ids,"
            "ethics_reference,created_by_user_id,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (link.link_id, link.examination_id, link.question_id, link.template_case_id,
             json.dumps(list(link.claim_ids)), link.ethics_reference, link.created_by_user_id, link.created_at),
            "That examination question already has a research link.")

    def list_links(self, examination_id: str) -> list[ResearchLink]:
        rows = self._fetch("SELECT * FROM research_links WHERE examination_id=%s ORDER BY created_at, link_id",
                           (examination_id,), many=True)
        return [_link(row) for row in rows]

    # Consent (append-only; latest event wins)

    def record_consent(self, examination_id: str, candidate_user_id: str, status: ConsentStatus, at) -> None:
        self._execute(
            "INSERT INTO research_consent_events (examination_id,candidate_user_id,status,recorded_at) "
            "VALUES (%s,%s,%s,%s)", (examination_id, candidate_user_id, status.value, at),
            "Consent could not be recorded.")

    def current_consent(self, examination_id: str, candidate_user_id: str) -> ConsentStatus | None:
        row = self._fetch("SELECT status FROM research_consent_events WHERE examination_id=%s "
                          "AND candidate_user_id=%s ORDER BY event_id DESC LIMIT 1",
                          (examination_id, candidate_user_id))
        return None if row is None else ConsentStatus(row["status"])

    # Identities (locked link)

    def get_research_code(self, examination_id: str, candidate_user_id: str) -> str | None:
        row = self._fetch("SELECT research_code FROM research_identities WHERE examination_id=%s "
                          "AND candidate_user_id=%s", (examination_id, candidate_user_id))
        return None if row is None else row["research_code"]

    def create_research_code(self, examination_id: str, candidate_user_id: str, code: str, at) -> bool:
        """False if this candidate already has a code (a concurrent run won)."""
        try:
            self._execute("INSERT INTO research_identities (examination_id,candidate_user_id,research_code,"
                          "created_at) VALUES (%s,%s,%s,%s)", (examination_id, candidate_user_id, code, at),
                          "duplicate")
        except ExaminationConflictError:
            return False
        return True

    def list_identities(self, examination_id: str) -> list[tuple[str, str]]:
        rows = self._fetch("SELECT candidate_user_id, research_code FROM research_identities "
                           "WHERE examination_id=%s ORDER BY research_code", (examination_id,), many=True)
        return [(row["candidate_user_id"], row["research_code"]) for row in rows]

    # Bridge records

    def get_bridge_record(self, session_id: str, question_id: str) -> BridgeRecord | None:
        row = self._fetch("SELECT * FROM research_bridge_records WHERE session_id=%s AND question_id=%s",
                          (session_id, question_id))
        return None if row is None else _record(row)

    def save_bridge_record(self, record: BridgeRecord) -> bool:
        """False if another run already recorded this (session, question)."""
        try:
            self._execute(
                "INSERT INTO research_bridge_records (session_id,question_id,link_id,outcome,research_case_id,"
                "response_revision,policy_version,bridged_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (record.session_id, record.question_id, record.link_id, record.outcome.value,
                 record.research_case_id, record.response_revision, record.policy_version, record.bridged_at),
                "duplicate")
        except ExaminationConflictError:
            return False
        return True

    def list_bridge_records(self, examination_id: str) -> list[BridgeRecord]:
        rows = self._fetch("SELECT b.* FROM research_bridge_records b JOIN research_links l "
                           "ON l.link_id = b.link_id WHERE l.examination_id=%s "
                           "ORDER BY b.bridged_at, b.session_id, b.question_id", (examination_id,), many=True)
        return [_record(row) for row in rows]
