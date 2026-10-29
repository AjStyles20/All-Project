from fastapi.testclient import TestClient

from app.api.mysql_platform_api import create_mysql_platform_app
from app.domain.examination import Examination, ExaminationStatus
from app.domain.identity import AuthenticatedPrincipal, Role
from app.services.examination_service import ExaminationService
from tests.examination_fakes import InMemoryExaminationRepository


class FakeAuth:
    TOKENS = {
        "examiner-token": AuthenticatedPrincipal("lecturer-1", "lecturer", frozenset({Role.EXAMINER})),
        "candidate-token": AuthenticatedPrincipal("student-1", "student", frozenset({Role.CANDIDATE})),
        "admin-token": AuthenticatedPrincipal("admin-1", "admin", frozenset({Role.ADMINISTRATOR})),
    }
    def authenticate(self, token): return self.TOKENS.get(token)
    def logout(self, token): return token in self.TOKENS


def client_and_repo():
    repo = InMemoryExaminationRepository()
    app = create_mysql_platform_app(auth_service=FakeAuth(), examination_service=ExaminationService(repo))
    return TestClient(app), repo


def bearer(token): return {"Authorization": "Bearer " + token}


def create_exam_with_question(client, headers):
    eid = client.post("/examiner/examinations", json={"title":"Python Final"}, headers=headers).json()["examination_id"]
    qid = client.post("/examiner/questions", json={"title":"Loops","prompt":"Write a loop","language":"python","max_score":10}, headers=headers).json()["question_id"]
    return eid, qid


def test_candidate_cannot_create_examination():
    client, _ = client_and_repo()
    response = client.post("/examiner/examinations", json={"title":"Python Final"}, headers=bearer("candidate-token"))
    assert response.status_code == 403


def test_candidate_cannot_read_examiner_content():
    client, _ = client_and_repo()
    assert client.get("/examiner/examinations", headers=bearer("candidate-token")).status_code == 403
    assert client.get("/examiner/questions", headers=bearer("candidate-token")).status_code == 403


def test_examiner_creates_exam_question_attaches_and_transitions():
    client, repo = client_and_repo()
    headers = bearer("examiner-token")
    exam = client.post("/examiner/examinations", json={"title":"Python Final"}, headers=headers)
    assert exam.status_code == 201
    eid = exam.json()["examination_id"]
    q = client.post("/examiner/questions", json={"title":"Loops","prompt":"Write a loop","language":"python","max_score":10}, headers=headers)
    assert q.status_code == 201
    qid = q.json()["question_id"]
    attached = client.post(f"/examiner/examinations/{eid}/questions", json={"question_id":qid,"display_order":1,"score_weight":10}, headers=headers)
    assert attached.status_code == 204
    assert repo.attachments == [(eid,qid,1,10)]
    transition = client.post(f"/examiner/examinations/{eid}/transition", json={"target_status":"SCHEDULED"}, headers=headers)
    assert transition.status_code == 200
    assert transition.json()["status"] == "SCHEDULED"


def test_non_owner_examiner_is_forbidden():
    client, repo = client_and_repo()
    repo.exams["foreign"] = Examination("foreign","Other Exam","","other-lecturer",ExaminationStatus.DRAFT)
    headers = bearer("examiner-token")
    assert client.post("/examiner/examinations/foreign/transition", json={"target_status":"SCHEDULED"}, headers=headers).status_code == 403
    assert client.get("/examiner/examinations/foreign", headers=headers).status_code == 403
    assert client.patch("/examiner/examinations/foreign", json={"title":"Hijack"}, headers=headers).status_code == 403


def test_illegal_transition_returns_conflict():
    client, _ = client_and_repo()
    headers = bearer("examiner-token")
    eid = client.post("/examiner/examinations", json={"title":"Python Final"}, headers=headers).json()["examination_id"]
    response = client.post(f"/examiner/examinations/{eid}/transition", json={"target_status":"ACTIVE"}, headers=headers)
    assert response.status_code == 409


def test_scheduling_empty_examination_returns_conflict():
    client, _ = client_and_repo()
    headers = bearer("examiner-token")
    eid = client.post("/examiner/examinations", json={"title":"Python Final"}, headers=headers).json()["examination_id"]
    response = client.post(f"/examiner/examinations/{eid}/transition", json={"target_status":"SCHEDULED"}, headers=headers)
    assert response.status_code == 409


def test_admin_passes_role_boundary_but_ownership_still_applies():
    client, repo = client_and_repo()
    response = client.post("/examiner/examinations", json={"title":"Admin-created Exam"}, headers=bearer("admin-token"))
    assert response.status_code == 201
    repo.exams["lecturer-exam"] = Examination("lecturer-exam","Lecturer Exam","","lecturer-1",ExaminationStatus.DRAFT)
    assert client.get("/examiner/examinations/lecturer-exam", headers=bearer("admin-token")).status_code == 403


