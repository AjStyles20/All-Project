"""The first-administrator script: no echo, policy enforced, nothing created on failure."""
import sys

import pytest

from app.domain.identity import Role
from app.security.passwords import verify_password
from scripts import create_admin
from tests.user_fakes import InMemoryUserRepository


@pytest.fixture
def run(monkeypatch, capsys):
    repo = InMemoryUserRepository()
    monkeypatch.setattr(create_admin, "MySQLUserRepository", lambda database: repo)
    monkeypatch.setattr(create_admin, "MySQLDatabase", lambda: None)

    def invoke(first, second, username="Root"):
        answers = iter([first, second])
        monkeypatch.setattr(create_admin, "getpass", lambda prompt: next(answers))
        monkeypatch.setattr(sys, "argv", ["create_admin", "--username", username, "--display-name", "Root User"])
        return create_admin.main(), capsys.readouterr().out
    return invoke, repo


def test_creates_administrator_who_need_not_change_password(run):
    invoke, repo = run
    code, out = invoke("correct-horse-battery", "correct-horse-battery")
    assert code == 0 and "correct-horse-battery" not in out
    [user] = repo.list_users()
    assert user.username == "root" and user.roles == frozenset({Role.ADMINISTRATOR})
    assert not user.must_change_password
    assert verify_password("correct-horse-battery", repo.get_by_id(user.user_id).password_hash)


@pytest.mark.parametrize("first,second", [("correct-horse-battery", "different-password-1"), ("short", "short"),
                                          ("has-root-inside-it", "has-root-inside-it")])
def test_bad_passwords_create_nothing(run, first, second):
    invoke, repo = run
    code, _ = invoke(first, second)
    assert code == 1 and repo.list_users() == []


def test_duplicate_username_is_reported_not_raised(run):
    invoke, _ = run
    assert invoke("correct-horse-battery", "correct-horse-battery")[0] == 0
    code, out = invoke("another-long-password", "another-long-password")
    assert code == 1 and "already taken" in out
