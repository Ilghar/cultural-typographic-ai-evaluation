"""Deterministic factual checks on native-text artifacts. No aesthetic judgement here."""
import unicodedata
CONFUSABLES = {"\u0643": "\u06a9", "\u064a": "\u06cc", "\u0649": "\u06cc"}  # Arabic kaf/yeh/alef maksura vs Persian
ZWNJ = "\u200c"
def cps(s): return [f"U+{ord(c):04X}" for c in s]
def glyph_exact(expected, observed):
    if expected == observed: return {"verdict": "pass", "evidence": "exact codepoint match"}
    notes = []
    if expected.count(ZWNJ) != observed.count(ZWNJ): notes.append(f"ZWNJ count {expected.count(ZWNJ)} expected, {observed.count(ZWNJ)} observed")
    for a, p in CONFUSABLES.items():
        if a in observed and p in expected: notes.append(f"Arabic {unicodedata.name(a)} used where Persian {unicodedata.name(p)} expected")
    if not notes: notes.append(f"expected {cps(expected)} observed {cps(observed)}")
    return {"verdict": "fail", "evidence": "; ".join(notes)}
def reading_order(expected_runs, observed_runs):
    return {"verdict": "pass" if expected_runs == observed_runs else "fail", "evidence": f"expected {expected_runs} observed {observed_runs}"}
def required_fields(required, artifact_fields):
    missing = [f for f in required if not str(artifact_fields.get(f, "")).strip()]
    return {"verdict": "fail" if missing else "pass", "evidence": "missing: " + ", ".join(missing) if missing else "all present"}
def run(case, artifact):
    out = []
    for c in case["constraints"]:
        t = c["type"]; a = artifact.get(c["id"])
        if a is None: r = {"verdict": "uncertain", "evidence": "artifact lacks data for this constraint"}
        elif t == "glyph_exact": r = glyph_exact(c["expected"], a)
        elif t == "reading_order": r = reading_order(c["expected"], a)
        elif t == "required_fields": r = required_fields(c["expected"], a)
        else: r = {"verdict": "uncertain", "evidence": f"{t} needs human review"}
        out.append({"constraint_id": c["id"], "type": t, **r})
    return out
