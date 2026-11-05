"""Tests follow the Pass 018 truth tables and experiments E1-E8."""
import pytest
from fastapi.testclient import TestClient

from p002.app import create_app
from p002.course import FORUM, build
from p002.domain import Assistance, Authority, ClaimStatus, EdgeType, IssueState, Mastery, PolicyError, Relation
from p002.evaluation import random_course, reference_flags
from p002.mastery import MasteryKernel
from p002.provenance import TrustKernel
from p002.roles import CURATOR, EXPLAINER, QUIZ_WRITER, derive, require


def kernel_with_source(authority=Authority.CANONICAL_APPROVED):
    k = TrustKernel()
    s = k.add_source("Notes", "v1", "text", authority)
    return k, s


# ---------- APLDG truth table ----------

def test_verbatim_copy_keeps_ancestry_and_never_exceeds_the_source():
    k, s = kernel_with_source(Authority.TRUSTED_REFERENCE)
    c = k.add_claim("fact", Authority.CANONICAL_APPROVED, CURATOR.actor, [(s.id, Relation.SUPPORTS)])
    assert c.authority is Authority.TRUSTED_REFERENCE          # capped by its source
    copy = derive(k, CURATOR, [c.id], "paraphrase", text="fact", edge=EdgeType.REUSE)
    assert copy.authority <= Authority.TRUSTED_REFERENCE and copy.parents[0][0] == c.id


def test_e1_unsupported_ai_claim_cannot_be_laundered_by_other_roles():
    k = TrustKernel()
    guess = k.add_claim("CROSS JOIN needs ON", Authority.CANONICAL_APPROVED, EXPLAINER.actor)
    hop = guess
    for role in (QUIZ_WRITER, EXPLAINER, QUIZ_WRITER, CURATOR):
        hop = derive(k, role, [hop.id], "paraphrase", edge=EdgeType.REUSE)
        assert hop.authority <= Authority.AI_DERIVED
    assert k.explain(hop.id).status is ClaimStatus.UNVERIFIED
    ancestors, cid = [], hop.id
    while k.claims[cid].parents:
        cid = k.claims[cid].parents[0][0]
        ancestors.append(cid)
    assert ancestors[-1] == guess.id   # the AI origin is still traceable after four hand-offs


def test_e2_lineage_survives_repeated_transformation():
    k, s = kernel_with_source()
    c = k.add_claim("fact", Authority.CANONICAL_APPROVED, CURATOR.actor, [(s.id, Relation.SUPPORTS)])
    chain = [c.id]
    for edge in (EdgeType.PARAPHRASE, EdgeType.SUMMARY, EdgeType.INFERENCE):
        chain.append(derive(k, EXPLAINER, [chain[-1]], "paraphrase", edge=edge).id)
    # Walking parents from the last claim reaches the original.
    cid, seen = chain[-1], []
    while k.claims[cid].parents:
        cid = k.claims[cid].parents[0][0]
        seen.append(cid)
    assert seen[-1] == c.id


def test_e3_supersession_marks_claims_and_everything_built_on_them():
    k, ids = build()
    assert k.explain(ids["natural"]).status is ClaimStatus.STALE
    assert k.explain(ids["natural-explained"]).status is ClaimStatus.STALE
    assert k.artifact_status(ids["lesson"])[0].value == "STALE"
    assert k.artifact_status(ids["style-guide"])[0].value == "STALE"
    # Claims re-confirmed by v2 stay current.
    assert k.explain(ids["left"]).status is ClaimStatus.CURRENT
    assert k.artifact_status(ids["quiz-left"])[0].value == "CURRENT"


def test_e4_trusted_conflict_is_explicit_with_no_silent_winner():
    k, s = kernel_with_source()
    other = k.add_source("Other book", "v1", "other", Authority.TRUSTED_REFERENCE)
    c = k.add_claim("fact", Authority.CANONICAL_APPROVED, CURATOR.actor, [(s.id, Relation.SUPPORTS)])
    k.add_evidence(c.id, other.id, Relation.CONTRADICTS)
    e = k.explain(c.id)
    assert e.status is ClaimStatus.CONFLICTED and "disagree" in e.reasons[0]
    a = k.add_artifact("quiz", "q", [c.id])
    assert k.artifact_status(a.id)[0].value == "CONFLICTED"


