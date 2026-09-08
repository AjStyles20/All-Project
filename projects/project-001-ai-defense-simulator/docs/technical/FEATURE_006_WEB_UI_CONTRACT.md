# Feature 006 Contract — First Usable Secure Web Interface

## Status
APPROVED FOR BOUNDED EXECUTION

## Purpose
Wrap the verified provider-neutral backend in a usable, accessible, server-rendered web interface without weakening existing security/provenance boundaries or pretending unconfigured AI capabilities are live.

## Platform / Stack
- Primary language: Python
- Backend: FastAPI
- Templates: Jinja2
- Frontend: semantic HTML + CSS + minimal/no JavaScript for this slice
- Persistence: existing SQLite
- Delivery platform: web application
- React: not required

## Required Pages / Flows
1. Home page with application status and workspace creation.
2. Workspace page with:
   - document upload;
   - lexical/hybrid evidence search;
   - visible document/source provenance;
   - question-generation form only when a provider is configured, otherwise a clear unavailable state;
   - recent generated questions/history.
3. Question detail page with:
   - question text;
   - reviewer role/topic;
   - evidence provenance;
   - answer form only when an evaluator is configured, otherwise a clear unavailable state;
   - recent qualitative evaluations/feedback.
4. Server-side form handlers redirect after successful state-changing actions.

## Security Requirements
- Jinja autoescaping remains enabled; never mark uploaded/model text as safe HTML.
- No user/model content is inserted through unsafe DOM APIs.
- Add restrictive security response headers, including CSP, anti-framing, no-sniff, and referrer policy.
- Unsafe browser-origin requests with an explicit foreign `Origin` must be rejected.
- API/CLI clients without an `Origin` header remain supported for the current local prototype.
- No wildcard authenticated CORS configuration.
- No real secrets in templates, HTML, JavaScript, logs, or repository.
- No public-deployment claim; authentication and full CSRF/session controls remain required before multi-user deployment.
- Internal filesystem paths must never be rendered.
- AI capability status must reflect actual provider configuration.
- Evidence provenance must remain visible when search/questions/evaluations are rendered.

## Accessibility Requirements
- Semantic headings/landmarks.
- Explicit form labels.
- Keyboard-operable native controls.
- Statuses are communicated with text, not color alone.
- Reasonable focus order.
- Evidence/source details readable without hover.
- No mandatory audio/visual interaction.

## Error Handling
- User-facing validation messages must be controlled and must not expose stack traces.
- Missing workspace/question returns a controlled not-found page/response.
- Provider-unavailable flows show `not configured` rather than fabricated outputs.

## Out of Scope
- React SPA migration.
- authentication/multi-user authorization.
- full CSRF token/session infrastructure.
- public internet deployment.
- speech input/output.
- live webcam/video.
- avatars/VR.
- visual document understanding.
- administrative dashboards.

## Verification Requirements
- home page renders successfully;
- security headers present;
- cross-origin unsafe form request rejected;
- create-workspace UI flow works;
- document upload through UI works;
- search through UI displays provenance;
- uploaded HTML/script-like text is escaped in rendered output;
- AI forms correctly disable/show unavailable state without providers;
- test-only provider path can complete question -> answer -> feedback through server-rendered forms;
- cross-workspace UI access cannot expose another workspace question/evaluation;
- previous Feature 001–005 suite remains passing;
- dependency audit remains passing at verification time.

## Completion Boundary
Feature 006 is considered implemented when the server-rendered web flows above exist and pass functional/security tests. It is not a public-production UI until authentication, deployment hardening, full CSRF/session controls, user-device verification, and deployment-specific security review are complete.
