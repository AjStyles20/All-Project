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
