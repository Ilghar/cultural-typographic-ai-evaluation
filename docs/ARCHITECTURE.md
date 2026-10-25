# Architecture and experiment plan (M02)

Diagram `docs/architecture.mmd`; ADR `docs/adr/0001-scope-and-boundaries.md`.

## Modules (`src/cultural_typographic_ai_evaluation/`, planned M03)
| Module | Responsibility |
|---|---|
| `schema.py` | stdlib validation of cases/annotations mirroring `schemas/*.json`; rejects identity-based fields |
| `checks.py` | Deterministic factual checks on **native text artifacts**: exact codepoint match (`glyph_exact`), bidi run order, required fields present/ordered, diagram nodes/edges vs stage list |
| `aggregate.py` | Keep constraint verdicts and aesthetic ratings separate; disagreement per constraint (any pass vs fail) and per axis (range, distribution) |
| `report.py` | JSON + Markdown report with denominators; `private` fields stripped from public export |
| `cli.py` | `python -m cultural_typographic_ai_evaluation report CASES ANNOTATIONS --out DIR` |
| `viewer/` (later) | Static HTML viewer, escaped text, RTL-safe |

## Data flow
Case spec → candidate artifact (text/metadata only in this phase) → automated factual checks + independent human annotations → aggregation (no averaging of facts with aesthetics) → adjudication record (minority kept) → versioned report.

## Failure cases to cover
missing rights/consent on external asset; glyph substitution (e.g. ك U+0643 vs ک U+06A9, ي U+064A vs ی U+06CC); dropped/added ZWNJ; reversed RTL/LTR order; missing required field; reference cited without justification; same rater pass+fail on one constraint (contradiction); aesthetic rating out of range; annotation carrying identity fields; private field leaking to export.

## Metrics
constraint pass/fail/uncertain counts with denominators per constraint type; aesthetic rating distribution per axis (no single beauty score); disagreement count with n raters; missing/uncertain counts. No cultural-bias population claims.

## Deterministic tests
stdlib `unittest`; fixtures are committed synthetic cases + hand-written synthetic annotations clearly labelled synthetic; canonical sorted JSON outputs; receipts under `tests/receipts/`.

## Dependencies
Python ≥3.11 stdlib (`unicodedata`). Viewer: plain HTML/CSS/JS, no build. No network/model calls.

## License / consent plan
Only original synthetic text now. Any image/media: requires source, license, consent and `private` flag before entering fixtures; portraits only if Ilghar selects them. No Outlier material ever. Repo license decided at M10.

## Review
Internal self-review 2026-10-23 against M02 + TEST_PLAN; independent review pending.

## Implementation status (after M04)
Built: `checks.py`, `aggregate.py`, `slice.py` (M04 template SVG renderer + extraction), `cli.py`. Planned not built: `schema.py`, `report.py` (Markdown), `viewer/`.
Schemas are documentation + test references; they are not machine-enforced (stdlib, no jsonschema).
