"""Persistence for measured method observations and independent references."""
import json
from dataclasses import dataclass
from datetime import datetime

from app.domain.enums import EvidenceState
from app.services.experiment_record import IndependentReferenceJudgment
from app.services.verification_burden import VerificationBurden
from .database import Database


@dataclass(frozen=True)
class PersistedMethodObservation:
    experiment_run_id: str
    method: str
    system_state: EvidenceState
    evidence_ids: tuple[str, ...]
    burden: VerificationBurden
    recorded_at: datetime


class ExperimentObservationRepository:
    def __init__(self, database: Database):
        self.database = database

    def add_method_observation(self, observation: PersistedMethodObservation) -> None:
        with self.database.connect() as connection:
            connection.execute(
                """INSERT INTO experiment_method_observations
                   (experiment_run_id, method, system_state, evidence_ids,
                    question_count, verification_seconds, complexity, recorded_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    observation.experiment_run_id, observation.method,
                    observation.system_state.value,
                    json.dumps(observation.evidence_ids),
                    observation.burden.question_count,
                    observation.burden.verification_seconds,
                    json.dumps(observation.burden.complexity),
                    observation.recorded_at.isoformat(),
                ),
            )

    def add_reference(
        self, experiment_run_id: str, reference: IndependentReferenceJudgment,
        recorded_at: datetime,
    ) -> None:
        with self.database.connect() as connection:
            run = connection.execute(
                "SELECT claim_id, assessor_rubric_version FROM experiment_runs WHERE experiment_run_id = ?",
                (experiment_run_id,),
            ).fetchone()
            if run is None:
                raise ValueError("Unknown experiment run.")
            if reference.claim_id != run["claim_id"]:
                raise ValueError("Reference judgment must concern the experiment claim.")
            if reference.rubric_version != run["assessor_rubric_version"]:
                raise ValueError("Reference rubric must match the frozen experiment rubric.")
            connection.execute(
                """INSERT INTO experiment_reference_judgments
                   (experiment_run_id, assessor_id, claim_id, state, rationale,
                    rubric_version, recorded_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    experiment_run_id, reference.assessor_id, reference.claim_id,
                    reference.state.value, reference.rationale,
                    reference.rubric_version, recorded_at.isoformat(),
                ),
            )

    def observations(self, experiment_run_id: str) -> tuple[PersistedMethodObservation, ...]:
        with self.database.connect() as connection:
            rows = connection.execute(
                """SELECT * FROM experiment_method_observations
                   WHERE experiment_run_id = ? ORDER BY method""",
                (experiment_run_id,),
            ).fetchall()
        return tuple(
            PersistedMethodObservation(
                experiment_run_id=row["experiment_run_id"], method=row["method"],
                system_state=EvidenceState(row["system_state"]),
                evidence_ids=tuple(json.loads(row["evidence_ids"])),
                burden=VerificationBurden(
                    row["question_count"], row["verification_seconds"],
                    tuple(json.loads(row["complexity"])),
                ),
                recorded_at=datetime.fromisoformat(row["recorded_at"]),
            )
            for row in rows
        )
