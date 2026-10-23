# M07 failure analysis (Bot-authored, not independently reviewed)

Reproduce: `PYTHONPATH=src python3 -m cultural_typographic_ai_evaluation failure --out out/m07` (receipt `tests/receipts/m07_failure.json`).
The suite (`src/cultural_typographic_ai_evaluation/failure.py`) has 28 rows: 20 adversarial/malformed check inputs and 8 aggregation/disagreement cases.

| Code version | Passed |
|---|---|
| M06 (commit 219be17) | 11/28 (pre-fix run recorded in `tests/receipts/m07_prefix_run.json`) |
| M07 | 28/28 |

## Defects found and fixed (14)
- **Crashes on malformed artifacts (5):** `glyph_exact` on int/list, `required_fields` on non-object, `diagram_fidelity` on non-string, `aggregate` with missing or non-list `constraint_results`. Each now returns `fail` or rejects the annotation, with evidence.
- **False passes (4):** required field containing only ZWSP/ZWNJ, only bidi controls, or `None` (stringified to "None"). Presence now requires a char outside Unicode Z*/C*.
- **Missed numeric claims (2):** Persian digits with Arabic percent sign `۵۰٪`, and "50 percent". The regex now covers Unicode digits, `%`, `٪` (U+066A), `percent` and `درصد`.
- **Annotation-integrity gaps (3):** `rating: True` accepted (bool is int), identity field bypass by case (`Rater_Nationality`), duplicate rater on one case counted twice. All are now rejected.

## Disagreement handling (new, 3 rows)
`disagreement` (pass vs fail) is kept; new `needs_adjudication` is true whenever more than one substantive verdict (ignoring `not_applicable`) is present, e.g. pass vs uncertain. Nothing is auto-resolved; no majority vote is applied.

## Verified unchanged
The M06 corruption-suite baseline (`tests/receipts/m06_baseline.json`) is byte-identical after the fixes.

## Limits
The adversarial rows were written by the same author as the checks, so this is a robustness check, not evidence that the checks cover what real evaluators would hit. NFC vs NFD (`آ` vs `ا`+U+0653) is a deliberate `fail` under the exact-codepoint policy; whether to normalize first is a reviewer decision.
