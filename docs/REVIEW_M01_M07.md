# Review of M01–M07

**Type: AI self-review by a separate pass (Grok Bot, 2026-10-25). This is not a human or independent expert review.** The same agent that built M01–M07 wrote this review, so it cannot replace a human reviewer.

## Method
- Fresh copy of `main` rebuilt from the GitHub tree, with every listed blob SHA-1 matching the local tree. The tree listing was truncated at 20 kB, so a few `tools/` files were not compared.
- Full test suite rerun under `PYTHONHASHSEED` = 0, 1 and 12345 with `-W error`, on Python 3.13.5 and, via uv, CPython 3.11.17.
- Every README command rerun. Outputs compared with the committed receipts, and reruns compared with each other to check determinism.
- Every `schemas/*.json` checked with `unsupported_keywords`. Fixtures, inputs and outputs validated against their schemas.
- Grep for leaked emails, tokens, box paths and identifiers. Checked whether blind packets expose item IDs. License notes re-read.

## Common findings
| ID | Severity | Finding | Fix |
|---|---|---|---|
| R-01 | medium | `docs/CASE_PAGE.md` was hand-written and stale against the M06/M07 results. `site/project.json` evidence text was stale too. | `tools/export_site.py` now generates CASE_PAGE.md and index.html from project.json. `tests/test_site.py` fails if either drifts. |
| R-00 | info | README says "Python >= 3.11", which was previously unverified. | Verified: the suite passes on CPython 3.11.17 and 3.13.5. |
| — | ok | The README numbers reproduce exactly. Slice outputs are byte-identical across reruns. No leaked emails, tokens or IDs. Blind packets carry no item IDs. All schemas use only supported keywords. | — |

## Project-specific findings
| ID | Severity | Finding | Fix |
|---|---|---|---|
| R-02 | medium | Regression from M07: `validate_annotation` returned early whenever a forbidden identity field was present, which hid other errors such as an out-of-range rating. The M03 report no longer matched its receipt. | Now returns early only on structural errors. The M03 report matches its receipt again, apart from the `needs_adjudication` field added in M07. A regression test is in `tests/test_review.py`. |
| — | low (documented, not fixed) | `fixtures/synthetic_eval_m03.json` uses the pre-M04 minimal case format and does not validate against the current `case.schema.json`. | Kept unchanged so the M03 receipt stays reproducible. The schema applies to M04+ inputs only. |

## Not covered
No human listening, expert annotation or blind probe authoring took place. Milestone acceptance stays "Bot review only".
