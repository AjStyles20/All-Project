from fastapi.testclient import TestClient

from app.api.mysql_platform_api import create_mysql_platform_app
from app.domain.identity import AuthenticatedPrincipal, Role
from app.services.candidate_session_service import CandidateSessionService
from app.services.contract_service import ContractService
from app.services.examination_service import ExaminationService
from tests.candidate_session_fakes import InMemoryCandidateSessionRepository
from tests.contract_fakes import InMemoryContractRepository
from tests.contract_helpers import LAB_CAPABILITIES
from tests.examination_fakes import InMemoryExaminationRepository


class FakeAuth:
    TOKENS = {
        "examiner-token": AuthenticatedPrincipal("lecturer-1", "lecturer", frozenset({Role.EXAMINER})),
        "student-token": AuthenticatedPrincipal("student-1", "student", frozenset({Role.CANDIDATE})),
        "student2-token": AuthenticatedPrincipal("student-2", "student2", frozenset({Role.CANDIDATE})),
    }
    def authenticate(self, token): return self.TOKENS.get(token)
    def logout(self, token): return token in self.TOKENS


def bearer(token): return {"Authorization": "Bearer " + token}


def client_with_exam():
    exams = InMemoryExaminationRepository()
    contract_repo = InMemoryContractRepository(exams)
    session_repo = InMemoryCandidateSessionRepository({"student-1", "student-2"})
    client = TestClient(create_mysql_platform_app(
        auth_service=FakeAuth(), examination_service=ExaminationService(exams),
        candidate_session_service=CandidateSessionService(session_repo, exams),
        contract_service=ContractService(contract_repo, exams, session_repo)))
    lecturer = bearer("examiner-token")
    eid = client.post("/examiner/examinations", json={"title": "Python Final"}, headers=lecturer).json()["examination_id"]
    qid = client.post("/examiner/questions", json={"title": "Loops", "prompt": "Write a loop",
                      "language": "python", "max_score": 10}, headers=lecturer).json()["question_id"]
    client.post(f"/examiner/examinations/{eid}/questions", json={"question_id": qid, "display_order": 1, "score_weight": 10}, headers=lecturer)
    client.post(f"/examiner/examinations/{eid}/assignments", json={"candidate_user_id": "student-1"}, headers=lecturer)
    return client, eid


def test_contract_lifecycle_through_api():
    client, eid = client_with_exam()
    lecturer, student = bearer("examiner-token"), bearer("student-token")

    refused = client.post(f"/examiner/examinations/{eid}/transition", json={"target_status": "SCHEDULED"}, headers=lecturer)
    assert refused.status_code == 409 and "contract" in refused.json()["detail"]

    draft = client.put(f"/examiner/examinations/{eid}/contract", json={"capabilities": LAB_CAPABILITIES}, headers=lecturer)
    assert draft.status_code == 200
    body = draft.json()
    assert (body["status"], body["integrity_mode"], body["enforcement"]) == ("DRAFT", "LAB_CONTROLLED", "DECLARED_NOT_ENFORCED")
    assert body["policy_version"] is None
    assert client.get(f"/candidate/examinations/{eid}/contract", headers=student).status_code == 409

    assert client.post(f"/examiner/examinations/{eid}/transition", json={"target_status": "SCHEDULED"}, headers=lecturer).status_code == 200
    published = client.get(f"/candidate/examinations/{eid}/contract", headers=student).json()
    assert published["status"] == "BOUND" and published["policy_version"].startswith(f"ecc:{eid}@v1#")
    assert published["content_hash"] == body["content_hash"]

    exc = client.post(f"/examiner/examinations/{eid}/contract/exceptions",
                      json={"candidate_user_id": "student-1", "reason_category": "ACCESSIBILITY",
                            "extra_time_minutes": 25}, headers=lecturer)
    assert exc.status_code == 201 and exc.json()["extra_time_applied_to_deadline"] is True
    mine = client.get(f"/candidate/examinations/{eid}/contract", headers=student).json()["my_exceptions"]
    assert [e["extra_time_minutes"] for e in mine] == [25]

    amended = client.post(f"/examiner/examinations/{eid}/contract/amendments",
                          json={"capabilities": {**LAB_CAPABILITIES, "internet": "ALLOW"},
                                "amendment_reason": "Docs mirror down"}, headers=lecturer)
    assert amended.status_code == 201 and amended.json()["version"] == 2
    versions = client.get(f"/examiner/examinations/{eid}/contract", headers=lecturer).json()
    assert [(v["version"], v["status"]) for v in versions] == [(1, "SUPERSEDED"), (2, "BOUND")]


def test_validation_and_isolation():
    client, eid = client_with_exam()
    lecturer = bearer("examiner-token")
    bad = dict(LAB_CAPABILITIES); bad.pop("clipboard")
    assert client.put(f"/examiner/examinations/{eid}/contract", json={"capabilities": bad}, headers=lecturer).status_code == 422
    remote = client.put(f"/examiner/examinations/{eid}/contract",
                        json={"capabilities": LAB_CAPABILITIES, "integrity_mode": "REMOTE_PROCTORED"}, headers=lecturer)
    assert remote.status_code == 422
    assert client.get(f"/candidate/examinations/{eid}/contract", headers=bearer("student2-token")).status_code == 404
    assert client.put(f"/examiner/examinations/{eid}/contract", json={"capabilities": LAB_CAPABILITIES},
                      headers=bearer("student-token")).status_code == 403
    client.put(f"/examiner/examinations/{eid}/contract", json={"capabilities": LAB_CAPABILITIES}, headers=lecturer)
    no_reason = client.post(f"/examiner/examinations/{eid}/contract/amendments",
                            json={"capabilities": LAB_CAPABILITIES}, headers=lecturer)
    assert no_reason.status_code == 409  # exam still DRAFT: amend is for scheduled exams
