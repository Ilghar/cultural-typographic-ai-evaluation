# Product contract (M01)

## User
A design/AI evaluator reviewing generated or edited visual-text artifacts (posters, cards, layouts, diagrams) that include Persian or mixed-direction typography and cultural references.

## Problem
Critiques mix two different things: **factual constraint failures** (wrong glyph, corrupted reading order, missing required field, unjustified reference, changed identity attribute) and **aesthetic judgment** (hierarchy, balance, resonance). Mixing them produces unfalsifiable "quality" scores and hides disagreement.

## Bounded scope
- Annotation schema with two separate axes: `constraints[]` (pass/fail/uncertain + evidence) and `aesthetic[]` (ordinal rating + rationale), never combined into one score.
- Every annotation records rater id (pseudonymous), uncertainty, source/rationale and — for cultural claims — a cited source, not the rater's identity.
- Offline Python validator + report: constraint pass/fail counts with denominators, aesthetic distributions, disagreement, missing/uncertain counts. Static viewer later.
- Start with neutral original/synthetic text cases (C01–C06 and new ones).

## Non-goals
- No completed benchmark, gold dataset or model-improvement claim.
- No confidential Outlier material, portraits or private media.
- Never infer cultural expertise or correctness from a rater's personal identity.
- No population-level cultural-bias claims from small convenience samples.
- No model calls.

## Acceptance criteria for the finished tool (planned)
1. Annotations missing source/consent/license metadata for external assets are rejected.
2. Factual constraint results and aesthetic ratings are stored and reported separately.
3. Minority annotations and uncertainty are preserved (no majority overwrite).
4. Malformed annotations and contradictory verdicts by the same rater are detected.
5. Persian/RTL/mixed text, including ZWNJ (U+200C), round-trips byte-identically through load → report.
6. Public exports exclude private references (fields marked `private`).
7. Offline; receipts under `tests/receipts/`.

## Data rights and gaps
Only newly authored synthetic text enters the repo. No images yet; any future image requires recorded source, license and consent. No license chosen yet (decided at M10). Gap: cases have no reviewed verdicts and no second rater.

## Contribution
Ilghar: critiques, requirements, design/curation expertise as documented source material. Implementation: AI-assisted (Grok Bot), attributed per commit.
