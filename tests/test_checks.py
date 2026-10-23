import json, pathlib, subprocess, sys, tempfile, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from cultural_typographic_ai_evaluation.checks import glyph_exact
from cultural_typographic_ai_evaluation.aggregate import aggregate
class Glyph(unittest.TestCase):
    def test_zwnj_and_arabic_kaf_detected(self):
        r = glyph_exact("می\u200cخواهم کتاب", "میخواهم كتاب")
        self.assertEqual(r["verdict"], "fail"); self.assertIn("ZWNJ count 1 expected, 0 observed", r["evidence"]); self.assertIn("ARABIC LETTER KAF", r["evidence"])
    def test_arabic_yeh_detected_and_exact_passes(self):
        self.assertIn("ARABIC LETTER YEH", glyph_exact("یک", "يک")["evidence"])
        self.assertEqual(glyph_exact("یک", "یک")["verdict"], "pass")
class Aggregation(unittest.TestCase):
    def test_identity_fields_and_range_rejected_minority_kept(self):
        anns = json.loads((ROOT / "fixtures/synthetic_eval_m03.json").read_text())["annotations"]
        r = aggregate(anns)
        self.assertEqual(r["n_valid_annotations"], 2); self.assertEqual(len(r["rejected_annotations"]), 1)
        self.assertTrue(any("forbidden identity field" in e for e in r["rejected_annotations"][0]["errors"]))
        self.assertEqual(r["constraints"]["ref"]["counts"], {"fail": 1, "pass": 1}); self.assertTrue(r["constraints"]["ref"]["disagreement"])
        self.assertEqual(r["aesthetics"]["hierarchy"]["distribution"], {2: 1, 4: 1}); self.assertNotIn("score", json.dumps(r))
class CLI(unittest.TestCase):
    def test_report(self):
        with tempfile.TemporaryDirectory() as t:
            subprocess.run([sys.executable, "-m", "cultural_typographic_ai_evaluation", "report", "fixtures/synthetic_eval_m03.json", "--out", t], check=True, cwd=ROOT, env={"PYTHONPATH": str(ROOT / "src")}, capture_output=True)
            r = json.loads((pathlib.Path(t) / "report.json").read_text())
        self.assertEqual([c["verdict"] for c in r["cases"]["X01"]["automated_checks"]], ["fail", "fail", "fail", "uncertain"])
        self.assertEqual(r["cases"]["X02"]["automated_checks"][0]["verdict"], "pass"); self.assertIsNone(r["cases"]["X01"]["gold_verdict"])
if __name__ == "__main__": unittest.main()
