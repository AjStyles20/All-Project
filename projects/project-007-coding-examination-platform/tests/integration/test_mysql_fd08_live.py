"""Opt-in FD-08 live MySQL integration test."""
import os
import threading
from datetime import datetime, timedelta, timezone
from uuid import uuid4
import pytest

from app.domain.identity import AuditAction, Role, UserConflictError
from app.persistence.mysql_database import MySQLDatabase
from app.persistence.mysql_login_throttle_repository import MySQLLoginThrottleRepository
from app.persistence.mysql_user_repository import MySQLUserRepository
from app.services.login_guard import USER_FAILURE_LIMIT, LoginGuard, LoginThrottled
from app.services.user_admin_service import UserAdminService

pytestmark = pytest.mark.skipif(
    os.getenv("P001_RUN_MYSQL_TESTS") != "1",
    reason="Set P001_RUN_MYSQL_TESTS=1 to run live MySQL integration tests.",
)


def test_mysql_fd08_throttle_counts_atomically_and_expires():
    database = MySQLDatabase()
    name = "fd08-" + uuid4().hex[:10]
    ip = "192.0.2." + str(uuid4().int % 250)
    moment = {"now": datetime.now(timezone.utc).replace(tzinfo=None)}
    guard = LoginGuard(MySQLLoginThrottleRepository(database), lambda: moment["now"])

    # Of many simultaneous attempts, exactly the limit get through on a real server.
    results = []

    def attempt():
        try:
            results.append(guard.begin(name, ip))
        except LoginThrottled:
            results.append("throttled")

    threads = [threading.Thread(target=attempt) for _ in range(USER_FAILURE_LIMIT + 7)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sorted(r for r in results if r != "throttled") == list(range(1, USER_FAILURE_LIMIT + 1))
    assert results.count("throttled") == 7
    assert [guard.attempt_failed(r) for r in results if r != "throttled"].count(True) == 1
    with pytest.raises(LoginThrottled):
        guard.begin(name, ip)
    guard.begin(name, "192.0.2.251")  # same name elsewhere: not locked
    guard.attempt_succeeded(name, "192.0.2.251")

    moment["now"] += timedelta(minutes=16)
    assert guard.attempt_failed(guard.begin(name, ip)) is False  # lock expired, fresh window

    assert guard.clear_user(name) == 1
    moment["now"] += timedelta(hours=1)
    guard.attempt_succeeded("fd08-other-" + uuid4().hex[:6], ip)  # triggers the purge
    with database.connect() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM login_throttle WHERE window_started_at < %s",
                       (moment["now"] - timedelta(minutes=40),))
        assert cursor.fetchone()[0] == 0
        cursor.close()


def test_mysql_fd08_audit_commits_and_rolls_back_with_the_change():
    database = MySQLDatabase()
    repo = MySQLUserRepository(database)
    guard = LoginGuard(MySQLLoginThrottleRepository(database))
    accounts = UserAdminService(repo, guard)
    suffix = uuid4().hex[:10]

    admin, _ = accounts.create_user(None, "fd08_admin_" + suffix, "FD08 Admin", {Role.ADMINISTRATOR})
    user, temp = accounts.create_user(admin.user_id, "fd08_user_" + suffix, "FD08 User", {Role.CANDIDATE})
    accounts.set_roles(admin.user_id, user.user_id, {Role.CANDIDATE, Role.EXAMINER})
    newest = accounts.list_audit(5)
    assert newest[0].action is AuditAction.ROLES_CHANGED and newest[0].target_user_id == user.user_id
    assert newest[0].detail == {"roles_after": ["CANDIDATE", "EXAMINER"], "roles_before": ["CANDIDATE"]}
    assert newest[1].action is AuditAction.USER_CREATED and newest[1].actor_user_id == admin.user_id
    assert newest[1].actor_username == admin.username

    # A refused change leaves no record: the guard raises inside the same transaction.
    for other in accounts.list_users():
        if Role.ADMINISTRATOR in other.roles and other.is_active and other.user_id != admin.user_id:
            repo.set_active(other.user_id, False)
    before = len(accounts.list_audit(500))
    with pytest.raises(UserConflictError):
        repo.set_active(admin.user_id, False, audit=accounts._event(AuditAction.DEACTIVATED, user.user_id, admin.user_id, "x"))
    assert len(accounts.list_audit(500)) == before

    with database.connect() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT detail FROM account_audit_events")
        text = " ".join(str(row[0]) for row in cursor.fetchall())
        cursor.close()
    assert temp not in text and "pbkdf2" not in text
