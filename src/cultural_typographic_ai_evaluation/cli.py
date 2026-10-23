import argparse, hashlib, json, pathlib, sys
from .checks import run
from .aggregate import aggregate
def main(argv=None):
    ap = argparse.ArgumentParser(prog="cultural_typographic_ai_evaluation"); ap.add_argument("cmd", choices=["report"])
    ap.add_argument("fixture"); ap.add_argument("--out", required=True); a = ap.parse_args(argv)
    raw = pathlib.Path(a.fixture).read_bytes(); d = json.loads(raw)
    rep = {"fixture_sha256": hashlib.sha256(raw).hexdigest(), "run_kind": d["run_kind"], "cases": {}}
    for c in d["cases"]:
        rep["cases"][c["id"]] = {"automated_checks": run(c, d["artifacts"].get(c["id"], {})),
                                 "human": aggregate([x for x in d["annotations"] if x["case_id"] == c["id"]]), "gold_verdict": None}
    o = pathlib.Path(a.out); o.mkdir(parents=True, exist_ok=True)
    (o / "report.json").write_text(json.dumps(rep, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
    print(json.dumps({k: [r["verdict"] for r in v["automated_checks"]] for k, v in rep["cases"].items()})); return 0
if __name__ == "__main__": sys.exit(main())
