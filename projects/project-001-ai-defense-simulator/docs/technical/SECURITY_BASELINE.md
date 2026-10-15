# Project 001 Security Baseline

## Status
ACTIVE — applies to all current and future Project 001 engineering work.

## Security Objective
Project 001 must be secure by default and resistant to tampering, malicious input, unauthorized access, data leakage, denial-of-service abuse, unsafe file processing, dependency compromise, insecure configuration, and future AI/RAG prompt abuse.

Security is a release gate, not an optional hardening phase.

## Mandatory Engineering Controls

### 1. Input Validation
- Validate all untrusted input server-side.
- Prefer allowlists over blocklists.
- Enforce type, length, range, format, and semantic constraints.
- Reject malformed or unexpected content explicitly.
- Never rely on client-side validation as a security boundary.

### 2. File Upload Security
- Enforce strict file-size limits.
- Enforce an approved extension allowlist.
- Verify content structure using the parser rather than trusting filename or MIME type alone.
- Reject malformed, encrypted, or unsupported files safely.
- Never execute uploaded content.
- Do not derive executable filesystem paths from user-controlled filenames.
- Do not expose internal filesystem paths to clients.
- Treat parser libraries as attack-surface dependencies and keep them updated.
- Future OCR/archive support requires separate security review before implementation.

### 3. Database Security
- Use parameterized queries only.
- Do not concatenate untrusted input into SQL.
- Enforce workspace/resource scoping on every data operation.
- Preserve foreign-key and transaction integrity.
- Add authorization checks before multi-user access is introduced.

### 4. Authentication and Authorization
Current single-user/local prototype does not yet claim authentication.
Before remote or multi-user deployment:
- use a vetted authentication library/provider rather than custom cryptography;
- enforce authorization server-side on every protected resource;
- default deny when ownership or permission cannot be proven;
- prevent horizontal and vertical privilege escalation;
- use secure session cookies (`HttpOnly`, `Secure`, appropriate `SameSite`) when cookie sessions are used;
- require HTTPS outside trusted local development.

### 5. Secrets and Configuration
- No API keys, passwords, tokens, or connection secrets in source code.
- Use environment variables or an approved secret store.
- Never commit `.env` files containing real secrets.
- Avoid logging secrets or full sensitive payloads.
- Production configuration must disable debug behavior and verbose internal exception output.

### 6. API and Abuse Resistance
- Bound request sizes and computationally expensive operations.
- Add rate limiting before public deployment or costly AI endpoints.
- Validate pagination/limit parameters.
- Use timeouts for external services.
- Fail closed when a security-sensitive dependency or provider is unavailable.
- Avoid returning internal stack traces to clients.

### 7. Web Security
When browser UI is introduced:
- escape/encode untrusted output in the correct rendering context;
- avoid unsafe HTML insertion and unsafe DOM APIs;
- add CSRF protection for state-changing cookie-authenticated requests;
- use restrictive CORS rules rather than `*` for authenticated deployments;
- set appropriate security headers for deployed web environments;
- do not expose internal API/debug documentation publicly unless intentionally approved.

### 8. AI / RAG Security
Before LLM features are treated as production-capable:
- uploaded documents and retrieved chunks are untrusted data, not trusted instructions;
- separate system/developer policy from retrieved document text;
- do not allow retrieved content to redefine permissions, tool access, security policy, or system prompts;
- constrain tools/actions with explicit authorization and allowlists;
- preserve provenance for generated questions and feedback;
- defend against prompt injection, retrieval poisoning, data exfiltration requests, and indirect instruction attacks;
- never allow model output alone to authorize destructive or privileged actions;
- cap token/context sizes and provider spend.

### 9. Dependencies and Supply Chain
- Keep dependency versions bounded and reviewed.
- Run dependency vulnerability scanning before release/deployment.
- Remove unused dependencies.
- Do not install packages only because generated code references them; verify package identity and provenance first.
- Record security-relevant dependency changes in the project decisions/work log.

### 10. Logging and Error Handling
- Log meaningful security events without recording secrets.
- Distinguish validation failure, authorization failure, parser failure, environment failure, and internal application failure.
- Return controlled error messages to clients.
- Preserve enough evidence for debugging and incident review without leaking implementation internals.

## Security Verification Gate
A substantial feature cannot be marked VERIFIED solely because functional tests pass. Verification must assess applicable abuse cases, including:
- malformed and boundary inputs;
- unauthorized resource access;
- workspace/tenant isolation;
- injection attempts;
- path traversal attempts;
- malicious or malformed file uploads;
- oversized/resource-exhaustion requests;
- sensitive error leakage;
- dependency/configuration risks;
- security regressions introduced by the diff.

For AI features also test:
- direct prompt injection;
- indirect prompt injection from uploaded documents;
- retrieval poisoning;
- attempts to reveal system prompts, secrets, or data from other workspaces;
- attempts to make the model bypass authorization or perform unsupported actions.

## Current Security Status
### Already Present
- parameterized SQLite statements;
- workspace-scoped lexical retrieval;
- file-size limits;
- extension allowlist;
- parser-based extraction failures;
- explicit encrypted-PDF rejection;
- no configured external AI provider or committed AI secret;
- controlled HTTP errors for several upload/search failures.

### Still Required Before Public/Multi-User Deployment
- authentication;
- per-resource authorization/ownership model;
- rate limiting;
- CSRF protections where applicable;
- production CORS and security headers;
- HTTPS deployment configuration;
- dependency vulnerability scan;
- hardened logging/error policy;
- security tests for malicious file structures and resource exhaustion;
- AI/RAG prompt-injection defenses once those features exist.

## Security Claim Rule
Do not describe Project 001 as "secure", "hardened", "tamper-proof", or "production-ready" without a completed security review and deployment-specific evidence. Use precise statuses such as `security baseline implemented`, `security tests partial`, or `public-deployment hardening not yet verified`.