def test_low_authority_contradiction_does_not_override_canonical_knowledge():
    k, ids = build()
    assert k.explain(ids["left"]).status is ClaimStatus.CURRENT   # the forum post disagrees


def test_learner_assertion_stays_learner_provided():
    k, s = kernel_with_source()
    c = k.add_claim("LEFT JOIN drops rows", Authority.CANONICAL_APPROVED, "learner:me")
    assert c.authority is Authority.HUMAN_ASSERTION and k.explain(c.id).status is ClaimStatus.UNVERIFIED


def test_promotion_needs_a_person_and_a_trusted_source():
    k, s = kernel_with_source()
    c = k.add_claim("fact", Authority.HUMAN_ASSERTION, "human:teacher")
    with pytest.raises(PolicyError):
        k.promote(c.id, Authority.CANONICAL_APPROVED, "ai:explainer", s.id)
    with pytest.raises(PolicyError):
        k.promote(c.id, Authority.CANONICAL_APPROVED, "human:teacher", s.id)   # not linked yet
    k.add_evidence(c.id, s.id, Relation.SUPPORTS)
    k.promote(c.id, Authority.CANONICAL_APPROVED, "human:teacher", s.id)
    assert c.authority is Authority.CANONICAL_APPROVED and k.audit[-1]["event"] == "CLAIM_PROMOTED"


def test_e8_text_in_a_source_cannot_change_anything():
    k, ids = build()
    forum = k.sources[ids["forum"]]
    assert "SYSTEM:" in forum.text and forum.text == FORUM
    assert forum.authority is Authority.COMMUNITY_ASSERTION
    assert all(e["event"] != "CLAIM_PROMOTED" for e in k.audit)


def test_role_contracts_are_enforced():
    with pytest.raises(PolicyError):
        require(EXPLAINER, "promote")
    require(CURATOR, "promote")


def test_random_courses_match_the_reference():
    for seed in range(3):
        k = random_course(seed, True)
        flagged, artifacts = reference_flags(k)
        got = {a for a in k.artifacts if k.artifact_status(a)[0].value in ("STALE", "CONFLICTED")}
        assert got == artifacts


def test_baseline_b2_records_but_does_not_propagate():
    k, ids = build(propagate=False)
    assert k.explain(ids["natural"]).status is ClaimStatus.CURRENT
    assert k.claims[ids["natural-explained"]].parents   # provenance still recorded


# ---------- PGAIC truth table ----------

def steps(level):
    return [(Assistance(lv), "asked") for lv in range(1, level + 1)]


@pytest.mark.parametrize("level,expected", [(0, Mastery.VERIFYING), (1, Mastery.PROVISIONAL), (2, Mastery.PROVISIONAL),
                                            (3, Mastery.ASSISTED_SUCCESS), (6, Mastery.ASSISTED_SUCCESS)])
def test_e5_same_answer_different_evidence_by_help(level, expected):
    k = MasteryKernel()
    k.record("me", "join", "q", True, steps(level))
    assert k.state("me", "join").mastery is expected


def test_direct_answer_success_never_becomes_independent():
    k = MasteryKernel()
    for _ in range(5):
        k.record("me", "join", "q", True, steps(6))
    assert k.state("me", "join").mastery is Mastery.ASSISTED_SUCCESS


def test_near_miss_triggers_reverification():
    k = MasteryKernel()
    k.record("me", "join", "q", True, reasoning_ok=False)
    assert k.state("me", "join").mastery is Mastery.VERIFYING and "near miss" in k.state("me", "join").reasons[0]


def test_e6_assisted_success_then_unaided_failure_is_not_mastery():
    k = MasteryKernel()
    k.record("me", "join", "q", True, steps(5))
    k.record("me", "join", "check", False, verification=True)
    assert k.state("me", "join").mastery is Mastery.REOPENED


def test_e7_assisted_success_then_unaided_success_is_independent_and_can_reopen():
    k = MasteryKernel()
    k.record("me", "join", "q", True, steps(4))
    k.record("me", "join", "check", True, verification=True)
    assert k.state("me", "join").mastery is Mastery.INDEPENDENT
    k.record("me", "join", "check", False, verification=True)
    assert k.state("me", "join").mastery is Mastery.REOPENED


def test_accommodation_never_lowers_mastery():
    with_support, without = MasteryKernel(), MasteryKernel()
    for k, acc in ((with_support, "screen reader"), (without, None)):
        k.record("me", "join", "q", True, accommodation=acc)
        k.record("me", "join", "check", True, verification=True, accommodation=acc)
    assert with_support.state("me", "join").mastery is without.state("me", "join").mastery is Mastery.INDEPENDENT


