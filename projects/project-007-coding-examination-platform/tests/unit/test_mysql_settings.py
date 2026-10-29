from app.persistence.mysql_database import MySQLSettings


def test_mysql_settings_from_environment(monkeypatch):
    monkeypatch.setenv("P001_DB_HOST", "db.example")
    monkeypatch.setenv("P001_DB_PORT", "3307")
    monkeypatch.setenv("P001_DB_NAME", "exam")
    monkeypatch.setenv("P001_DB_USER", "app")
    monkeypatch.setenv("P001_DB_PASSWORD", "secret")
    settings = MySQLSettings.from_env()
    assert settings.host == "db.example"
    assert settings.port == 3307
    assert settings.database == "exam"
    assert settings.user == "app"
    assert settings.password == "secret"


def test_mysql_defaults_are_local_and_non_secret(monkeypatch):
    for name in ("P001_DB_HOST", "P001_DB_PORT", "P001_DB_NAME",
                 "P001_DB_USER", "P001_DB_PASSWORD"):
        monkeypatch.delenv(name, raising=False)
    settings = MySQLSettings.from_env()
    assert settings.host == "127.0.0.1"
    assert settings.port == 3306
    assert settings.database == "p001_coding_exam"
    assert settings.user == "p001_app"
    assert settings.password == ""


def test_connections_report_matched_rows(monkeypatch):
    # Guarded UPDATEs treat rowcount == 1 as "row found"; without FOUND_ROWS MySQL
    # reports 0 when the new values equal the old ones.
    import mysql.connector
    from mysql.connector.constants import ClientFlag
    from app.persistence.mysql_database import MySQLDatabase

    captured = {}

    class Connection:
        def commit(self): pass
        def rollback(self): pass
        def close(self): pass

    def fake_connect(**kwargs):
        captured.update(kwargs)
        return Connection()

    monkeypatch.setattr(mysql.connector, "connect", fake_connect)
    with MySQLDatabase(MySQLSettings()).connect():
        pass
    assert ClientFlag.FOUND_ROWS in captured["client_flags"]
