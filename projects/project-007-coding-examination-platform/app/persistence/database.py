"""SQLite persistence for the P001 research-critical prototype.

The schema mirrors the M1 domain model. Evidence-state history is append-only:
the repository exposes INSERT and SELECT operations but no UPDATE/DELETE method.
"""
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS programming_cases (
    case_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    task_description TEXT NOT NULL,
    language TEXT NOT NULL,
    version TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS competence_claim_definitions (
    claim_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    definition TEXT NOT NULL,
    version TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS case_claims (
    case_id TEXT NOT NULL,
    claim_id TEXT NOT NULL,
    applicability TEXT NOT NULL
        CHECK (applicability IN ('REQUIRED', 'NOT_APPLICABLE')),
    PRIMARY KEY (case_id, claim_id),
    FOREIGN KEY (case_id) REFERENCES programming_cases(case_id),
    FOREIGN KEY (claim_id) REFERENCES competence_claim_definitions(claim_id)
);

CREATE TABLE IF NOT EXISTS evidence_items (
    evidence_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    evidence_type TEXT NOT NULL
        CHECK (evidence_type IN (
            'ARTIFACT', 'PROCESS', 'EXECUTION',
            'RUBRIC', 'VERIFICATION', 'POLICY_CONTEXT'
        )),
    content TEXT NOT NULL,
    source_type TEXT NOT NULL,
    created_at TEXT NOT NULL,
    policy_version TEXT,
    assistance_context TEXT,
    FOREIGN KEY (case_id) REFERENCES programming_cases(case_id)
);

CREATE TABLE IF NOT EXISTS claim_evidence_links (
    case_id TEXT NOT NULL,
    claim_id TEXT NOT NULL,
    evidence_id TEXT NOT NULL,
    rationale TEXT NOT NULL,
    PRIMARY KEY (case_id, claim_id, evidence_id),
    FOREIGN KEY (case_id) REFERENCES programming_cases(case_id),
    FOREIGN KEY (claim_id) REFERENCES competence_claim_definitions(claim_id),
    FOREIGN KEY (evidence_id) REFERENCES evidence_items(evidence_id)
);

CREATE TABLE IF NOT EXISTS evidence_state_history (
    state_record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id TEXT NOT NULL,
    claim_id TEXT NOT NULL,
    state TEXT NOT NULL
        CHECK (state IN ('SUPPORTED', 'PARTIAL', 'UNRESOLVED', 'CONTRADICTED')),
    rationale TEXT NOT NULL,
    recorded_at TEXT NOT NULL,
    source TEXT NOT NULL,
    FOREIGN KEY (case_id) REFERENCES programming_cases(case_id),
    FOREIGN KEY (claim_id) REFERENCES competence_claim_definitions(claim_id)
);

CREATE TABLE IF NOT EXISTS verification_runs (
    run_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    method_version TEXT NOT NULL,
    configuration_version TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN (
        'ACTIVE', 'VERIFICATION_COMPLETE', 'HUMAN_REVIEW_REQUIRED'
    )),
    started_at TEXT NOT NULL,
    ended_at TEXT,
    final_decision TEXT,
    final_rationale TEXT,
    FOREIGN KEY (case_id) REFERENCES programming_cases(case_id)
);

CREATE TABLE IF NOT EXISTS verification_run_probes (
    run_id TEXT NOT NULL,
    probe_id TEXT NOT NULL,
    claim_id TEXT NOT NULL,
    gap_type TEXT NOT NULL,
    used_at TEXT NOT NULL,
    PRIMARY KEY (run_id, probe_id),
    FOREIGN KEY (run_id) REFERENCES verification_runs(run_id)
);

CREATE INDEX IF NOT EXISTS idx_verification_runs_case
    ON verification_runs(case_id, started_at);

CREATE TABLE IF NOT EXISTS probe_candidate_audit (
    candidate_audit_seq INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT NOT NULL,
    case_id TEXT NOT NULL,
    claim_id TEXT NOT NULL,
    gap_type TEXT NOT NULL,
    probe_id TEXT NOT NULL,
    admissible INTEGER NOT NULL CHECK (admissible IN (0, 1)),
    potentially_sufficient INTEGER NOT NULL CHECK (potentially_sufficient IN (0, 1)),
    burden_rank INTEGER NOT NULL,
    disposition TEXT NOT NULL,
    rationale TEXT NOT NULL,
    FOREIGN KEY (case_id) REFERENCES programming_cases(case_id),
    UNIQUE (event_id, probe_id)
);

CREATE INDEX IF NOT EXISTS idx_probe_candidate_audit_case
    ON probe_candidate_audit(case_id, candidate_audit_seq);

CREATE TABLE IF NOT EXISTS audit_events (
    audit_event_seq INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT NOT NULL UNIQUE,
    case_id TEXT NOT NULL,
    event_type TEXT NOT NULL
        CHECK (event_type IN (
            'EVIDENCE_STATE_RECORDED', 'GAP_DETECTED', 'PROBE_SELECTION',
            'PROBE_RESULT_RECORDED', 'CONTROL_DECISION'
        )),
    recorded_at TEXT NOT NULL,
    actor_type TEXT NOT NULL,
    rationale TEXT NOT NULL,
    claim_id TEXT,
    gap_type TEXT,
    probe_id TEXT,
    evidence_id TEXT,
    from_state TEXT,
    to_state TEXT,
    decision TEXT,
    method_version TEXT,
    FOREIGN KEY (case_id) REFERENCES programming_cases(case_id)
);

CREATE INDEX IF NOT EXISTS idx_audit_case
    ON audit_events(case_id, audit_event_seq);

CREATE TABLE IF NOT EXISTS experiment_runs (
    experiment_run_id TEXT PRIMARY KEY,
    case_id TEXT NOT NULL,
    claim_id TEXT NOT NULL,
    corpus_version TEXT NOT NULL,
    assessor_rubric_version TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('ACTIVE', 'COMPLETE', 'INVALID')),
    started_at TEXT NOT NULL,
    ended_at TEXT,
    FOREIGN KEY (case_id) REFERENCES programming_cases(case_id),
    FOREIGN KEY (claim_id) REFERENCES competence_claim_definitions(claim_id)
);

