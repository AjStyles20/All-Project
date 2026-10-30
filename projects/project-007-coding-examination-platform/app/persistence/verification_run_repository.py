"""Persistence for B4 verification sessions and probe exhaustion state."""
from datetime import datetime

from app.domain.verification_run import UsedProbe, VerificationRun, VerificationRunStatus
from .database import Database


class VerificationRunRepository:
    def __init__(self, database: Database):
        self.database = database

    def create(self, run: VerificationRun) -> None:
        with self.database.connect() as connection:
            connection.execute(
                """INSERT INTO verification_runs
                   (run_id, case_id, method_version, configuration_version, status,
                    started_at, ended_at, final_decision, final_rationale)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    run.run_id, run.case_id, run.method_version,
                    run.configuration_version, run.status.value,
                    run.started_at.isoformat(),
                    run.ended_at.isoformat() if run.ended_at else None,
                    run.final_decision, run.final_rationale,
                ),
            )

    def record_used_probe(self, probe: UsedProbe) -> None:
        with self.database.connect() as connection:
            connection.execute(
                """INSERT INTO verification_run_probes
                   (run_id, probe_id, claim_id, gap_type, used_at)
                   VALUES (?, ?, ?, ?, ?)""",
                (probe.run_id, probe.probe_id, probe.claim_id,
                 probe.gap_type, probe.used_at.isoformat()),
            )

    def used_probe_ids(self, run_id: str) -> frozenset[str]:
        with self.database.connect() as connection:
            rows = connection.execute(
                """SELECT probe_id FROM verification_run_probes
                   WHERE run_id = ? ORDER BY used_at, probe_id""", (run_id,)
            ).fetchall()
        return frozenset(row["probe_id"] for row in rows)

    def finish(
        self, *, run_id: str, status: VerificationRunStatus,
        ended_at: datetime, final_decision: str, final_rationale: str,
    ) -> None:
        if status is VerificationRunStatus.ACTIVE:
            raise ValueError("A finished verification run cannot remain ACTIVE.")
        with self.database.connect() as connection:
            cursor = connection.execute(
                """UPDATE verification_runs
                   SET status = ?, ended_at = ?, final_decision = ?, final_rationale = ?
                   WHERE run_id = ? AND status = 'ACTIVE'""",
                (status.value, ended_at.isoformat(), final_decision,
                 final_rationale, run_id),
            )
            if cursor.rowcount != 1:
                raise ValueError("Verification run does not exist or is already terminal.")

    def get(self, run_id: str) -> VerificationRun | None:
        with self.database.connect() as connection:
            row = connection.execute(
                "SELECT * FROM verification_runs WHERE run_id = ?", (run_id,)
            ).fetchone()
        if row is None:
            return None
        return VerificationRun(
            run_id=row["run_id"], case_id=row["case_id"],
            method_version=row["method_version"],
            configuration_version=row["configuration_version"],
            status=VerificationRunStatus(row["status"]),
            started_at=datetime.fromisoformat(row["started_at"]),
            ended_at=datetime.fromisoformat(row["ended_at"]) if row["ended_at"] else None,
            final_decision=row["final_decision"],
            final_rationale=row["final_rationale"],
        )
