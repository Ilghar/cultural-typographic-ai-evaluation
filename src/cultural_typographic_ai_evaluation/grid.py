"""Modular grid checker: does a declared page grid actually hold together?

Restores an ambition from the original brief: "what should be the relation between the margins
and gutters and still arrive at a modular, flexible and square rhythmic grid-system?" and the
recorded failure where a generated InDesign template had one margin at 37.89 pt while the rest
were 36 pt. Pure arithmetic on declared numbers. No image or screenshot inference, no default 4/8 pt grid.
"""
import math
UNITS = {"pt": 1.0, "mm": 72 / 25.4, "px": 0.75}

def _num(v): return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)

def check_grid(spec, tol=0.01):
    """spec: unit, page{w,h}, margins{top,bottom,inside,outside}, columns, rows, gutter,
    optional baseline, optional equal_margins:[names], optional square_modules:bool."""
    errs, findings = [], []
    u = spec.get("unit")
    if u not in UNITS: return {"verdict": "fail", "errors": [f"unit must be one of {sorted(UNITS)}; got {u!r}"], "findings": []}
    pg, m = spec.get("page") or {}, spec.get("margins") or {}
    vals = {"page.w": pg.get("w"), "page.h": pg.get("h"), "gutter": spec.get("gutter"), **{f"margins.{k}": m.get(k) for k in ("top", "bottom", "inside", "outside")}}
    for k, v in vals.items():
        if not _num(v) or v < 0: errs.append(f"{k} must be a finite non-negative number; got {v!r}")
    for k in ("columns", "rows"):
        if not isinstance(spec.get(k), int) or isinstance(spec.get(k), bool) or spec.get(k) < 1: errs.append(f"{k} must be an integer >= 1")
    if errs: return {"verdict": "fail", "errors": errs, "findings": []}
    W = pg["w"] - m["inside"] - m["outside"]; H = pg["h"] - m["top"] - m["bottom"]
    c, r, g = spec["columns"], spec["rows"], spec["gutter"]
    mw = (W - g * (c - 1)) / c; mh = (H - g * (r - 1)) / r
    if mw <= 0 or mh <= 0: errs.append(f"no room for modules: module {mw:.3f} x {mh:.3f} {u}")
    eq = spec.get("equal_margins") or []
    if eq:
        vs = {k: m[k] for k in eq if k in m}
        if len(set(round(v, 6) for v in vs.values())) > 1:
            findings.append({"check": "equal_margins", "verdict": "fail", "evidence": f"declared equal but got {vs} {u}"})
        else: findings.append({"check": "equal_margins", "verdict": "pass", "evidence": f"{sorted(vs)} all {next(iter(vs.values()), None)} {u}"})
    if spec.get("square_modules"):
        ok = abs(mw - mh) <= tol
        findings.append({"check": "square_modules", "verdict": "pass" if ok else "fail",
                         "evidence": f"module {mw:.3f} x {mh:.3f} {u} (difference {abs(mw - mh):.3f})"})
    b = spec.get("baseline")
    if b is not None:
        if not _num(b) or b <= 0: errs.append("baseline must be a positive number")
        else:
            k = mh / b; kg = (mh + g) / b
            ok = abs(k - round(k)) <= tol and abs(kg - round(kg)) <= tol
            findings.append({"check": "baseline_rhythm", "verdict": "pass" if ok else "fail",
                             "evidence": f"module height = {k:.3f} baselines, module+gutter = {kg:.3f} baselines (both must be whole)"})
    verdict = "fail" if errs or any(f["verdict"] == "fail" for f in findings) else "pass"
    return {"verdict": verdict, "errors": errs, "findings": findings,
            "derived": {"unit": u, "text_area": [round(W, 3), round(H, 3)], "module": [round(mw, 3), round(mh, 3)],
                        "module_pt": [round(mw * UNITS[u], 3), round(mh * UNITS[u], 3)]}}
