"""M04 vertical slice: cleared synthetic spec -> deterministic native-text SVG artifact -> text extraction
-> automated factual checks -> blank annotation template (human axes) -> report.
Renderer is a plain template (not an AI generator); it exists to exercise the evaluation path end to end."""
import json, xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from .checks import run as run_checks
NS = "{http://www.w3.org/2000/svg}"
def render_card(spec, corrupt=None):
    f = dict(spec["fields"])
    if corrupt: f = {k: corrupt(v) for k, v in f.items()}
    rows = [("title", 'direction="rtl" font-size="28"', 60), ("date", 'direction="ltr" font-size="16"', 110),
            ("venue", 'direction="rtl" font-size="16"', 140)]
    body = "".join(f'<text id="{k}" x="300" y="{y}" text-anchor="middle" {a}>{escape(f.get(k, ""))}</text>' for k, a, y in rows if k in f)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" lang="fa">{body}</svg>'
def extract(svg):
    root = ET.fromstring(svg)
    els = [(e.get("id"), e.text or "", e.get("direction", "ltr"), float(e.get("y"))) for e in root.iter(NS + "text")]
    els.sort(key=lambda x: x[3])
    return {"fields": {i: t for i, t, _, _ in els}, "order": [f"{d}:{i}" for i, _, d, _ in els]}
def evaluate(spec, svg):
    ex = extract(svg)
    artifact = {"title": ex["fields"].get("title"), "order": ex["order"], "fields": ex["fields"]}
    case = {"constraints": [{"id": "title", "type": "glyph_exact", "expected": spec["fields"]["title"]},
                            {"id": "order", "type": "reading_order", "expected": spec["expected_order"]},
                            {"id": "fields", "type": "required_fields", "expected": spec["required_fields"]}]}
    return run_checks(case, artifact)
def annotation_template(case):
    return {"case_id": case["id"], "artifact_id": None, "rater_id": None,
            "constraint_results": [{"constraint_id": "objective", "verdict": None, "evidence": None, "source_citation": None, "instructions": case.get("objective_check")}],
            "aesthetic_ratings": [{"axis": case.get("subjective_axis"), "rating": None, "rationale": None, "confidence": None}],
            "notes": "Fill independently. Do not record nationality/ethnicity; cite sources for cultural claims."}
def run(cases, specs):
    out = {}
    for c in cases:
        s = specs.get(c["id"])
        entry = {"brief": c["brief"], "gold_verdict": None, "annotation_template": annotation_template(c)}
        if s:
            svg = render_card(s); entry["artifact_svg"] = svg; entry["automated_checks"] = evaluate(s, svg)
            bad = render_card(s, corrupt=lambda v: v.replace("\u200c", "").replace("\u06a9", "\u0643"))
            entry["negative_control_checks"] = evaluate(s, bad)
        else:
            entry["automated_checks"] = []; entry["status"] = "human_review_only (no automatable spec)"
        out[c["id"]] = entry
    return out
