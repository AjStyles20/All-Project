"""MySQL connection adapter for the P001 operational product layer.

MySQL Server is the canonical full-product DBMS. Credentials are supplied via
environment variables; this module never contains application secrets.
"""
from contextlib import contextmanager
from dataclasses import dataclass
import os
from typing import Iterator

import mysql.connector
from mysql.connector import MySQLConnection


@dataclass(frozen=True)
class MySQLSettings:
    host: str = "127.0.0.1"
    port: int = 3306
    database: str = "p001_coding_exam"
    user: str = "p001_app"
    password: str = ""

    @classmethod
    def from_env(cls) -> "MySQLSettings":
        return cls(
            host=os.getenv("P001_DB_HOST", "127.0.0.1"),
            port=int(os.getenv("P001_DB_PORT", "3306")),
            database=os.getenv("P001_DB_NAME", "p001_coding_exam"),
            user=os.getenv("P001_DB_USER", "p001_app"),
            password=os.getenv("P001_DB_PASSWORD", ""),
        )


class MySQLDatabase:
    def __init__(self, settings: MySQLSettings | None = None):
        self.settings = settings or MySQLSettings.from_env()

    @contextmanager
    def connect(self) -> Iterator[MySQLConnection]:
        connection = mysql.connector.connect(
            host=self.settings.host,
            port=self.settings.port,
            database=self.settings.database,
            user=self.settings.user,
            password=self.settings.password,
            autocommit=False,
        )
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()
