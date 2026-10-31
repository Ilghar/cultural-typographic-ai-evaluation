# Source and access register (M01)

Machine-readable: `inputs/source_register.jsonl`.

## Existing evidence
| ID | What | Status |
|---|---|---|
| S01 | 6 newly drafted synthetic case specifications (C01–C06) | In repo. **Unreviewed, no gold verdicts**, not model outputs. |
| S02 | Paraphrased historical requirements from ilghar.studio design critiques | Summarized below; source file not copied. |
| S03 | Four private user excerpts (grid margins/gutters, InDesign parent pages and inside margins, wrong Persian glyphs on a generated typewriter) | **Not copied** (private). Used only to derive requirement categories. |
| S04 | Locators (conversation/message IDs + sha256) for 6 user messages | Not copied; no share URLs exist. |

Requirement categories derived from S02/S03 (paraphrase, not quotes):
1. Glyph/orthography correctness of Persian text is a **factual** constraint.
2. Reference identity/attributes are separate from setting/style.
3. Objects and cultural references need a documented reason, not decoration.
4. Measured layout values (margins, gutters, grid) must be distinguished from assumed conventions.
5. Explicit user constraints are preserved; failed iterations are documented.

These are historical design requirements, **not** a benchmark, gold dataset or universal cultural standard. No measured model improvement exists.

## Access actually used (2026-10-23, Europe/Berlin)
Drive project-02 folder read via connector (all files except `.DS_Store`; `source_register.jsonl` was empty). GitHub `Ilghar` verified; repo private. The project library could not be searched, so the SEARCH_GUIDE terms were not searched; no source came from it.

## Plans
Everything in `docs/PRODUCT_CONTRACT.md` acceptance criteria and `docs/ARCHITECTURE.md` is planned until code + receipts exist.
