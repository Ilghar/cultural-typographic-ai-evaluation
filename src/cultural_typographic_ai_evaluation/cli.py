import argparse, hashlib, json, pathlib, sys
from .checks import run
from .aggregate import aggregate
def main(argv=None):
    ap = argparse.ArgumentParser(prog="cultural_typographic_ai_evaluation"); ap.add_argument("cmd", choices=["report","slice","collection","baseline","failure"]); ap.add_argument("--specs")
    ap.add_argument("fixture", nargs="?", default="."); ap.add_argument("--out", required=True); a = ap.parse_args(argv)
    if a.cmd == "failure":
        from .failure import run as frun
        rep = frun(); o = pathlib.Path(a.out); o.mkdir(parents=True, exist_ok=True)
        (o / "failure.json").write_text(json.dumps(rep, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
        print(json.dumps({"passed": f'{rep["passed"]}/{rep["n"]}'})); return 0 if rep["passed"] == rep["n"] else 1
    if a.cmd in ("collection", "baseline"):
        from .collection import build, corruption_suite
        man, specs = build(a.fixture); o = pathlib.Path(a.out); o.mkdir(parents=True, exist_ok=True)
        if a.cmd == "collection":
            (o / "manifest.json").write_text(json.dumps(man, indent=1, sort_keys=True, ensure_ascii=False) + "\n"); print(json.dumps({"errors": man["errors"], "automatable": man["automatable"]})); return 1 if man["errors"] else 0
        rep = corruption_suite(specs); (o / "baseline.json").write_text(json.dumps(rep, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
        print(json.dumps({k: rep[k] for k in ("detection", "false_positives_on_clean", "by_variant")})); return 0
    raw = pathlib.Path(a.fixture).read_bytes(); d = json.loads(raw)
    if a.cmd == "slice":
        from .slice import run as srun
        res = srun(d, json.loads(pathlib.Path(a.specs).read_text())["specs"]); o = pathlib.Path(a.out); o.mkdir(parents=True, exist_ok=True)
        for k, v in res.items():
            if "artifact_svg" in v: (o / f"{k}.svg").write_text(v.pop("artifact_svg"))
        rep = {"fixture_sha256": hashlib.sha256(raw).hexdigest(), "run_kind": "template_render", "cases": res}
        (o / "report.json").write_text(json.dumps(rep, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
        print(json.dumps({k: [r["verdict"] for r in v["automated_checks"]] for k, v in res.items()})); return 0
    rep = {"fixture_sha256": hashlib.sha256(raw).hexdigest(), "run_kind": d["run_kind"], "cases": {}}
    for c in d["cases"]:
        rep["cases"][c["id"]] = {"automated_checks": run(c, d["artifacts"].get(c["id"], {})),
                                 "human": aggregate([x for x in d["annotations"] if x["case_id"] == c["id"]]), "gold_verdict": None}
    o = pathlib.Path(a.out); o.mkdir(parents=True, exist_ok=True)
    (o / "report.json").write_text(json.dumps(rep, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
    print(json.dumps({k: [r["verdict"] for r in v["automated_checks"]] for k, v in rep["cases"].items()})); return 0
if __name__ == "__main__": sys.exit(main())