def test_help_escalation_rules():
    k = MasteryKernel()
    trail = []
    k.escalate(trail, Assistance.L1_METACOGNITIVE, "stuck")
    with pytest.raises(PolicyError):
        k.escalate(trail, Assistance.L3_TARGETED_HINT, "skip")
    with pytest.raises(PolicyError):
        k.escalate(trail, Assistance.L2_CONCEPTUAL_CUE, "")
    with pytest.raises(PolicyError):
        k.record("me", "join", "check", True, steps(1), verification=True)


def test_knowledge_issue_needs_independent_evidence_and_reopens():
    k = MasteryKernel()
    i = k.open_issue("me", "join", "LEFT vs INNER")
    k.move_issue(i.id, IssueState.WORKING)
    k.move_issue(i.id, IssueState.VERIFYING)
    with pytest.raises(PolicyError):
        k.move_issue(i.id, IssueState.RESOLVED)
    k.record("me", "join", "q", True)
    k.record("me", "join", "check", True, verification=True)
    k.move_issue(i.id, IssueState.RESOLVED)
    k.record("me", "join", "check", False, verification=True)
    assert k.issues[i.id].state is IssueState.REOPENED and k.issues[i.id].reopen_count == 1


# ---------- app ----------

def client(tmp_path):
    return TestClient(create_app(tmp_path / "w.sqlite3", "tok"), base_url="http://127.0.0.1"), {"X-Token": "tok"}


def test_app_requires_token_and_local_host(tmp_path):
    c, h = client(tmp_path)
    assert c.get("/api/practice").status_code == 401
    other = TestClient(create_app(tmp_path / "x.sqlite3", "tok"), base_url="http://evil.example")
    assert other.get("/api/practice", headers=h).status_code == 403


def test_practice_flow_with_help_then_check(tmp_path):
    c, h = client(tmp_path)
    q = c.get("/api/practice", headers=h).json()["question"]
    assert q["id"] == "q-inner" and "hints" in q and "answer" not in q
    for _ in range(6):
        q = c.post("/api/hint", headers=h, json={"question_id": q["id"]}).json()["question"]
    assert c.post("/api/hint", headers=h, json={"question_id": q["id"]}).status_code == 409
    r = c.post("/api/answer", headers=h, json={"question_id": "q-inner", "choice": 0}).json()
    assert r["correct"] and r["help_level"] == 6 and r["mastery"] == "ASSISTED_SUCCESS"
    check = c.get("/api/practice", headers=h).json()["question"]
    assert check["check"] and check["id"] == "q-inner-check"
    assert c.post("/api/hint", headers=h, json={"question_id": check["id"]}).status_code == 409
    r = c.post("/api/answer", headers=h, json={"question_id": check["id"], "choice": 0}).json()
    assert r["mastery"] == "INDEPENDENT"


def test_progress_survives_restart(tmp_path):
    c, h = client(tmp_path)
    c.post("/api/answer", headers=h, json={"question_id": "q-left", "choice": 1})
    c2, _ = client(tmp_path)
    left = next(x for x in c2.get("/api/mastery", headers=h).json()["concepts"] if x["concept"] == "left-join")
    assert left["mastery"] == "VERIFYING" and len(left["trail"]) == 1


def test_course_view_explains_trust(tmp_path):
    c, h = client(tmp_path)
    data = c.get("/api/course", headers=h).json()
    natural = next(x for x in data["claims"] if x["text"].startswith("NATURAL JOIN"))
    assert natural["status"] == "STALE" and "superseded" in natural["reasons"][0]
    assert any(a["status"] == "STALE" for a in data["artifacts"])


def test_issue_cannot_be_resolved_without_evidence(tmp_path):
    c, h = client(tmp_path)
    c.post("/api/issues", headers=h, json={"concept": "left-join", "description": "NULL rows"})
    issue = c.get("/api/mastery", headers=h).json()["issues"][0]
    for to in ("WORKING", "VERIFYING"):
        assert c.post(f"/api/issues/{issue['id']}/move", headers=h, json={"to": to}).status_code == 200
    assert c.post(f"/api/issues/{issue['id']}/move", headers=h, json={"to": "RESOLVED"}).status_code == 409
