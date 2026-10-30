from fastapi.testclient import TestClient

from app.api.mysql_platform_api import create_mysql_platform_app
from app.domain.identity import AuthenticatedPrincipal, Role
from app.services.candidate_session_service import CandidateSessionService
from app.services.examination_service import ExaminationService
from app.services.review_service import ReviewService
from tests.candidate_session_fakes import InMemoryCandidateSessionRepository
from tests.examination_fakes import InMemoryExaminationRepository
from tests.review_fakes import InMemoryReviewRepository


class FakeAuth:
    TOKENS = {
        "examiner-token": AuthenticatedPrincipal("lecturer-1", "lecturer", frozenset({Role.EXAMINER})),
        "other-examiner-token": AuthenticatedPrincipal("lecturer-2", "lecturer2", frozenset({Role.EXAMINER})),
        "student-token": AuthenticatedPrincipal("student-1", "student", frozenset({Role.CANDIDATE})),
    }
    def authenticate(self, token): return self.TOKENS.get(token)
    def logout(self, token): return token in self.TOKENS


def bearer(token): return {"Authorization": "Bearer " + token}


def submitted_session_client():
    exams = InMemoryExaminationRepository()
    session_repo = InMemoryCandidateSessionRepository({"student-1"})
    exams.on_close.append(session_repo.finalize_open_sessions)
    client = TestClient(create_mysql_platform_app(
        auth_service=FakeAuth(), examination_service=ExaminationService(exams),
        candidate_session_service=CandidateSessionService(session_repo, exams),
        review_service=ReviewService(InMemoryReviewRepository(session_repo, exams), session_repo, exams)))
    lecturer, student = bearer("examiner-token"), bearer("student-token")
    eid = client.post("/examiner/examinations", json={"title": "Python Final"}, headers=lecturer).json()["examination_id"]
    qid = client.post("/examiner/questions", json={"title": "Loops", "prompt": "Write a loop",
                      "language": "python", "max_score": 10}, headers=lecturer).json()["question_id"]
    client.post(f"/examiner/examinations/{eid}/questions", json={"question_id": qid, "display_order": 1, "score_weight": 10}, headers=lecturer)
    client.post(f"/examiner/examinations/{eid}/assignments", json={"candidate_user_id": "student-1"}, headers=lecturer)
    for target in ("SCHEDULED", "ACTIVE"):
        client.post(f"/examiner/examinations/{eid}/transition", json={"target_status": target}, headers=lecturer)
    sid = client.post(f"/candidate/examinations/{eid}/session", headers=student).json()["session_id"]
    client.put(f"/candidate/sessions/{sid}/responses/{qid}", json={"content": "print(1)"}, headers=student)
    return client, eid, qid, sid


def test_examiner_reviews_and_marks_after_submission():
    client, eid, qid, sid = submitted_session_client()
    lecturer = bearer("examiner-token")
    assert client.put(f"/examiner/sessions/{sid}/marks/{qid}", json={"score": 5}, headers=lecturer).status_code == 409
    client.post(f"/candidate/sessions/{sid}/submit", headers=bearer("student-token"))

    listed = client.get(f"/examiner/examinations/{eid}/sessions", headers=lecturer).json()
    assert [(s["session_id"], s["status"], s["submission_mode"], s["marked_questions"]) for s in listed] == [(sid, "SUBMITTED", "CANDIDATE", 0)]

    marked = client.put(f"/examiner/sessions/{sid}/marks/{qid}", json={"score": 8, "comment": "Good."}, headers=lecturer)
    assert marked.status_code == 200 and marked.json()["response_revision"] == 1

    review = client.get(f"/examiner/sessions/{sid}", headers=lecturer).json()
    question = review["questions"][0]
    assert question["max_score"] == 10 and question["response"]["content"] == "print(1)"
    assert question["mark"]["score"] == 8 and question["mark"]["marked_by_user_id"] == "lecturer-1"
    totals = client.get(f"/examiner/examinations/{eid}/sessions", headers=lecturer).json()[0]
    assert (totals["raw_score"], totals["raw_max"]) == (8, 10)


def test_marks_validate_and_stay_with_owner():
    client, _, qid, sid = submitted_session_client()
    client.post(f"/candidate/sessions/{sid}/submit", headers=bearer("student-token"))
    lecturer = bearer("examiner-token")
    assert client.put(f"/examiner/sessions/{sid}/marks/{qid}", json={"score": 11}, headers=lecturer).status_code == 422
    assert client.put(f"/examiner/sessions/{sid}/marks/{qid}", json={"score": -1}, headers=lecturer).status_code == 422
    assert client.get(f"/examiner/sessions/{sid}", headers=bearer("other-examiner-token")).status_code == 403
    assert client.get(f"/examiner/sessions/{sid}", headers=bearer("student-token")).status_code == 403
    assert client.get("/examiner/sessions/missing", headers=lecturer).status_code == 404


def test_auto_submitted_session_is_markable_after_close_and_frozen_after_archive():
    client, eid, qid, sid = submitted_session_client()
    lecturer = bearer("examiner-token")
    client.post(f"/examiner/examinations/{eid}/transition", json={"target_status": "CLOSED"}, headers=lecturer)
    review = client.get(f"/examiner/sessions/{sid}", headers=lecturer).json()
    assert review["submission_mode"] == "AUTO_ON_CLOSE"
    assert client.put(f"/examiner/sessions/{sid}/marks/{qid}", json={"score": 4}, headers=lecturer).status_code == 200
    client.post(f"/examiner/examinations/{eid}/transition", json={"target_status": "ARCHIVED"}, headers=lecturer)
    assert client.put(f"/examiner/sessions/{sid}/marks/{qid}", json={"score": 6}, headers=lecturer).status_code == 409


def test_release_flow_and_candidate_result():
    client, eid, qid, sid = submitted_session_client()
    lecturer, student = bearer("examiner-token"), bearer("student-token")
    assert client.get(f"/candidate/sessions/{sid}/result", headers=student).status_code == 409
    client.post(f"/examiner/examinations/{eid}/transition", json={"target_status": "CLOSED"}, headers=lecturer)
    assert client.post(f"/examiner/examinations/{eid}/release", headers=lecturer).status_code == 409  # unmarked
    client.put(f"/examiner/sessions/{sid}/marks/{qid}", json={"score": 6, "comment": "first"}, headers=lecturer)
    client.put(f"/examiner/sessions/{sid}/marks/{qid}", json={"score": 7, "comment": "Solid loop."}, headers=lecturer)
    history = client.get(f"/examiner/sessions/{sid}", headers=lecturer).json()["questions"][0]["mark_history"]
    assert [h["score"] for h in history] == [6, 7]

    released = client.post(f"/examiner/examinations/{eid}/release", headers=lecturer)
    assert released.status_code == 200 and released.json()["released_by_user_id"] == "lecturer-1"
    assert client.put(f"/examiner/sessions/{sid}/marks/{qid}", json={"score": 9}, headers=lecturer).status_code == 409

    result = client.get(f"/candidate/sessions/{sid}/result", headers=student).json()
    assert (result["raw_score"], result["raw_max"], result["weighted_percent"]) == (7, 10, 70.0)
    assert result["questions"][0]["comment"] == "Solid loop." and "marked_by_user_id" not in result["questions"][0]
    totals = client.get(f"/examiner/examinations/{eid}/sessions", headers=lecturer).json()[0]
    assert totals["weighted_percent"] == 70.0
