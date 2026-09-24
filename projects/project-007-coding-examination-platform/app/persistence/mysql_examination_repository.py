"""MySQL repository for FD-02 examinations and programming questions."""
from app.domain.examination import Examination, ExaminationStatus, ProgrammingQuestion
from app.persistence.mysql_database import MySQLDatabase


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
        if row is None:
            return None
        return Examination(row["examination_id"], row["title"], row["description"],
                           row["owner_user_id"], ExaminationStatus(row["status"]),
                           row["starts_at"], row["ends_at"])

    def update_status(self, examination_id: str, status: ExaminationStatus) -> bool:
        with self.database.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE examinations SET status=%s WHERE examination_id=%s",
                           (status.value, examination_id))
            changed = cursor.rowcount
            cursor.close()
        return changed == 1

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
        if row is None:
            return None
        return ProgrammingQuestion(row["question_id"], row["title"], row["prompt"],
                                   row["language"], row["max_score"], row["version"])

    def attach_question(self, examination_id: str, question_id: str,
                        display_order: int, score_weight: int) -> None:
        if display_order <= 0 or score_weight <= 0:
            raise ValueError("Display order and score weight must be positive.")
        with self.database.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO examination_questions "
                "(examination_id,question_id,display_order,score_weight) VALUES (%s,%s,%s,%s)",
                (examination_id, question_id, display_order, score_weight),
            )
            cursor.close()
