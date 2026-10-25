# Original vision: what this project was meant to be

Sources read on 2026-10-25: the project package in Google Drive (the 2026-10-23 portfolio package folder `02_cultural-typographic-ai-evaluation`, `PROJECT_INDEX.json`, `chat_exports/PROJECT_02.txt`, `REQUIREMENTS_FROM_HISTORY.md`, `SELECTED_SOURCE_EXCERPTS.md`). Paraphrased; private media and full conversations were not used.

## The original direction
- **Typography systems with history and poetics.** Trace how modern type and layout systems, Apple's included, grew out of historical references, and what changed and why: "not only the numbers but also the poetic, conceptual thoughts".
- **Grids that actually add up.** The core design question: what relation between margins and gutters still arrives at a modular, flexible, square, rhythmic grid? Suggestions need a how-to, not just theory. A generated InDesign template got this wrong: missing parent pages, no text frames, and an inside margin of 37.89 pt where every other margin was 36 pt.
- **Persian glyphs done right or not at all.** A generated typewriter with Persian letters on its keys repeated some letters many times and got others wrong. Preserve Persian glyphs and orthography exactly.
- **Identity vs setting.** Keep a reference person's identity and attributes separate from setting and style.
- **Objects need a reason.** Literary and cultural references must have a reason to appear, not work as decorative name-dropping.
- **Measured, not assumed.** Distinguish measured layout from assumed conventions (no default 4/8 pt grid). Reject busy output that defeats the brief. Preserve explicit constraints and document failed iterations.

## The ambitious parts that were cut (and where they stand)
| Ambition | Status now |
|---|---|
| Grid relation check (margins, gutters, square module, baseline rhythm) | Checker implemented as `grid` (2026-10-25); solver/suggester not yet built. |
| Persian keyboard/typewriter fidelity | Keycap checker implemented as `keyboard` (2026-10-25); benchmark cases planned. |
| Glyph, ZWNJ, reading-order exactness | Implemented (`checks.py`). |
| Typography-history layer | Not started. |
| Reference-justified objects | Human-review axis only. |
| Identity preservation on portraits | Not started; needs consent-cleared material chosen by the owner. |
| Real rater study with disagreement | Schemas and aggregation built; no real annotations. |

## What must stay true
No cultural expertise inferred from identity. No OCR or screenshot transcription. Synthetic examples are labelled synthetic; no gold labels claimed.
