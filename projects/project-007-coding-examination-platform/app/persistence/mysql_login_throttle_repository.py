"""MySQL storage for FD-08 login throttling. Counters survive restarts and work across
processes, unlike an in-memory limiter."""
from app.persistence.mysql_database import MySQLDatabase


class MySQLLoginThrottleRepository:
    def __init__(self, database: MySQLDatabase):
        self.database = database

    def locked_until(self, keys: list[str]):
        placeholders = ",".join(["%s"] * len(keys))
        with self.database.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT MAX(locked_until) FROM login_throttle WHERE scope_key IN ({placeholders})",
                           tuple(keys))
            row = cursor.fetchone()
            cursor.close()
        return row[0] if row else None

    def reserve(self, key: str, subject_key: str | None, limit: int, now, window_cutoff, lock_until) -> int:
        """Count one attempt and return this attempt's position in the window. The upsert
        holds the row lock until commit, so the read-back sees exactly this attempt's count.
        MySQL applies the assignments left to right, so locked_until reads old values first."""
        with self.database.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO login_throttle (scope_key, subject_key, failed_count, window_started_at, locked_until) "
                "VALUES (%s, %s, 1, %s, NULL) ON DUPLICATE KEY UPDATE "
                "locked_until = IF(window_started_at >= %s AND failed_count + 1 >= %s, %s, locked_until), "
                "failed_count = IF(window_started_at >= %s, failed_count + 1, 1), "
                "window_started_at = IF(window_started_at >= %s, window_started_at, %s)",
                (key, subject_key, now, window_cutoff, limit, lock_until, window_cutoff, window_cutoff, now),
            )
            cursor.execute("SELECT failed_count FROM login_throttle WHERE scope_key = %s", (key,))
            row = cursor.fetchone()
            cursor.close()
        return row[0] if row else 1

    def refund(self, key: str) -> None:
        with self.database.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE login_throttle SET failed_count = GREATEST(failed_count - 1, 0) "
                           "WHERE scope_key = %s", (key,))
            cursor.close()

    def clear(self, keys: list[str]) -> None:
        placeholders = ",".join(["%s"] * len(keys))
        with self.database.connect() as connection:
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM login_throttle WHERE scope_key IN ({placeholders})", tuple(keys))
            cursor.close()

    def clear_subject(self, subject_key: str) -> int:
        with self.database.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM login_throttle WHERE subject_key = %s", (subject_key,))
            removed = cursor.rowcount
            cursor.close()
        return removed

    def purge_older_than(self, cutoff) -> None:
        # Keeps the table small, since unknown usernames create rows too.
        with self.database.connect() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM login_throttle WHERE window_started_at < %s "
                           "AND (locked_until IS NULL OR locked_until < %s)", (cutoff, cutoff))
            cursor.close()
