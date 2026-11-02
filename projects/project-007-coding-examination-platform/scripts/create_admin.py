"""Create the first administrator (FD-07). Run once from the project folder:

    python -m scripts.create_admin --username <name> --display-name "<full name>"

There is deliberately no API for this: an unauthenticated "first admin" endpoint could be
claimed by anyone who reached the server first. Whoever can run this script already has the
database credentials. The password is read without echo and never written anywhere but as a hash.
"""
import argparse
from getpass import getpass
from uuid import uuid4

from app.domain.identity import Role, UserConflictError
from app.persistence.mysql_database import MySQLDatabase
from app.persistence.mysql_user_repository import MySQLUserRepository
from app.persistence.user_repository import UserRecord
from app.security.passwords import hash_password
from app.services.user_admin_service import check_new_password


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a P001 administrator account.")
    parser.add_argument("--username", required=True)
    parser.add_argument("--display-name", required=True)
    args = parser.parse_args()

    username = args.username.strip().lower()
    password = getpass("New administrator password: ")
    if password != getpass("Repeat password: "):
        print("Passwords do not match; nothing was created.")
        return 1
    try:
        check_new_password(password, username)
        record = UserRecord(str(uuid4()), username, hash_password(password), args.display_name.strip(), True)
        MySQLUserRepository(MySQLDatabase()).create(record, {Role.ADMINISTRATOR})
    except (ValueError, UserConflictError) as error:
        print(f"Nothing was created: {error}")
        return 1
    print(f"Administrator '{username}' created.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
