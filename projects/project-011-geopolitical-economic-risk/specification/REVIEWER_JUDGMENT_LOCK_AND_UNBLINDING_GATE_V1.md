# P003 — Reviewer Judgment Lock and Unblinding Gate v1

## Rule
Independent reviewer judgments must be locked **before** baseline identity is restored or comparative metrics are calculated.

## Lock
For each reviewer, store the complete blinded review batch and calculate a deterministic SHA-256 digest over:
- batch ID;
- reviewer ID;
- blind claim IDs;
- judgment labels;
- rationales.

The digest is an integrity reference. Changing a judgment or rationale after locking changes the digest.

## Unblinding gate
Unblinding is permitted only when:
1. the expected reviewer batches are complete;
2. each batch verifies against its lock digest;
3. reviewers have not been shown the B2/B3 mapping or aggregate results;
4. the private blind-ID mapping is preserved;
5. any missing review is documented rather than silently dropped.

## After unblinding
Join blind IDs to baseline/run identities, then compute the already predeclared metrics. Preserve the locked pre-unblinding batches alongside the unblinded analysis.

## Boundary
A cryptographic lock is an integrity mechanism, not proof that a reviewer is independent or qualified. Actual reviewer recruitment, identity/qualification documentation and judgments remain external evidence.
