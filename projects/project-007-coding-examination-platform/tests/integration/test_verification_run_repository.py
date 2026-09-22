from datetime import datetime, timezone

import pytest

from app.domain.models import ProgrammingCase
from app.domain.verification_run import UsedProbe, VerificationRun, VerificationRunStatus
from app.persistence.database import Database
from app.persistence.repositories import P001Repository
from app.persistence.verification_run_repository import VerificationRunRepository


def setup_repo(tmp_path):
    db = Database(tmp_path / "run.db")
    db.initialize()
    P001Repository(db).add_case(ProgrammingCase(
        case_id="CASE-DEV-003", title="Find even numbers",
        task_description="Return even numbers.", language="python",
    ))
    return VerificationRunRepository(db)


def test_run_persists_versions_used_probes_and_terminal_decision(tmp_path):
    repo = setup_repo(tmp_path)
    started = datetime(2026, 9, 20, 11, 30, tzinfo=timezone.utc)
    repo.create(VerificationRun(
        run_id="RUN-003-01", case_id="CASE-DEV-003",
        method_version="B4-v1.0-development",
        configuration_version="PROBE-CATALOG-v1.0-development",
        status=VerificationRunStatus.ACTIVE, started_at=started,
    ))
    repo.record_used_probe(UsedProbe(
        run_id="RUN-003-01", probe_id="VP-CC3-02",
        claim_id="CC3", gap_type="EG-T3", used_at=started,
    ))
    assert repo.used_probe_ids("RUN-003-01") == frozenset({"VP-CC3-02"})

    ended = datetime(2026, 9, 20, 11, 35, tzinfo=timezone.utc)
    repo.finish(
        run_id="RUN-003-01",
        status=VerificationRunStatus.VERIFICATION_COMPLETE,
        ended_at=ended, final_decision="VERIFICATION_COMPLETE",
        final_rationale="All REQUIRED claims are supported.",
    )
    stored = repo.get("RUN-003-01")
    assert stored is not None
    assert stored.status is VerificationRunStatus.VERIFICATION_COMPLETE
    assert stored.configuration_version == "PROBE-CATALOG-v1.0-development"
    assert stored.ended_at == ended


def test_same_probe_cannot_be_recorded_twice_in_one_run(tmp_path):
    repo = setup_repo(tmp_path)
    now = datetime.now(timezone.utc)
    repo.create(VerificationRun(
        run_id="RUN-003-01", case_id="CASE-DEV-003",
        method_version="B4-v1.0-development", configuration_version="CFG-v1",
        status=VerificationRunStatus.ACTIVE, started_at=now,
    ))
    used = UsedProbe("RUN-003-01", "VP-CC3-02", "CC3", "EG-T3", now)
    repo.record_used_probe(used)
    with pytest.raises(Exception):
        repo.record_used_probe(used)


def test_terminal_run_cannot_be_finished_twice(tmp_path):
    repo = setup_repo(tmp_path)
    now = datetime.now(timezone.utc)
    repo.create(VerificationRun(
        run_id="RUN-003-01", case_id="CASE-DEV-003",
        method_version="B4-v1.0-development", configuration_version="CFG-v1",
        status=VerificationRunStatus.ACTIVE, started_at=now,
    ))
    repo.finish(
        run_id="RUN-003-01", status=VerificationRunStatus.HUMAN_REVIEW_REQUIRED,
        ended_at=now, final_decision="HUMAN_REVIEW_REQUIRED",
        final_rationale="No adequate unused probe remains.",
    )
    with pytest.raises(ValueError):
        repo.finish(
            run_id="RUN-003-01", status=VerificationRunStatus.VERIFICATION_COMPLETE,
            ended_at=now, final_decision="VERIFICATION_COMPLETE",
            final_rationale="Invalid second terminal transition.",
        )