def test_whitespace_title_is_rejected_not_server_error():
    client, _ = client_and_repo()
    response = client.post("/examiner/examinations", json={"title":"   "}, headers=bearer("examiner-token"))
    assert response.status_code == 422


def test_inverted_time_window_is_rejected():
    client, _ = client_and_repo()
    response = client.post("/examiner/examinations", json={"title":"Timed",
        "starts_at":"2026-11-02T10:00:00+00:00","ends_at":"2026-11-02T09:00:00+00:00"},
        headers=bearer("examiner-token"))
    assert response.status_code == 422


def test_aware_times_are_stored_as_naive_utc():
    client, repo = client_and_repo()
    response = client.post("/examiner/examinations", json={"title":"Timed",
        "starts_at":"2026-11-02T10:00:00+02:00","ends_at":"2026-11-02T12:00:00+02:00"},
        headers=bearer("examiner-token"))
    exam = repo.exams[response.json()["examination_id"]]
    assert exam.starts_at.tzinfo is None and exam.starts_at.hour == 8


def test_duplicate_attachment_returns_conflict():
    client, _ = client_and_repo()
    headers = bearer("examiner-token")
    eid, qid = create_exam_with_question(client, headers)
    body = {"question_id":qid,"display_order":1,"score_weight":10}
    assert client.post(f"/examiner/examinations/{eid}/questions", json=body, headers=headers).status_code == 204
    assert client.post(f"/examiner/examinations/{eid}/questions", json=body, headers=headers).status_code == 409


def test_attaching_unknown_question_returns_not_found():
    client, _ = client_and_repo()
    headers = bearer("examiner-token")
    eid, _ = create_exam_with_question(client, headers)
    response = client.post(f"/examiner/examinations/{eid}/questions", json={"question_id":"nope","display_order":1,"score_weight":1}, headers=headers)
    assert response.status_code == 404


def test_foreign_question_attach_returns_not_found():
    client, repo = client_and_repo()
    headers = bearer("examiner-token")
    eid, _ = create_exam_with_question(client, headers)
    from app.domain.examination import ProgrammingQuestion
    repo.create_question(ProgrammingQuestion("theirs","T","P","python",5), "other-lecturer")
    response = client.post(f"/examiner/examinations/{eid}/questions", json={"question_id":"theirs","display_order":1,"score_weight":5}, headers=headers)
    assert response.status_code == 404


def test_examiner_reads_lists_updates_and_detaches():
    client, _ = client_and_repo()
    headers = bearer("examiner-token")
    eid, qid = create_exam_with_question(client, headers)
    client.post(f"/examiner/examinations/{eid}/questions", json={"question_id":qid,"display_order":1,"score_weight":10}, headers=headers)

    listed = client.get("/examiner/examinations", headers=headers).json()
    assert [e["examination_id"] for e in listed] == [eid]
    assert [q["question_id"] for q in client.get("/examiner/questions", headers=headers).json()] == [qid]

    detail = client.get(f"/examiner/examinations/{eid}", headers=headers).json()
    assert detail["status"] == "DRAFT"
    assert [(q["question_id"], q["display_order"], q["score_weight"]) for q in detail["questions"]] == [(qid, 1, 10)]

    updated = client.patch(f"/examiner/examinations/{eid}", json={"title":"Python Final v2","description":"Paper A"}, headers=headers)
    assert updated.status_code == 200 and updated.json()["title"] == "Python Final v2"

    assert client.delete(f"/examiner/examinations/{eid}/questions/{qid}", headers=headers).status_code == 204
    assert client.get(f"/examiner/examinations/{eid}", headers=headers).json()["questions"] == []
    assert client.delete(f"/examiner/examinations/{eid}/questions/{qid}", headers=headers).status_code == 404


def test_scheduled_examination_is_locked_against_edits():
    client, _ = client_and_repo()
    headers = bearer("examiner-token")
    eid, qid = create_exam_with_question(client, headers)
    client.post(f"/examiner/examinations/{eid}/questions", json={"question_id":qid,"display_order":1,"score_weight":10}, headers=headers)
    client.post(f"/examiner/examinations/{eid}/transition", json={"target_status":"SCHEDULED"}, headers=headers)
    assert client.patch(f"/examiner/examinations/{eid}", json={"title":"Late edit"}, headers=headers).status_code == 409
    assert client.delete(f"/examiner/examinations/{eid}/questions/{qid}", headers=headers).status_code == 409


def test_unknown_examination_returns_not_found():
    client, _ = client_and_repo()
    assert client.get("/examiner/examinations/missing", headers=bearer("examiner-token")).status_code == 404
