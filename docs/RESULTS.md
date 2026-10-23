# Results (M06) — measured, synthetic only
Command: `PYTHONPATH=src python3 -m cultural_typographic_ai_evaluation baseline --out out/m06` (receipt `tests/receipts/m06_baseline.json`).

Detector baseline on a generated corruption suite over template RTL SVG cards (C01, C02, C05) and a Mermaid diagram (C06):
- Detection 15/15 across 9 variants (drop ZWNJ, ZWNJ→space, Arabic kaf, Arabic yeh, missing venue, title moved last, diagram swap/drop/invented metric). Some variants are not applicable to some cases and are excluded from the denominator.
- False positives on clean artifacts 0/4.

Reading: this shows the checks are internally consistent, not that they catch real model failures. Real candidate artifacts and multi-rater annotations are required for an empirical baseline.
