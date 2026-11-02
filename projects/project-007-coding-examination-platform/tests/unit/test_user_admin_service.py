from datetime import datetime

import pytest
from mysql.connector import errors as mysql_errors

from app.domain.identity import Role, UserConflictError
from app.persistence.mysql_user_repository import MySQLUserRepository
from app.persistence.user_repository import UserRecord
from app.security.passwords import hash_password, verify_password
from app.security.tokens import token_digest
from app.services.user_admin_service import (
    UserAdminService, UserNotFoundError, WrongPasswordError, check_new_password,
)
from tests.unit.test_mysql_examination_repository import FakeDatabase
from tests.user_fakes import InMemoryUserRepository


def service_with_admin():
    repo = InMemoryUserRepository()
    repo.create(UserRecord("admin-1", "root", hash_password("AdminPassword123"), "Root", True), {Role.ADMINISTRATOR})
    return UserAdminService(repo), repo


def test_created_user_has_one_time_password_stored_only_as_a_hash():
    service, repo = service_with_admin()
    user, password = service.create_user("admin-1", "  Student.One ", "Student One", {Role.CANDIDATE})
    assert user.username == "student.one" and user.must_change_password
    stored = repo.get_by_id(user.user_id).password_hash
    assert password not in stored and verify_password(password, stored)
    with pytest.raises(UserConflictError):
        service.create_user("admin-1", "student.one", "Again", {Role.CANDIDATE})
    with pytest.raises(ValueError):
        service.create_user("admin-1", "nobody", "No Roles", set())


def test_password_rules():
    check_new_password("a-long-enough-one", "student")
    with pytest.raises(ValueError):
        check_new_password("short", "student")
    with pytest.raises(ValueError):
        check_new_password("x" * 129, "student")
    with pytest.raises(ValueError, match="username"):
        check_new_password("my-STUDENT-password", "student")


def test_change_own_password_clears_flag_and_signs_out_other_devices():
    service, repo = service_with_admin()
    user, temp = service.create_user("admin-1", "student", "Student", {Role.CANDIDATE})
    repo.sessions = {token_digest("this-device"): user.user_id, token_digest("other-device"): user.user_id,
                     token_digest("someone-else"): "admin-1"}
    with pytest.raises(WrongPasswordError):
        service.change_own_password(user.user_id, "wrong", "a-long-enough-one", "this-device")
    with pytest.raises(ValueError):
        service.change_own_password(user.user_id, temp, temp, "this-device")
    service.change_own_password(user.user_id, temp, "a-long-enough-one", "this-device")
    assert verify_password("a-long-enough-one", repo.get_by_id(user.user_id).password_hash)
    assert not repo.principal_for_user(user.user_id).must_change_password
    assert set(repo.sessions) == {token_digest("this-device"), token_digest("someone-else")}


def test_reset_issues_new_one_time_password_and_revokes_all_sessions():
    service, repo = service_with_admin()
    user, old = service.create_user("admin-1", "student", "Student", {Role.CANDIDATE})
    service.change_own_password(user.user_id, old, "a-long-enough-one", "t")
    repo.sessions = {token_digest("t"): user.user_id}
    new = service.reset_password("admin-1", user.user_id)
    assert repo.sessions == {}
    assert repo.principal_for_user(user.user_id).must_change_password
    assert verify_password(new, repo.get_by_id(user.user_id).password_hash)
    with pytest.raises(UserNotFoundError):
        service.reset_password("admin-1", "missing")


def test_deactivation_blocks_access_and_revokes_sessions():
    service, repo = service_with_admin()
    user, _ = service.create_user("admin-1", "student", "Student", {Role.CANDIDATE})
    repo.sessions = {token_digest("t"): user.user_id}
    service.set_active("admin-1", user.user_id, False)
    assert repo.principal_for_user(user.user_id) is None and repo.sessions == {}
    assert service.list_candidates() == []
    service.set_active("admin-1", user.user_id, True)
    assert repo.principal_for_user(user.user_id) is not None
    assert repo.sessions == {}  # reactivation does not revive old sessions


def test_administrators_cannot_be_locked_out():
    service, _ = service_with_admin()
    with pytest.raises(UserConflictError, match="own account"):
        service.set_active("admin-1", "admin-1", False)
    with pytest.raises(UserConflictError, match="own administrator"):
        service.set_roles("admin-1", "admin-1", {Role.EXAMINER})
    # Another administrator acting on the last one: the repository guard refuses.
    second, _ = service.create_user("admin-1", "second", "Second", {Role.ADMINISTRATOR})
    service.set_active("admin-1", second.user_id, False)
    with pytest.raises(UserConflictError, match="last active"):
        service.set_active(second.user_id, "admin-1", False)
    with pytest.raises(UserConflictError, match="last active"):
        service.set_roles(second.user_id, "admin-1", {Role.EXAMINER})


# ---- SQL contract ----

def test_last_admin_check_locks_rows_inside_the_transaction():
    database = FakeDatabase(fetch_results=[(1,)])  # the target is an active administrator
    database.fetch_all = [("other-admin",)]
    MySQLUserRepository(database).set_active("u1", False)
    sqls = [sql for sql, _ in database.statements]
    assert sqls[0].endswith("FOR UPDATE")
    assert sqls[-1].startswith("UPDATE users SET is_active")


def test_last_admin_is_refused_by_the_repository():
    database = FakeDatabase(fetch_results=[(1,)])
    database.fetch_all = [("u1",)]  # the only active administrator is the target itself
    with pytest.raises(UserConflictError, match="last active"):
        MySQLUserRepository(database).set_active("u1", False)
    assert not any(sql.startswith("UPDATE") for sql, _ in database.statements)


def test_duplicate_username_becomes_conflict():
    duplicate = mysql_errors.IntegrityError(msg="Duplicate entry", errno=1062)
    repo = MySQLUserRepository(FakeDatabase(raise_on_execute=duplicate))
    with pytest.raises(UserConflictError):
        repo.create(UserRecord("u", "name", "hash", "Name", True), {Role.CANDIDATE})


def test_session_revocation_can_keep_the_current_device():
    database = FakeDatabase()
    MySQLUserRepository(database).revoke_user_sessions("u1", datetime(2026, 11, 2), keep_token_hash="keep")
    sql, params = database.statements[0]
    assert sql.endswith("AND token_hash <> %s") and params[-1] == "keep"
