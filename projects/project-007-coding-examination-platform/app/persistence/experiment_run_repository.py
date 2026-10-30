"""Persistence for comparative B0-B4 experiment identity and method freeze."""
from datetime import datetime

from app.domain.experiment_run import (
    ExperimentRun, ExperimentRunStatus, FrozenMethodConfiguration,
)
from .database import Database


class ExperimentRunRepository:
    def __init__(self, database: Database):
        self.database = database

    def create(self, run: ExperimentRun) -> None:
        with self.database.connect() as connection:
            connection.execute(
                """INSERT INTO experiment_runs
                   (experiment_run_id, case_id, claim_id, corpus_version,
                    assessor_rubric_version, status, started_at, ended_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    run.experiment_run_id, run.case_id, run.claim_id,
                    run.corpus_version, run.assessor_rubric_version,
                    run.status.value, run.started_at.isoformat(),
                    run.ended_at.isoformat() if run.ended_at else None,
                ),
            )

    def freeze_method(self, config: FrozenMethodConfiguration) -> None:
        with self.database.connect() as connection:
            connection.execute(
                """INSERT INTO experiment_method_configurations
                   (experiment_run_id, method, method_version, configuration_version)
                   VALUES (?, ?, ?, ?)""",
                (
                    config.experiment_run_id, config.method,
                    config.method_version, config.configuration_version,
                ),
            )

    def method_configurations(self, experiment_run_id: str) -> tuple[FrozenMethodConfiguration, ...]:
        with self.database.connect() as connection:
            rows = connection.execute(
                """SELECT experiment_run_id, method, method_version, configuration_version
                   FROM experiment_method_configurations
                   WHERE experiment_run_id = ? ORDER BY method""",
                (experiment_run_id,),
            ).fetchall()
        return tuple(FrozenMethodConfiguration(**dict(row)) for row in rows)

    def finish(self, experiment_run_id: str, ended_at: datetime) -> None:
        with self.database.connect() as connection:
            cursor = connection.execute(
                """UPDATE experiment_runs SET status = 'COMPLETE', ended_at = ?
                   WHERE experiment_run_id = ? AND status = 'ACTIVE'""",
                (ended_at.isoformat(), experiment_run_id),
            )
            if cursor.rowcount != 1:
                raise ValueError("Experiment run does not exist or is not ACTIVE.")

    def get(self, experiment_run_id: str) -> ExperimentRun | None:
        with self.database.connect() as connection:
            row = connection.execute(
                "SELECT * FROM experiment_runs WHERE experiment_run_id = ?",
                (experiment_run_id,),
            ).fetchone()
        if row is None:
            return None
        return ExperimentRun(
            experiment_run_id=row["experiment_run_id"], case_id=row["case_id"],
            claim_id=row["claim_id"], corpus_version=row["corpus_version"],
            assessor_rubric_version=row["assessor_rubric_version"],
            status=ExperimentRunStatus(row["status"]),
            started_at=datetime.fromisoformat(row["started_at"]),
            ended_at=datetime.fromisoformat(row["ended_at"]) if row["ended_at"] else None,
        )
