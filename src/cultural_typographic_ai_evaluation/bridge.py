"""Bridge the Drive source format (inputs/synthetic_cases.json) into schemas/case.schema.json for ALL cases.
Automatable constraints get an `expected` from fixtures/card_specs (C01, C02, C05) or a stage list (C06);
C03/C04 constraints are typed but left for human review (no expected value is invented)."""
import json, pathlib
TYPE = {"C01": ["glyph_exact"], "C02": ["required_fields", "reading_order"], "C03": ["reference_justified"],
        "C04": ["identity_attribute_preserved"], "C05": ["reading_order", "glyph_exact"], "C06": ["diagram_fidelity"]}
def _dir(v):
    fa = any("\u0600" <= ch <= "\u06ff" for ch in v); la = any(ch.isascii() and ch.isalpha() for ch in v)
    return "mixed" if fa and la else ("rtl" if fa else "ltr")

def bridge(src_cases, specs):
    out = []
    for c in src_cases:
        sp = specs.get(c["id"], {}); cons = []
        for i, t in enumerate(TYPE[c["id"]], 1):
            k = {"id": f"{c['id']}-{t}", "type": t, "description": c["objective_check"]}
            if t == "glyph_exact" and sp.get("fields"): k["expected"] = sp["fields"]["title"]
            if t == "reading_order" and sp.get("expected_order"): k["expected"] = sp["expected_order"]
            if t == "required_fields" and sp.get("required_fields"): k["expected"] = sp["required_fields"]
            if t == "diagram_fidelity" and sp.get("stages"): k["expected"] = sp["stages"]
            if "expected" not in k: k["review"] = "human_only"
            cons.append(k)
        f = sp.get("fields", {})
        rt = [{"text": v, "direction": _dir(v)} for v in f.values()]
        out.append({"id": c["id"], "kind": c["kind"], "brief": c["brief"], "required_text": rt, "constraints": cons,
                    "aesthetic_axes": [c["subjective_axis"]], "rights": {"source": "newly drafted (Drive S-register)", "license": "not yet chosen (repo-level decision at M10)", "consent": "not_applicable_synthetic", "private": False},
                    "review_status": c["review_status"], "gold_verdict": None})
    return out
