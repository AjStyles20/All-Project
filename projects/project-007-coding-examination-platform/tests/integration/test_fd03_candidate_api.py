from fastapi.testclient import TestClient

from app.api.mysql_platform_api import create_mysql_platform_app
from app.domain.identity import AuthenticatedPrincipal, Role
from app.services.candidate_session_service import CandidateSessionService
from app.services.examination_service import ExaminationService
from tests.candidate_session_fakes import InMemoryCandidateSessionRepository
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


def active_exam_client():
    exams = InMemoryExaminationRepository()
    sessions = CandidateSessionService(InMemoryCandidateSessionRepository({"student-1", "student-2"}), exams)
    client = TestClient(create_mysql_platform_app(
        auth_service=FakeAuth(), examination_service=ExaminationService(exams),
        candidate_session_service=sessions))
    lecturer = bearer("examiner-token")
    eid = client.post("/examiner/examinations", json={"title": "Python Final"}, headers=lecturer).json()["examination_id"]
    qid = client.post("/examiner/questions", json={"title": "Loops", "prompt": "Write a loop",
                      "language": "python", "max_score": 10}, headers=lecturer).json()["question_id"]
    client.post(f"/examiner/examinations/{eid}/questions", json={"question_id": qid, "display_order": 1, "score_weight": 10}, headers=lecturer)
    assert client.post(f"/examiner/examinations/{eid}/assignments", json={"candidate_user_id": "student-1"}, headers=lecturer).status_code == 201
    for target in ("SCHEDULED", "ACTIVE"):
        client.post(f"/examiner/examinations/{eid}/transition", json={"target_status": target}, headers=lecturer)
    return client, eid, qid


def test_candidate_full_flow_start_save_submit():
    client, eid, qid = active_exam_client()
    student = bearer("student-token")
    listed = client.get("/candidate/examinations", headers=student).json()
    assert [(e["examination_id"], e["status"]) for e in listed] == [(eid, "ACTIVE")]

    session = client.post(f"/candidate/examinations/{eid}/session", headers=student).json()
    assert session["status"] == "IN_PROGRESS"
    sid = session["session_id"]
    assert client.post(f"/candidate/examinations/{eid}/session", headers=student).json()["session_id"] == sid

    view = client.get(f"/candidate/sessions/{sid}", headers=student).json()
    assert [q["question_id"] for q in view["questions"]] == [qid]
    assert "max_score" not in view["questions"][0] and view["questions"][0]["response"] is None

    saved = client.put(f"/candidate/sessions/{sid}/responses/{qid}", json={"content": "for i in range(5): print(i)"}, headers=student)
    assert saved.status_code == 200 and saved.json()["revision"] == 1
    stale = client.put(f"/candidate/sessions/{sid}/responses/{qid}", json={"content": "old tab", "base_revision": 0}, headers=student)
    assert stale.status_code == 409

    submitted = client.post(f"/candidate/sessions/{sid}/submit", headers=student)
    assert submitted.status_code == 200 and submitted.json()["status"] == "SUBMITTED"
    assert client.post(f"/candidate/sessions/{sid}/submit", headers=student).status_code == 200
    assert client.put(f"/candidate/sessions/{sid}/responses/{qid}", json={"content": "late"}, headers=student).status_code == 409
    final = client.get(f"/candidate/sessions/{sid}", headers=student).json()
    assert final["questions"][0]["response"]["content"] == "for i in range(5): print(i)"


def test_unassigned_candidate_and_foreign_session_are_not_found():
    client, eid, qid = active_exam_client()
    other = bearer("student2-token")
    assert client.post(f"/candidate/examinations/{eid}/session", headers=other).status_code == 404
    sid = client.post(f"/candidate/examinations/{eid}/session", headers=bearer("student-token")).json()["session_id"]
    assert client.get(f"/candidate/sessions/{sid}", headers=other).status_code == 404
    assert client.put(f"/candidate/sessions/{sid}/responses/{qid}", json={"content": "x"}, headers=other).status_code == 404


def test_role_boundaries():
    client, eid, _ = active_exam_client()
    assert client.post(f"/candidate/examinations/{eid}/session", headers=bearer("examiner-token")).status_code == 403
    assert client.post(f"/examiner/examinations/{eid}/assignments", json={"candidate_user_id": "student-2"}, headers=bearer("student-token")).status_code == 403


def test_examiner_assignment_errors_and_listing():
    client, eid, _ = active_exam_client()
    lecturer = bearer("examiner-token")
    assert client.post(f"/examiner/examinations/{eid}/assignments", json={"candidate_user_id": "student-1"}, headers=lecturer).status_code == 409
    assert client.post(f"/examiner/examinations/{eid}/assignments", json={"candidate_user_id": "nobody"}, headers=lecturer).status_code == 404
    listed = client.get(f"/examiner/examinations/{eid}/assignments", headers=lecturer).json()
    assert [a["candidate_user_id"] for a in listed] == ["student-1"]


def test_oversized_response_is_rejected_by_validation():
    client, eid, qid = active_exam_client()
    student = bearer("student-token")
    sid = client.post(f"/candidate/examinations/{eid}/session", headers=student).json()["session_id"]
    response = client.put(f"/candidate/sessions/{sid}/responses/{qid}", json={"content": "x" * 100_001}, headers=student)
    assert response.status_code == 422


def test_session_cannot_start_before_activation():
    exams = InMemoryExaminationRepository()
    sessions = CandidateSessionService(InMemoryCandidateSessionRepository({"student-1"}), exams)
    client = TestClient(create_mysql_platform_app(auth_service=FakeAuth(),
        examination_service=ExaminationService(exams), candidate_session_service=sessions))
    eid = client.post("/examiner/examinations", json={"title": "Draft"}, headers=bearer("examiner-token")).json()["examination_id"]
    client.post(f"/examiner/examinations/{eid}/assignments", json={"candidate_user_id": "student-1"}, headers=bearer("examiner-token"))
    assert client.post(f"/candidate/examinations/{eid}/session", headers=bearer("student-token")).status_code == 409
