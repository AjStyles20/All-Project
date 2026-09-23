"""Opt-in live MySQL integration test.

Skipped unless P001_RUN_MYSQL_TESTS=1 so ordinary CI never pretends a live
MySQL server exists. Uses the configured development/test schema.
"""
import os
from uuid import uuid4

import pytest

from app.domain.identity import Role
from app.persistence.mysql_database import MySQLDatabase
from app.persistence.mysql_user_repository import MySQLUserRepository
from app.services.auth_service import AuthService


pytestmark = pytest.mark.skipif(
    os.getenv("P001_RUN_MYSQL_TESTS") != "1",
    reason="Set P001_RUN_MYSQL_TESTS=1 to run live MySQL integration tests.",
)


def test_mysql_identity_login_and_revoke():
    repository = MySQLUserRepository(MySQLDatabase())
    service = AuthService(repository)
    suffix = uuid4().hex[:10]
    user_id = "mysql-test-" + suffix
    username = "mysql_test_" + suffix

    service.create_user(
        user_id, username, "TemporaryTestPass123!",
        "MySQL Integration Test", {Role.CANDIDATE},
    )
    token, _ = service.login(username, "TemporaryTestPass123!")
    principal = service.authenticate(token)
    assert principal is not None
    assert principal.user_id == user_id
    assert Role.CANDIDATE in principal.roles
    assert service.logout(token)
    assert service.authenticate(token) is None
