# Cultural and typographic AI evaluation kit

**Status: work in progress (private). 7/10 milestones (Bot-reviewed); synthetic inputs.**

- Product contract: `docs/PRODUCT_CONTRACT.md`
- Sources/evidence vs plans: `docs/SOURCES.md`
- Architecture/experiment plan: `docs/ARCHITECTURE.md`, ADR `docs/adr/0001-scope-and-boundaries.md`
- Handoff: `handoff/`

Contribution: Ilghar — problem framing, requirements, evaluation direction. Implementation AI-assisted (Grok Bot). License: not yet chosen.

## Quickstart (fresh environment)
Requires Python >= 3.11, no dependencies, no network.
```
git clone <this repo> && cd cultural-typographic-ai-evaluation
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m cultural_typographic_ai_evaluation report fixtures/synthetic_eval_m03.json --out out/
```
Modules: checks.py, aggregate.py, cli.py. Fixture: 2 synthetic specs, mock artifacts and 3 mock annotations (one deliberately invalid); exercises ZWNJ/Arabic-kaf detection, identity-field rejection, minority retention. Receipts: `tests/receipts/`.

## Vertical slice (M04)
```
PYTHONPATH=src python3 -m cultural_typographic_ai_evaluation slice inputs/synthetic_cases.json --specs fixtures/card_specs_m04.json --out out/m04
```
Cleared C01-C06 -> C01/C02 deterministic RTL SVG cards (template, not AI) -> text extraction -> glyph/order/field checks + corrupted negative control -> blank annotation templates for all six. C03-C06 human-review only.
Review: `docs/REVIEW_M01_M03.md`.

## Collection and results
- Datasheet: `data/collection_v1/DATASHEET.md`
- Results: `docs/RESULTS.md`
- Case page: `docs/CASE_PAGE.md`; static page: `site/index.html` (`python3 tools/export_site.py`); diagram `docs/architecture.mmd` + `docs/architecture.svg`
- Schema validation in code: `src/cultural_typographic_ai_evaluation/schema.py` (stdlib subset)
- Failure analysis (M07): `docs/FAILURE_ANALYSIS.md`
- Illustration provenance: `assets/ASSETS.json` (image on Drive, not in git)
