"""Opt-in FD-07 live MySQL integration test."""
import os
from uuid import uuid4
import pytest

from app.domain.identity import Role, UserConflictError
from app.persistence.mysql_database import MySQLDatabase
from app.persistence.mysql_user_repository import MySQLUserRepository
from app.services.auth_service import AuthenticationError, AuthService
from app.services.user_admin_service import UserAdminService, WrongPasswordError

pytestmark = pytest.mark.skipif(
    os.getenv("P001_RUN_MYSQL_TESTS") != "1",
    reason="Set P001_RUN_MYSQL_TESTS=1 to run live MySQL integration tests.",
)


def test_mysql_fd07_accounts_passwords_and_lockout_guard():
    repo = MySQLUserRepository(MySQLDatabase())
    auth = AuthService(repo)
    accounts = UserAdminService(repo)
    suffix = uuid4().hex[:10]

    admin, _ = accounts.create_user("fd07_admin_" + suffix, "FD07 Admin", {Role.ADMINISTRATOR})
    with pytest.raises(UserConflictError):
        accounts.create_user("fd07_admin_" + suffix, "Duplicate", {Role.CANDIDATE})

    user, temp = accounts.create_user("fd07_user_" + suffix, "FD07 User", {Role.CANDIDATE})
    listed = {u.user_id: u for u in accounts.list_users()}[user.user_id]
    assert listed.must_change_password and listed.roles == frozenset({Role.CANDIDATE})
    assert user.user_id in {u.user_id for u in accounts.list_candidates()}

    token, _ = auth.login(user.username, temp)
    other_device, _ = auth.login(user.username, temp)
    assert auth.authenticate(token).must_change_password
    with pytest.raises(WrongPasswordError):
        accounts.change_own_password(user.user_id, "wrong", "a-long-enough-one", token)
    accounts.change_own_password(user.user_id, temp, "a-long-enough-one", token)
    assert not auth.authenticate(token).must_change_password
    assert auth.authenticate(other_device) is None  # other device signed out, this one kept
    with pytest.raises(AuthenticationError):
        auth.login(user.username, temp)

    accounts.set_roles(admin.user_id, user.user_id, {Role.EXAMINER, Role.CANDIDATE})
    assert auth.authenticate(token).roles == frozenset({Role.EXAMINER, Role.CANDIDATE})

    new_temp = accounts.reset_password(user.user_id)
    assert auth.authenticate(token) is None
    token, _ = auth.login(user.username, new_temp)
    assert auth.authenticate(token).must_change_password

    accounts.set_active(admin.user_id, user.user_id, False)
    assert auth.authenticate(token) is None
    with pytest.raises(AuthenticationError):
        auth.login(user.username, new_temp)
    accounts.set_active(admin.user_id, user.user_id, True)
    assert auth.authenticate(token) is None  # reactivation does not revive sessions

    # Last-administrator guard on a real server: deactivate every other active admin first.
    for other in accounts.list_users():
        if Role.ADMINISTRATOR in other.roles and other.is_active and other.user_id != admin.user_id:
            repo.set_active(other.user_id, False)
    with pytest.raises(UserConflictError, match="last active"):
        repo.set_active(admin.user_id, False)
    with pytest.raises(UserConflictError, match="last active"):
        repo.set_roles(admin.user_id, {Role.CANDIDATE})
    assert Role.ADMINISTRATOR in {u.user_id: u for u in accounts.list_users()}[admin.user_id].roles
