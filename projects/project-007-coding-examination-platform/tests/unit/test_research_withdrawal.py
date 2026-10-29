"""DR-016: withdrawal deletes bridged research data; the store must live outside the app."""
import sqlite3
from pathlib import Path

import pytest

from app.domain.research_bridge import ResearchStoreNotConfigured
from app.persistence.database import Database
from app.persistence.repositories import P001Repository
from app.persistence.research_case_store import ResearchCaseStore
from app.services.research_bridge_service import APPLICATION_DIR
from tests.unit.test_research_bridge_service import World


def count(world, table):
    connection = sqlite3.connect(world.db.path)
    total = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    connection.close()
    return total


def bridged_world(tmp_path):
    world = World(tmp_path)
    world.link()
    world.bridge.set_consent("e1", "student-1", True)
    world.bridge.set_consent("e1", "student-2", True)
    world.close()
    assert world.bridge.run("e1").bridged == 2
    return world


def test_withdrawal_deletes_that_candidates_cases_and_unlinks_the_code(tmp_path):
    world = bridged_world(tmp_path)
    code_1 = world.research_repo.get_research_code("e1", "student-1")
    result = world.bridge.set_consent("e1", "student-1", False)
    assert (result.withdrawal.cases_deleted, result.withdrawal.purge_pending) == (1, False)

    store = ResearchCaseStore(world.db)
    assert store.get_case(f"op-{code_1}-q1") is None
    assert count(world, "evidence_items") == 2  # only student-2's artifact + policy remain
    assert "def test_add" not in world.research_text()
    # Operationally: code link and bridge records forgotten; the log keeps only the code.
    assert world.research_repo.get_research_code("e1", "student-1") is None
    assert world.research_repo.bridged_case_ids("e1", "student-1") == []
    assert [row["research_code"] for row in world.research_repo.withdrawal_log] == [code_1]
    assert world.research_repo.bridged_case_ids("e1", "student-2") != []


def test_case_referenced_by_analysis_is_kept_as_empty_shell(tmp_path):
    world = bridged_world(tmp_path)
    code_1 = world.research_repo.get_research_code("e1", "student-1")
    case_id = f"op-{code_1}-q1"
    from datetime import datetime
    from app.domain.enums import EvidenceState
    from app.domain.models import EvidenceStateRecord
    # An analysis already recorded a state for this case.
    P001Repository(world.db).append_evidence_state(
        EvidenceStateRecord(case_id, "CC3", EvidenceState.UNRESOLVED, "analysis", datetime(2026, 11, 5), "B3"))
    result = world.bridge.set_consent("e1", "student-1", False)
    assert (result.withdrawal.cases_deleted, result.withdrawal.cases_retained_as_shell) == (0, 1)
    assert ResearchCaseStore(world.db).get_case(case_id) is not None  # shell kept
    connection = sqlite3.connect(world.db.path)
    remaining = connection.execute("SELECT COUNT(*) FROM evidence_items WHERE case_id = ?", (case_id,)).fetchone()[0]
    connection.close()
    assert remaining == 0  # but the evidence is gone


def test_unavailable_store_keeps_withdrawal_and_marks_deletion_pending(tmp_path):
    world = bridged_world(tmp_path)
    store = world.bridge.store
    world.bridge.store = None
    result = world.bridge.set_consent("e1", "student-1", False)
    assert result.withdrawal.purge_pending
    # The withdrawal itself is already recorded, so no further copying can happen.
    from app.domain.research_bridge import ConsentStatus
    assert world.research_repo.current_consent("e1", "student-1") is ConsentStatus.WITHDRAWN
    world.bridge.store = store
    retry = world.bridge.purge_withdrawn("e1")
    assert (retry.cases_deleted, retry.purge_pending) == (1, False)
    assert world.research_repo.get_research_code("e1", "student-1") is None
    assert world.bridge.purge_withdrawn("e1").cases_deleted == 0  # idempotent


def test_re_consent_after_withdrawal_bridges_again_under_a_new_code(tmp_path):
    world = bridged_world(tmp_path)
    old_code = world.research_repo.get_research_code("e1", "student-1")
    world.bridge.set_consent("e1", "student-1", False)
    world.bridge.set_consent("e1", "student-1", True)
    assert world.bridge.run("e1").bridged == 1
    assert world.research_repo.get_research_code("e1", "student-1") not in (None, old_code)


def test_store_inside_application_directory_is_refused(tmp_path):
    world = World(tmp_path)
    inside = APPLICATION_DIR / "research-store-should-not-be-here.sqlite3"
    world.bridge.store = ResearchCaseStore(Database(inside))
    with pytest.raises(ResearchStoreNotConfigured, match="outside the application directory"):
        world.link()
    assert not inside.exists()
