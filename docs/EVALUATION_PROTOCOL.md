# Proposed independent evaluation protocol

**Status: proposed, not run.** Nothing in this document has been carried out. It adds no data, no annotations, no model calls and no new numbers. It describes how a future evaluation could be recorded so that results can be read honestly.

## What exists today
- Collection v1 has six development cases (C01–C06), `n=6`. It is too small to split, and `gold_verdict` is null for every case ([datasheet](../data/collection_v1/DATASHEET.md)).
- The M06 baseline ([results](RESULTS.md)) detected 15/15 generated corruptions and raised 0/4 false positives on clean template artifacts. These are internal fixture results: the corruptions were written by the author of the checks, and the clean artifacts are templates, not model outputs. They show the checks are self-consistent. They are not a measure of independent model performance, and they say nothing about fairness.

## Why disaggregate, and why record raters
- [Gender Shades (Buolamwini and Gebru, PMLR v81, 2018)](https://proceedings.mlr.press/v81/buolamwini18a.html) showed that one overall error rate can hide large differences between subgroups. That motivates reporting errors per relevant case type, with numerators and denominators, instead of one pooled figure.
- [Consensus and subjectivity of skin tone annotation for ML fairness (Google Research)](https://research.google/pubs/consensus-and-subjectivity-of-skin-tone-annotation-for-ml-fairness/) found that annotator background and context affect labels and that disagreement carries information. That motivates recording rater context and keeping disagreement visible instead of averaging it away.
- Neither source establishes that this typography kit is fair, and following this protocol would not show that either. It would only make errors and disagreements easier to see.

## Future sample: what it must be
- Separately sourced from the development cases, and not written by the author of the checks.
- Every artifact consent- and licence-cleared before inclusion. Artifacts without cleared rights are left out, not anonymised and kept.
- Small samples are reported as counts with their denominators. No percentages without the count beside them, no confidence claims the sample cannot support, and no claim that the sample represents Persian typography, Persian speakers or any population.

## Per-artifact record
| field | required? | notes |
|---|---|---|
| `artifact_id` | required | stable id |
| `origin` | required | `human-made`, `model-generated` or `unknown`; for model output, the model name and version if known |
| `source_and_rights` | required | where it came from, licence or consent reference |
| `case_type` | required | one of the kit's case types (e.g. card text, diagram, stage list) |
| `design_context` | optional | intended use, medium, brief, as stated by the source; otherwise `unknown` |
| `script_and_language` | required | as stated by the source or visible in the artifact; otherwise `unknown` |
| `automated_check_results` | required | output of the existing checks, unchanged |

Do not record or infer the nationality, ethnicity, religion, gender or any other identity attribute of artifact makers or of people shown. Leave unknown values as `unknown`; never fill them by guessing.

## Human review
- **Factual and cultural checks** (correct letterforms, ZWNJ use, Persian rather than Arabic kaf/yeh, reading order, venue and title facts): at least two independent reviewers per artifact, each blind to the other's verdict and to the automated check results. Each verdict is `pass`, `fail` or `cannot judge`, with a short reason.
- **Aesthetic ratings** are recorded in a separate field and reported separately. They never change a factual verdict and never count as an error.
- **Rater context** (optional, self-described only): relevant reading fluency in Persian script and typographic experience, in the rater's own words. No other personal data is collected.

## Disagreement and adjudication
- Record every reviewer's verdict before adjudication. Report the raw agreement count per case type (for example, `agreed k of n`).
- Disagreements go to an adjudicator, who records the final verdict and the reason. The original verdicts stay in the record.
- If adjudication cannot resolve it, the final verdict is `disputed` and is reported as such, not dropped.

## Reporting
For each relevant case type, report:
- the number of artifacts reviewed (the denominator);
- automated-check flags against the adjudicated human verdict: true flags, missed failures and false flags, each as `k/n`;
- the number of `disputed` and `cannot judge` items.

No pooled score across case types, and no statement that bias has been removed or that the kit is fair.
