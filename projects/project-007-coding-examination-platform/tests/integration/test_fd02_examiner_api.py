from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient

from app.api.mysql_platform_api import create_mysql_platform_app
from app.domain.examination import Examination
from app.domain.identity import AuthenticatedPrincipal, Role
from app.services.examination_service import ExaminationService


class FakeAuth:
    TOKENS = {
        "examiner-token": AuthenticatedPrincipal("lecturer-1", "lecturer", frozenset({Role.EXAMINER})),
        "candidate-token": AuthenticatedPrincipal("student-1", "student", frozenset({Role.CANDIDATE})),
        "admin-token": AuthenticatedPrincipal("admin-1", "admin", frozenset({Role.ADMINISTRATOR})),
    }
    def authenticate(self, token): return self.TOKENS.get(token)
    def logout(self, token): return token in self.TOKENS


class FakeExamRepository:
    def __init__(self):
        self.exams, self.questions, self.attachments = {}, {}, []
    def create_examination(self, e): self.exams[e.examination_id] = e
    def get_examination(self, eid): return self.exams.get(eid)
    def update_status(self, eid, status):
        e = self.exams.get(eid)
        if not e: return False
        self.exams[eid] = Examination(e.examination_id,e.title,e.description,e.owner_user_id,status,e.starts_at,e.ends_at)
        return True
    def create_question(self, q, creator): self.questions[q.question_id] = q
    def get_question(self, qid): return self.questions.get(qid)
    def attach_question(self,eid,qid,order,weight): self.attachments.append((eid,qid,order,weight))


def client_and_repo():
    repo = FakeExamRepository()
    app = create_mysql_platform_app(auth_service=FakeAuth(), examination_service=ExaminationService(repo))
    return TestClient(app), repo


def bearer(token): return {"Authorization": "Bearer " + token}


def test_candidate_cannot_create_examination():
    client, _ = client_and_repo()
    response = client.post("/examiner/examinations", json={"title":"Python Final"}, headers=bearer("candidate-token"))
    assert response.status_code == 403


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
    repo.exams["foreign"] = Examination("foreign","Other Exam","","other-lecturer",__import__("app.domain.examination",fromlist=["ExaminationStatus"]).ExaminationStatus.DRAFT)
    response = client.post("/examiner/examinations/foreign/transition", json={"target_status":"SCHEDULED"}, headers=bearer("examiner-token"))
    assert response.status_code == 403


def test_illegal_transition_returns_conflict():
    client, _ = client_and_repo()
    headers = bearer("examiner-token")
    eid = client.post("/examiner/examinations", json={"title":"Python Final"}, headers=headers).json()["examination_id"]
    response = client.post(f"/examiner/examinations/{eid}/transition", json={"target_status":"ACTIVE"}, headers=headers)
    assert response.status_code == 409


def test_admin_passes_role_boundary_but_ownership_still_applies():
    client, _ = client_and_repo()
    response = client.post("/examiner/examinations", json={"title":"Admin-created Exam"}, headers=bearer("admin-token"))
    assert response.status_code == 201
