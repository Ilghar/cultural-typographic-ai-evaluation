"""Keep factual verdicts and aesthetic ratings separate; never merge into one score."""
from collections import Counter, defaultdict
FORBIDDEN = {"rater_nationality", "rater_ethnicity", "rater_native_language_as_authority"}
def validate_annotation(a):
    errs = [f"forbidden identity field {k}" for k in a if k in FORBIDDEN]
    for r in a.get("aesthetic_ratings", []):
        if not isinstance(r.get("rating"), int) or not 1 <= r["rating"] <= 5: errs.append(f"rating out of range on {r.get('axis')}")
    for c in a.get("constraint_results", []):
        if c.get("verdict") not in {"pass", "fail", "uncertain", "not_applicable"}: errs.append(f"bad verdict {c.get('verdict')}")
    return errs
def aggregate(annotations):
    valid, rejected = [], []
    for a in annotations:
        e = validate_annotation(a); (rejected.append({"rater_id": a.get("rater_id"), "errors": e}) if e else valid.append(a))
    cons = defaultdict(Counter); axes = defaultdict(list)
    for a in valid:
        for c in a["constraint_results"]: cons[c["constraint_id"]][c["verdict"]] += 1
        for r in a["aesthetic_ratings"]: axes[r["axis"]].append(r["rating"])
    constraints = {k: {"counts": dict(sorted(v.items())), "raters": sum(v.values()), "disagreement": v["pass"] > 0 and v["fail"] > 0} for k, v in sorted(cons.items())}
    aesthetics = {k: {"n": len(v), "min": min(v), "max": max(v), "distribution": dict(sorted(Counter(v).items()))} for k, v in sorted(axes.items())}
    return {"constraints": constraints, "aesthetics": aesthetics, "rejected_annotations": rejected, "n_valid_annotations": len(valid)}
