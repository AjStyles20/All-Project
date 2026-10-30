"""MySQL repository for FD-02 examinations and programming questions."""
from mysql.connector import errors as mysql_errors

from app.domain.examination import (
    Examination, ExaminationConflictError, ExaminationQuestionEntry, ExaminationStatus,
    ProgrammingQuestion,
)
from app.domain.capability_contract import ContractRequiredError
from app.persistence.mysql_database import MySQLDatabase


def _examination(row) -> Examination:
    return Examination(row["examination_id"], row["title"], row["description"],
                       row["owner_user_id"], ExaminationStatus(row["status"]),
                       row["starts_at"], row["ends_at"])


def _question(row) -> ProgrammingQuestion:
    return ProgrammingQuestion(row["question_id"], row["title"], row["prompt"],
                               row["language"], row["max_score"], row["version"])


class MySQLExaminationRepository:
    def __init__(self, database: MySQLDatabase):
        self.database = database

    def create_examination(self, exam: Examination) -> None:
        exam.validate()
        with self.database.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO examinations "
                "(examination_id,title,description,owner_user_id,status,starts_at,ends_at) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (exam.examination_id, exam.title, exam.description, exam.owner_user_id,
                 exam.status.value, exam.starts_at, exam.ends_at),
            )
            cursor.close()

    def get_examination(self, examination_id: str) -> Examination | None:
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM examinations WHERE examination_id=%s", (examination_id,))
            row = cursor.fetchone()
            cursor.close()
        return None if row is None else _examination(row)

    def list_examinations_by_owner(self, owner_user_id: str) -> list[Examination]:
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM examinations WHERE owner_user_id=%s "
                "ORDER BY created_at, examination_id",
                (owner_user_id,),
            )
            rows = cursor.fetchall()
            cursor.close()
        return [_examination(row) for row in rows]

    def update_details(self, exam: Examination) -> bool:
        exam.validate()
        with self.database.connect() as connection:
            cursor = connection.cursor()
            # Guarded by status so details cannot change once the examination leaves DRAFT.
            cursor.execute(
                "UPDATE examinations SET title=%s, description=%s, starts_at=%s, ends_at=%s "
                "WHERE examination_id=%s AND status='DRAFT'",
                (exam.title, exam.description, exam.starts_at, exam.ends_at, exam.examination_id),
            )
            changed = cursor.rowcount
            cursor.close()
        return changed == 1

    def update_status(self, examination_id: str, status: ExaminationStatus, *,
                      expected: ExaminationStatus) -> bool:
        with self.database.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE examinations SET status=%s WHERE examination_id=%s AND status=%s",
                (status.value, examination_id, expected.value),
            )
            changed = cursor.rowcount
            if changed == 1 and status is ExaminationStatus.SCHEDULED:
                self._bind_contract(cursor, examination_id)
            if changed == 1 and status is ExaminationStatus.CLOSED:
                # DR-011 (6): closing finalises every open session in the same transaction,
                # so saved work is never left unsubmitted and the close cannot half-apply.
                cursor.execute(
                    "UPDATE examination_sessions s "
                    "JOIN candidate_assignments a ON a.assignment_id = s.assignment_id "
                    "SET s.status='SUBMITTED', s.submitted_at=UTC_TIMESTAMP(6), "
                    "s.submission_mode='AUTO_ON_CLOSE' "
                    "WHERE a.examination_id=%s AND s.status='IN_PROGRESS'",
                    (examination_id,),
                )
            cursor.close()
        return changed == 1

    def has_bindable_contract(self, examination_id: str) -> bool:
        with self.database.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM capability_contracts "
                           "WHERE examination_id=%s AND status IN ('DRAFT','BOUND')", (examination_id,))
            count = cursor.fetchone()[0]
            cursor.close()
        return count > 0

    @staticmethod
    def _bind_contract(cursor, examination_id: str) -> None:
        # ECC spec §5.2 (DR-013 Q2): scheduling binds the draft contract in the same
        # transaction. Raising here rolls the status change back as well.
        cursor.execute("SELECT version FROM capability_contracts "
                       "WHERE examination_id=%s AND status='DRAFT' FOR UPDATE", (examination_id,))
        draft = cursor.fetchone()
        if draft is not None:
            cursor.execute("UPDATE capability_contracts SET status='SUPERSEDED' "
                           "WHERE examination_id=%s AND status='BOUND'", (examination_id,))
            cursor.execute("UPDATE capability_contracts SET status='BOUND', bound_at=UTC_TIMESTAMP(6) "
                           "WHERE examination_id=%s AND version=%s", (examination_id, draft[0]))
        # A previously bound contract (exam returned to DRAFT unedited) stays in force.
        cursor.execute("SELECT COUNT(*) FROM capability_contracts "
                       "WHERE examination_id=%s AND status='BOUND'", (examination_id,))
        if cursor.fetchone()[0] != 1:
            raise ContractRequiredError("Scheduling requires a capability contract (ECC spec §5.2).")

    def create_question(self, question: ProgrammingQuestion, created_by_user_id: str) -> None:
        question.validate()
        with self.database.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO questions "
                "(question_id,title,prompt,language,max_score,version,created_by_user_id) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (question.question_id, question.title, question.prompt, question.language,
                 question.max_score, question.version, created_by_user_id),
            )
            cursor.close()

    def get_question(self, question_id: str) -> ProgrammingQuestion | None:
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM questions WHERE question_id=%s", (question_id,))
            row = cursor.fetchone()
            cursor.close()
        return None if row is None else _question(row)

    def question_created_by(self, question_id: str) -> str | None:
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT created_by_user_id FROM questions WHERE question_id=%s",
                           (question_id,))
            row = cursor.fetchone()
            cursor.close()
        return None if row is None else row["created_by_user_id"]

    def list_questions_by_creator(self, created_by_user_id: str) -> list[ProgrammingQuestion]:
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM questions WHERE created_by_user_id=%s "
                "ORDER BY created_at, question_id",
                (created_by_user_id,),
            )
            rows = cursor.fetchall()
            cursor.close()
        return [_question(row) for row in rows]

    def list_examination_questions(self, examination_id: str) -> list[ExaminationQuestionEntry]:
        with self.database.connect() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT q.*, eq.display_order, eq.score_weight "
                "FROM examination_questions eq "
                "JOIN questions q ON q.question_id = eq.question_id "
                "WHERE eq.examination_id=%s ORDER BY eq.display_order",
                (examination_id,),
            )
            rows = cursor.fetchall()
            cursor.close()
        return [ExaminationQuestionEntry(_question(row), row["display_order"], row["score_weight"])
                for row in rows]

    def attach_question(self, examination_id: str, question_id: str,
                        display_order: int, score_weight: int) -> None:
        if display_order <= 0 or score_weight <= 0:
            raise ValueError("Display order and score weight must be positive.")
        try:
            with self.database.connect() as connection:
                cursor = connection.cursor()
                # INSERT ... SELECT only matches a DRAFT examination, so membership cannot
                # change after a concurrent schedule even though the service checked first.
                cursor.execute(
                    "INSERT INTO examination_questions "
                    "(examination_id,question_id,display_order,score_weight) "
                    "SELECT examination_id,%s,%s,%s FROM examinations "
                    "WHERE examination_id=%s AND status='DRAFT'",
                    (question_id, display_order, score_weight, examination_id),
                )
                inserted = cursor.rowcount
                cursor.close()
        except mysql_errors.IntegrityError as exc:
            # Backstop for races the service pre-check cannot see: duplicate key or vanished FK.
            raise ExaminationConflictError(
                "Question attachment conflicts with existing examination content."
            ) from exc
        if inserted != 1:
            raise ExaminationConflictError("Examination is no longer DRAFT.")

    def detach_question(self, examination_id: str, question_id: str) -> bool:
        with self.database.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM examination_questions WHERE examination_id=%s AND question_id=%s "
                "AND EXISTS (SELECT 1 FROM examinations "
                "WHERE examination_id=%s AND status='DRAFT')",
                (examination_id, question_id, examination_id),
            )
            changed = cursor.rowcount
            cursor.close()
        return changed == 1
