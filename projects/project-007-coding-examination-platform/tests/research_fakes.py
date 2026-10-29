"""In-memory stand-in for MySQLResearchRepository used by FD-06 tests.

The research store side is NOT faked: tests use the real SQLite ResearchCaseStore
on a temporary file. This fake mirrors the MySQL guards: one link per exam question,
append-only consent with latest-wins, unique research codes, and one bridge record
per (session, question).
"""
from app.domain.examination import ExaminationConflictError


class InMemoryResearchRepository:
    def __init__(self, session_repository=None):
        # Needed to resolve which bridge records belong to a candidate (the SQL joins).
        self.sessions = session_repository
        self.withdrawal_log = []
        self.links = []
        self.consent_events = []
        self.identities = {}
        self.records = {}

    def create_link(self, link):
        link.validate()
        if any(l.examination_id == link.examination_id and l.question_id == link.question_id for l in self.links):
            raise ExaminationConflictError("That examination question already has a research link.")
        self.links.append(link)

    def list_links(self, examination_id):
        return [l for l in self.links if l.examination_id == examination_id]

    def record_consent(self, examination_id, candidate_user_id, status, at):
        self.consent_events.append((examination_id, candidate_user_id, status, at))

    def current_consent(self, examination_id, candidate_user_id):
        matching = [e for e in self.consent_events if e[0] == examination_id and e[1] == candidate_user_id]
        return matching[-1][2] if matching else None

    def get_research_code(self, examination_id, candidate_user_id):
        return self.identities.get((examination_id, candidate_user_id))

    def create_research_code(self, examination_id, candidate_user_id, code, at):
        if (examination_id, candidate_user_id) in self.identities:
            return False
        self.identities[(examination_id, candidate_user_id)] = code
        return True

    def list_identities(self, examination_id):
        return sorted(((uid, code) for (eid, uid), code in self.identities.items() if eid == examination_id),
                      key=lambda pair: pair[1])

    def get_bridge_record(self, session_id, question_id):
        return self.records.get((session_id, question_id))

    def save_bridge_record(self, record):
        key = (record.session_id, record.question_id)
        if key in self.records:
            return False
        self.records[key] = record
        return True

    def list_bridge_records(self, examination_id):
        link_ids = {l.link_id for l in self.list_links(examination_id)}
        return [r for r in self.records.values() if r.link_id in link_ids]

    def _candidate_of(self, session_id):
        session = self.sessions.sessions[session_id]
        return self.sessions.assignments[session.assignment_id]

    def bridged_case_ids(self, examination_id, candidate_user_id):
        return sorted(r.research_case_id for r in self.records.values()
                      if r.outcome.value == "BRIDGED"
                      and self._candidate_of(r.session_id).examination_id == examination_id
                      and self._candidate_of(r.session_id).candidate_user_id == candidate_user_id)

    def complete_withdrawal(self, examination_id, candidate_user_id, research_code, deleted, retained, at):
        self.records = {k: r for k, r in self.records.items()
                        if not (self._candidate_of(r.session_id).examination_id == examination_id
                                and self._candidate_of(r.session_id).candidate_user_id == candidate_user_id)}
        self.identities.pop((examination_id, candidate_user_id), None)
        if research_code is not None:
            self.withdrawal_log.append({"research_code": research_code, "cases_deleted": deleted,
                                        "cases_retained_as_shell": retained, "completed_at": at})

    def list_withdrawal_log(self, examination_id):
        return list(self.withdrawal_log)
