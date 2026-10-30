"""MySQL repository for FD-05 Examination Capability Contracts and exceptions."""
import json

from mysql.connector import errors as mysql_errors

from app.domain.capability_contract import (
    AssistanceConstruct, CapabilityContract, ContractException, ContractStatus,
    ExceptionReason, IntegrityMode,
)
from app.domain.examination import ExaminationConflictError
from app.persistence.mysql_database import MySQLDatabase


def contract_from_row(row) -> CapabilityContract:
    doc = row["document"]
    doc = json.loads(doc) if isinstance(doc, (str, bytes, bytearray)) else doc
    return CapabilityContract(
        doc["examination_id"], doc["version"], ContractStatus(row["status"]),
        IntegrityMode(doc["integrity_mode"]), doc["capabilities"],
        AssistanceConstruct(doc["assistance_construct"]["default"]),
        doc["assistance_construct"]["per_claim"], doc["remote_proctoring_justification"],
        doc["bound_by_user_id"], doc["supersedes_version"], doc["amendment_reason"],
        row["bound_at"], row["content_hash"],
    )


def _exception(row) -> ContractException:
    overrides = row["capability_overrides"]
    overrides = json.loads(overrides) if isinstance(overrides, (str, bytes, bytearray)) else overrides
    return ContractException(row["exception_id"], row["examination_id"], row["contract_version"],
                             row["candidate_user_id"], ExceptionReason(row["reason_category"]),
                             row["approved_by_user_id"], row["approved_at"], overrides,
                             row["extra_time_minutes"])


def _document(contract: CapabilityContract) -> str:
    return json.dumps(contract.hashed_document(), sort_keys=True, separators=(",", ":"))


class MySQLContractRepository:
    def __init__(self, database: MySQLDatabase):
        self.database = database

    def _fetch(self, sql: str, params: tuple, many: bool = False):
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, params)
            result = cursor.fetchall() if many else cursor.fetchone()
            cursor.close()
        return result

    def list_versions(self, examination_id: str) -> list[CapabilityContract]:
        rows = self._fetch("SELECT * FROM capability_contracts WHERE examination_id=%s ORDER BY version",
                           (examination_id,), many=True)
        return [contract_from_row(row) for row in rows]

    def get_latest(self, examination_id: str) -> CapabilityContract | None:
        row = self._fetch("SELECT * FROM capability_contracts WHERE examination_id=%s "
                          "ORDER BY version DESC LIMIT 1", (examination_id,))
        return None if row is None else contract_from_row(row)

    def get_bound(self, examination_id: str) -> CapabilityContract | None:
        row = self._fetch("SELECT * FROM capability_contracts WHERE examination_id=%s AND status='BOUND'",
                          (examination_id,))
        return None if row is None else contract_from_row(row)

    def in_force_at(self, examination_id: str, at) -> CapabilityContract | None:
        """Spec §5.3: the version bound most recently at or before `at`."""
        row = self._fetch("SELECT * FROM capability_contracts WHERE examination_id=%s "
                          "AND bound_at IS NOT NULL AND bound_at <= %s "
                          "ORDER BY bound_at DESC, version DESC LIMIT 1", (examination_id, at))
        return None if row is None else contract_from_row(row)

    def save_draft(self, contract: CapabilityContract) -> bool:
        """Insert or replace the DRAFT version, only while the examination is DRAFT."""
        contract.validate()
        with self.database.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE capability_contracts c JOIN examinations e ON e.examination_id = c.examination_id "
                "SET c.document=%s, c.content_hash=%s "
                "WHERE c.examination_id=%s AND c.version=%s AND c.status='DRAFT' AND e.status='DRAFT'",
                (_document(contract), contract.compute_hash(), contract.examination_id, contract.version),
            )
            changed = cursor.rowcount
            if changed == 0:
                try:
                    cursor.execute(
                        "INSERT INTO capability_contracts (examination_id,version,status,document,content_hash) "
                        "SELECT examination_id,%s,'DRAFT',%s,%s FROM examinations "
                        "WHERE examination_id=%s AND status='DRAFT'",
                        (contract.version, _document(contract), contract.compute_hash(),
                         contract.examination_id),
                    )
                except mysql_errors.IntegrityError as exc:
                    # The version exists but is no longer DRAFT: never rewrite a bound contract.
                    raise ExaminationConflictError("That contract version is already bound.") from exc
                changed = cursor.rowcount
            cursor.close()
        return changed == 1

    def amend_bound(self, contract: CapabilityContract, bound_at) -> bool:
        """Bind a new version immediately and supersede the current one, in one transaction."""
        contract.validate()
        with self.database.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE capability_contracts c JOIN examinations e ON e.examination_id = c.examination_id "
                "SET c.status='SUPERSEDED' WHERE c.examination_id=%s AND c.version=%s "
                "AND c.status='BOUND' AND e.status IN ('SCHEDULED','ACTIVE')",
                (contract.examination_id, contract.supersedes_version),
            )
            if cursor.rowcount != 1:
                cursor.close()
                return False
            try:
                cursor.execute(
                    "INSERT INTO capability_contracts "
                    "(examination_id,version,status,document,content_hash,bound_at) "
                    "VALUES (%s,%s,'BOUND',%s,%s,%s)",
                    (contract.examination_id, contract.version, _document(contract),
                     contract.compute_hash(), bound_at),
                )
            except mysql_errors.IntegrityError as exc:
                raise ExaminationConflictError("A newer contract version already exists.") from exc
            cursor.close()
        return True

    def create_exception(self, exception: ContractException) -> None:
        exception.validate()
        with self.database.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO contract_exceptions "
                "(exception_id,examination_id,contract_version,candidate_user_id,capability_overrides,"
                "extra_time_minutes,reason_category,approved_by_user_id,approved_at) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (exception.exception_id, exception.examination_id, exception.contract_version,
                 exception.candidate_user_id, json.dumps(exception.capability_overrides, sort_keys=True),
                 exception.extra_time_minutes, exception.reason_category.value,
                 exception.approved_by_user_id, exception.approved_at),
            )
            cursor.close()

    def list_exceptions(self, examination_id: str, candidate_user_id: str | None = None) -> list[ContractException]:
        if candidate_user_id is None:
            rows = self._fetch("SELECT * FROM contract_exceptions WHERE examination_id=%s "
                               "ORDER BY approved_at, exception_id", (examination_id,), many=True)
        else:
            rows = self._fetch("SELECT * FROM contract_exceptions WHERE examination_id=%s "
                               "AND candidate_user_id=%s ORDER BY approved_at, exception_id",
                               (examination_id, candidate_user_id), many=True)
        return [_exception(row) for row in rows]
