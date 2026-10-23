import json, pathlib, subprocess, sys, tempfile, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from cultural_typographic_ai_evaluation.schema import validate, load_schema
from cultural_typographic_ai_evaluation.collection import build, mermaid
from cultural_typographic_ai_evaluation.checks import diagram_fidelity
class Bridge(unittest.TestCase):
    def test_all_six_cases_bridge_and_validate(self):
        m, _ = build(ROOT); self.assertEqual(m["errors"], []); self.assertEqual([c["id"] for c in m["cases"]], ["C01", "C02", "C03", "C04", "C05", "C06"])
        self.assertEqual(m["human_only"]["C03"], ["reference_justified"]); self.assertEqual(m["human_only"]["C04"], ["identity_attribute_preserved"])
        self.assertTrue(all(c["gold_verdict"] is None for c in m["cases"]))
        self.assertEqual(next(c for c in m["cases"] if c["id"] == "C05")["required_text"][0]["direction"], "mixed")
    def test_annotation_schema_forbids_identity_fields(self):
        s = load_schema(ROOT, "annotation.schema.json")
        a = {"case_id": "C01", "artifact_id": "a", "rater_id": "r", "constraint_results": [], "aesthetic_ratings": []}
        self.assertEqual(validate(a, s), []); self.assertTrue(validate(dict(a, rater_ethnicity="x"), s))
        self.assertTrue(validate(dict(a, aesthetic_ratings=[{"axis": "x", "rating": 6, "rationale": "r"}]), s))
class Diagram(unittest.TestCase):
    def test_fidelity(self):
        st = ["A", "B", "C"]
        self.assertEqual(diagram_fidelity(st, mermaid(st))["verdict"], "pass")
        for kw in ({"swap": (0, 1)}, {"drop": 1}, {"add_metric": True}):
            self.assertEqual(diagram_fidelity(st, mermaid(st, **kw))["verdict"], "fail")
class Baseline(unittest.TestCase):
    def test_measured_detector_baseline_regression(self):
        with tempfile.TemporaryDirectory() as t:
            subprocess.run([sys.executable, "-m", "cultural_typographic_ai_evaluation", "baseline", "--out", t], check=True, cwd=ROOT, env={"PYTHONPATH": str(ROOT / "src")}, capture_output=True)
            r = json.loads((pathlib.Path(t) / "baseline.json").read_text())
        self.assertEqual(r["detection"], {"detected": 15, "denominator": 15, "value": 1.0})
        self.assertEqual(r["false_positives_on_clean"], {"count": 0, "denominator": 4})
        self.assertTrue(any("self-consistency" in l for l in r["limitations"]))
if __name__ == "__main__": unittest.main()
