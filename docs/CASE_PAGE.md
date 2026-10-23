# Cultural and typographic AI evaluation kit

> How can evaluators separate factual cultural/typographic constraint failures from subjective aesthetic preference, while documenting disagreement and source provenance?

**Status:** Measured check self-consistency on template artifacts; no model or rater results. Private work in progress.

## Problem
How can evaluators separate factual cultural/typographic constraint failures from subjective aesthetic preference, while documenting disagreement and source provenance?

## Existing contribution
Ilghar Dadgostari: problem framing, requirements and evaluation direction. Implementation AI-assisted (Grok Bot), reviewed only by Grok Bot so far.

## Architecture
See `architecture.mmd` (authoritative) and `architecture.svg` (fallback). Stages: Cleared brief + reference constraints → Original or licensed candidate example → Separate factual and aesthetic rubric axes → Independent annotation + uncertainty → Adjudication without identity-based inference → Versioned evaluation report and design examples

## Example
See README *Vertical slice* and `tests/receipts/`.

## Measured results
- automated check detection of generated corruptions: 15/15 (measured self-consistency; corruptions written by check author)
- false positives on clean template artifacts: 0/4 (measured; template SVG, not model outputs)

## Limitations
- No generative model outputs evaluated.
- No human annotations; aesthetic axes unmeasured.
- C03/C04 are human-review-only; text checks cannot see font shaping.

## Next step
See `handoff/NEXT.md`.
