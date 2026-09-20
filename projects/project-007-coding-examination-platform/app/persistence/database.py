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
