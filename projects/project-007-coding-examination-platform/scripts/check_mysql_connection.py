"""Non-destructive MySQL connectivity/schema check for local development."""
from app.persistence.mysql_database import MySQLDatabase


REQUIRED_TABLES = {"users", "user_roles", "auth_sessions"}


def main() -> int:
    database = MySQLDatabase()
    with database.connect() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE(), VERSION()")
        database_name, version = cursor.fetchone()
        cursor.execute("SHOW TABLES")
        tables = {row[0] for row in cursor.fetchall()}
        cursor.close()

    missing = sorted(REQUIRED_TABLES - tables)
    print(f"Connected database: {database_name}")
    print(f"MySQL version: {version}")
    print(f"Required tables present: {sorted(REQUIRED_TABLES - set(missing))}")
    if missing:
        print(f"Missing required tables: {missing}")
        return 1
    print("P001 MySQL FD-01 schema check: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
