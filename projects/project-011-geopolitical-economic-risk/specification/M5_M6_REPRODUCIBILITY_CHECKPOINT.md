# P003 M5/M6 — Falsification and Reproducibility Checkpoint

## M5 verification

GitHub Actions P003 ETEC Tests run #32 verified the deterministic F1-F8 contract suite and preceding implementation: **22 passed, 0 failed in 0.05s**.

M5 is closed for constructed software falsification contracts.

## M6 objective

M6 adds deterministic, inspectable persistence for later historical replay. A replay record freezes:
- schema version;
- economic case and information cutoff;
- evidence records and provenance fields;
- transition assessments;
- released/stopped progression decision;
- audit trace.

Canonical JSON serialization is SHA-256 hashed. The hash is an integrity/reproducibility mechanism, not proof that the evidence is true or authoritative.

## M6 boundaries

No database, live retrieval, historical case, or external data source is introduced yet. JSON is intentionally used first because it is transparent, low-overhead, diffable and appropriate for the user's low-spec development environment. SQLite can be added when query/persistence requirements justify it.
