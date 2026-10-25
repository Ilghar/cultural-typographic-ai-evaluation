# ADR 0001 — Scope and boundaries
Status: accepted (internal self-review, 2026-10-23); independent review pending.

## Decision
- Two independent axes: factual constraints (pass/fail/uncertain + evidence) and aesthetic ratings (ordinal + rationale). They are never merged into one score.
- Cultural/reference claims require a cited source; rater identity is never evidence and identity fields are schema-forbidden.
- Minority annotations and uncertainty are preserved; adjudication adds a record, it does not overwrite.
- Phase 1 evaluates native text/metadata artifacts only; no images, no model calls.
- Synthetic cases carry `gold_verdict: null` until adjudicated.

## Consequences
No benchmark or model-quality claim is possible until reviewed annotations by multiple raters exist.
