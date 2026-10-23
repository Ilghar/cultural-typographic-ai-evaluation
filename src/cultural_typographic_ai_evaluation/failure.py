"""M07: adversarial/malformed inputs for checks + aggregation. Each row states the verdict a correct checker must give."""
from . import checks, aggregate as ag
T = "کارگاه Python برای همه"
STAGES = ["Brief", "Check", "Report"]
MM = 'flowchart LR\n  a["Brief"] --> b["Check"] --> c["Report"]'
def _ann(rid="r1", rating=3, verdict="pass", **extra):
    return dict({"rater_id": rid, "case_id": "C01", "constraint_results": [{"constraint_id": "k", "verdict": verdict}], "aesthetic_ratings": [{"axis": "balance", "rating": rating}]}, **extra)
CHECKS = [  # (name, callable, expected_verdict)
    ("glyph_clean", lambda: checks.glyph_exact(T, T), "pass"),
    ("glyph_arabic_yeh", lambda: checks.glyph_exact(T, T.replace("ی", "ي")), "fail"),
    ("glyph_nfd_vs_nfc", lambda: checks.glyph_exact("آ", "ا\u0653"), "fail"),
    ("glyph_injected_rlm", lambda: checks.glyph_exact(T, "\u200f" + T), "fail"),
    ("glyph_observed_int", lambda: checks.glyph_exact(T, 5), "fail"),
    ("glyph_observed_list", lambda: checks.glyph_exact(T, [T]), "fail"),
    ("order_clean", lambda: checks.reading_order(["rtl:title"], ["rtl:title"]), "pass"),
    ("order_tuple_vs_list", lambda: checks.reading_order(["rtl:title"], ("rtl:title",)), "fail"),
    ("fields_clean", lambda: checks.required_fields(["title"], {"title": T}), "pass"),
    ("fields_zwsp_only", lambda: checks.required_fields(["title"], {"title": "\u200b\u200c"}), "fail"),
    ("fields_bidi_only", lambda: checks.required_fields(["title"], {"title": "\u202b\u202c"}), "fail"),
    ("fields_not_dict", lambda: checks.required_fields(["title"], "title"), "fail"),
    ("fields_none_value", lambda: checks.required_fields(["title"], {"title": None}), "fail"),
    ("diagram_clean", lambda: checks.diagram_fidelity(STAGES, MM), "pass"),
    ("diagram_pct_ascii", lambda: checks.diagram_fidelity(STAGES, MM + '\n  c --> d["50% better"]'), "fail"),
    ("diagram_pct_persian", lambda: checks.diagram_fidelity(STAGES, MM + '\n  c -.->|"۵۰٪ بهتر"| c'), "fail"),
    ("diagram_pct_word", lambda: checks.diagram_fidelity(STAGES, MM + '\n  c -.->|"50 percent better"| c'), "fail"),
    ("diagram_swapped", lambda: checks.diagram_fidelity(STAGES, MM.replace('"Brief"', '"X"').replace('"Check"', '"Brief"').replace('"X"', '"Check"')), "fail"),
    ("diagram_duplicate_stage", lambda: checks.diagram_fidelity(STAGES, MM + '\n  c --> d["Report"]'), "fail"),
    ("diagram_not_string", lambda: checks.diagram_fidelity(STAGES, None), "fail"),
]
AGG = [  # (name, annotations, predicate on result)
    ("agg_bool_rating_rejected", [_ann(rating=True)], lambda r: r["n_valid_annotations"] == 0),
    ("agg_identity_field_case_variant", [_ann(Rater_Nationality="x")], lambda r: r["n_valid_annotations"] == 0),
    ("agg_missing_results_no_crash", [{"rater_id": "r1", "case_id": "C01"}], lambda r: r["n_valid_annotations"] == 0),
    ("agg_results_not_list", [_ann(constraint_results="pass")], lambda r: r["n_valid_annotations"] == 0),
    ("agg_duplicate_rater_rejected", [_ann("r1"), _ann("r1", verdict="fail")], lambda r: r["n_valid_annotations"] == 1),
    ("agg_pass_vs_uncertain_flagged", [_ann("r1"), _ann("r2", verdict="uncertain")], lambda r: r["constraints"]["k"]["needs_adjudication"]),
    ("agg_pass_vs_fail_flagged", [_ann("r1"), _ann("r2", verdict="fail")], lambda r: r["constraints"]["k"]["disagreement"] and r["constraints"]["k"]["needs_adjudication"]),
    ("agg_agreement_not_flagged", [_ann("r1"), _ann("r2")], lambda r: not r["constraints"]["k"]["needs_adjudication"]),
]
def run():
    rows = []
    for name, f, exp in CHECKS:
        try: v = f()["verdict"]; err = None
        except Exception as e: v, err = None, f"{type(e).__name__}: {e}"
        rows.append({"name": name, "expected": exp, "got": v, "exception": err, "pass": v == exp})
    for name, anns, pred in AGG:
        try: r = ag.aggregate(anns); ok = bool(pred(r)); err = None
        except Exception as e: ok, err = False, f"{type(e).__name__}: {e}"
        rows.append({"name": name, "exception": err, "pass": ok})
    return {"n": len(rows), "passed": sum(r["pass"] for r in rows), "rows": rows}
