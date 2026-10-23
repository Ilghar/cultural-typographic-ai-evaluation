"""Keep factual verdicts and aesthetic ratings separate; never merge into one score."""
from collections import Counter, defaultdict
FORBIDDEN = {"rater_nationality", "rater_ethnicity", "rater_native_language_as_authority"}
def validate_annotation(a):
    if not isinstance(a, dict): return ["annotation is not an object"]
    errs = [f"forbidden identity field {k}" for k in a if isinstance(k, str) and k.lower() in FORBIDDEN]
    if not isinstance(a.get("rater_id"), str) or not a["rater_id"]: errs.append("missing rater_id")
    for key in ("constraint_results", "aesthetic_ratings"):
        if not isinstance(a.get(key), list) or not all(isinstance(x, dict) for x in a[key]): errs.append(f"{key} must be a list of objects")
    if errs: return errs
    for r in a["aesthetic_ratings"]:
        v = r.get("rating")
        if isinstance(v, bool) or not isinstance(v, int) or not 1 <= v <= 5: errs.append(f"rating out of range on {r.get('axis')}")
    for c in a["constraint_results"]:
        if c.get("verdict") not in {"pass", "fail", "uncertain", "not_applicable"}: errs.append(f"bad verdict {c.get('verdict')}")
    return errs
def aggregate(annotations):
    valid, rejected, seen = [], [], set()
    for a in annotations:
        e = validate_annotation(a)
        rid = a.get("rater_id") if isinstance(a, dict) else None
        if not e and (rid, a.get("case_id")) in seen: e = ["duplicate rater_id for this case (first kept)"]
        if e: rejected.append({"rater_id": rid, "errors": e})
        else: valid.append(a); seen.add((rid, a.get("case_id")))
    cons = defaultdict(Counter); axes = defaultdict(list)
    for a in valid:
        for c in a["constraint_results"]: cons[c["constraint_id"]][c["verdict"]] += 1
        for r in a["aesthetic_ratings"]: axes[r["axis"]].append(r["rating"])
    constraints = {k: {"counts": dict(sorted(v.items())), "raters": sum(v.values()), "disagreement": v["pass"] > 0 and v["fail"] > 0,
                       "needs_adjudication": len([k2 for k2 in v if k2 != "not_applicable" and v[k2]]) > 1} for k, v in sorted(cons.items())}
    aesthetics = {k: {"n": len(v), "min": min(v), "max": max(v), "distribution": dict(sorted(Counter(v).items()))} for k, v in sorted(axes.items())}
    return {"constraints": constraints, "aesthetics": aesthetics, "rejected_annotations": rejected, "n_valid_annotations": len(valid)}
