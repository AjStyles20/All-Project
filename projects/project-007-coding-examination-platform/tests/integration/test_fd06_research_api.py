from fastapi.testclient import TestClient

from app.api.mysql_platform_api import create_mysql_platform_app
from app.domain.identity import AuthenticatedPrincipal, Role
from app.services.examination_service import ExaminationService
from app.services.research_bridge_service import ResearchBridgeService
from tests.unit.test_research_bridge_service import World


class FakeAuth:
    TOKENS = {
        "admin-token": AuthenticatedPrincipal("admin-1", "admin", frozenset({Role.ADMINISTRATOR})),
        "examiner-token": AuthenticatedPrincipal("lecturer-1", "lecturer", frozenset({Role.EXAMINER})),
        "student-token": AuthenticatedPrincipal("student-1", "student", frozenset({Role.CANDIDATE})),
    }
    def authenticate(self, token): return self.TOKENS.get(token)
    def logout(self, token): return token in self.TOKENS


def bearer(token): return {"Authorization": "Bearer " + token}


def client_for(world):
    return TestClient(create_mysql_platform_app(
        auth_service=FakeAuth(), examination_service=ExaminationService(world.exam_repo),
        candidate_session_service=world.candidates, contract_service=world.contracts,
        research_bridge_service=world.bridge))


LINK = {"examination_id": "e1", "question_id": "q1", "template_case_id": "TPL-CC3",
        "claim_ids": ["CC3"], "ethics_reference": "ETH-2026-041"}


def test_research_flow_through_api(tmp_path):
    world = World(tmp_path)
    client = client_for(world)
    admin, student = bearer("admin-token"), bearer("student-token")

    assert client.post("/admin/research/links", json=LINK, headers=bearer("examiner-token")).status_code == 403
    assert client.get("/candidate/examinations/e1/research", headers=student).json()["study_linked"] is False
    assert client.post("/admin/research/links", json=LINK, headers=admin).status_code == 201

    info = client.get("/candidate/examinations/e1/research", headers=student).json()
    assert info["study_linked"] and info["ethics_references"] == ["ETH-2026-041"] and info["consent"] is None
    assert "identity are not copied" in info["collected"]
    assert client.put("/candidate/examinations/e1/research", json={"opt_in": True}, headers=student).json() == {"consent": "OPTED_IN"}

    assert client.post("/admin/research/examinations/e1/bridge", headers=admin).status_code == 409  # not CLOSED
    world.close()
    summary = client.post("/admin/research/examinations/e1/bridge", headers=admin).json()
    assert (summary["bridged"], summary["skipped_no_consent"]) == (1, 1)

    records = client.get("/admin/research/examinations/e1/records", headers=admin).json()
    assert [r["outcome"] for r in records] == ["BRIDGED"]
    identities = client.get("/admin/research/examinations/e1/identities", headers=admin).json()
    assert [i["candidate_user_id"] for i in identities] == ["student-1"]
    assert client.get("/admin/research/examinations/e1/identities", headers=bearer("examiner-token")).status_code == 403


def test_unconfigured_research_store_answers_503(tmp_path):
    world = World(tmp_path, configured=False)
    client = client_for(world)
    response = client.post("/admin/research/links", json=LINK, headers=bearer("admin-token"))
    assert response.status_code == 503 and "not configured" in response.json()["detail"]


def test_withdrawal_through_api_reports_deletion(tmp_path):
    world = World(tmp_path)
    client = client_for(world)
    admin, student = bearer("admin-token"), bearer("student-token")
    client.post("/admin/research/links", json=LINK, headers=admin)
    client.put("/candidate/examinations/e1/research", json={"opt_in": True}, headers=student)
    world.close()
    client.post("/admin/research/examinations/e1/bridge", headers=admin)
    withdrawn = client.put("/candidate/examinations/e1/research", json={"opt_in": False}, headers=student).json()
    assert withdrawn == {"consent": "WITHDRAWN", "research_cases_deleted": 1, "deletion_pending": False}
    log = client.get("/admin/research/examinations/e1/withdrawals", headers=admin).json()
    assert [(row["cases_deleted"], row["cases_retained_as_shell"]) for row in log] == [(1, 0)]
    assert "candidate_user_id" not in log[0]
    assert client.get("/admin/research/examinations/e1/identities", headers=admin).json() == []


def test_admin_lists_exam_questions_for_the_link_form(tmp_path):
    world = World(tmp_path)
    client = client_for(world)
    listed = client.get("/admin/research/examinations/e1/questions", headers=bearer("admin-token"))
    assert listed.status_code == 200
    assert [q["question_id"] for q in listed.json()] == ["q1", "q2"]
    assert set(listed.json()[0]) == {"question_id", "title"}  # no prompts, answers or scores
    assert client.get("/admin/research/examinations/e1/questions", headers=bearer("examiner-token")).status_code == 403
    assert client.get("/admin/research/examinations/nope/questions", headers=bearer("admin-token")).status_code == 404