CREATE TABLE IF NOT EXISTS experiment_method_configurations (
    experiment_run_id TEXT NOT NULL,
    method TEXT NOT NULL CHECK (method IN ('B0', 'B1', 'B2', 'B3', 'B4')),
    method_version TEXT NOT NULL,
    configuration_version TEXT NOT NULL,
    PRIMARY KEY (experiment_run_id, method),
    FOREIGN KEY (experiment_run_id) REFERENCES experiment_runs(experiment_run_id)
);

CREATE INDEX IF NOT EXISTS idx_experiment_runs_case_claim
    ON experiment_runs(case_id, claim_id, started_at);

CREATE TABLE IF NOT EXISTS experiment_method_observations (
    experiment_run_id TEXT NOT NULL,
    method TEXT NOT NULL CHECK (method IN ('B0', 'B1', 'B2', 'B3', 'B4')),
    system_state TEXT NOT NULL CHECK (
        system_state IN ('SUPPORTED', 'PARTIAL', 'UNRESOLVED', 'CONTRADICTED')
    ),
    evidence_ids TEXT NOT NULL,
    question_count INTEGER NOT NULL CHECK (question_count >= 0),
    verification_seconds REAL NOT NULL CHECK (verification_seconds >= 0),
    complexity TEXT NOT NULL,
    recorded_at TEXT NOT NULL,
    PRIMARY KEY (experiment_run_id, method),
    FOREIGN KEY (experiment_run_id, method)
        REFERENCES experiment_method_configurations(experiment_run_id, method)
);

CREATE TABLE IF NOT EXISTS experiment_reference_judgments (
    experiment_run_id TEXT PRIMARY KEY,
    assessor_id TEXT NOT NULL,
    claim_id TEXT NOT NULL,
    state TEXT NOT NULL CHECK (
        state IN ('SUPPORTED', 'PARTIAL', 'UNRESOLVED', 'CONTRADICTED')
    ),
    rationale TEXT NOT NULL,
    rubric_version TEXT NOT NULL,
    recorded_at TEXT NOT NULL,
    FOREIGN KEY (experiment_run_id) REFERENCES experiment_runs(experiment_run_id),
    FOREIGN KEY (claim_id) REFERENCES competence_claim_definitions(claim_id)
);


CREATE INDEX IF NOT EXISTS idx_evidence_case
    ON evidence_items(case_id);

CREATE INDEX IF NOT EXISTS idx_state_history_case_claim
    ON evidence_state_history(case_id, claim_id, state_record_id);
"""


class Database:
    def __init__(self, path: str | Path):
        self.path = str(path)

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(SCHEMA)
