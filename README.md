# Cultural and typographic AI evaluation kit

**Status: work in progress (private). 3/10 milestones; minimal stdlib tool on synthetic/mock fixtures only — no measured model results.**

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
