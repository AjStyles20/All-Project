# Feature 011 Test Matrix

| Area | Expected result |
| --- | --- |
| Start session | Redirects to first authoritative turn |
| Turn progress | Shows current turn / max turns |
| Session membership | Workspace + session + question association required |
| Cross-workspace tampering | Rejected |
| Answer | Feedback recorded inside owning rehearsal flow |
| Follow-up | Redirects directly to new turn |
| Final turn | Answer marks session complete |
| Completed session | Further follow-up rejected |
| Completion reconciliation | Idempotent |
| Existing Features 001–010 | Regression suite remains passing |
| Dependencies | Audit reports no known vulnerabilities at verification time |
