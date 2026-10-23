import json, pathlib, subprocess, sys, tempfile, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from cultural_typographic_ai_evaluation.slice import render_card, extract, evaluate
SPEC = {"fields": {"title": "<b>کتاب‌ها</b>", "date": "2026", "venue": "تالار"}, "expected_order": ["rtl:title", "ltr:date", "rtl:venue"], "required_fields": ["title", "date", "venue"]}
class Slice(unittest.TestCase):
    def test_render_escapes_and_roundtrips_exact_unicode(self):
        svg = render_card(SPEC); self.assertNotIn("<b>", svg)
        self.assertEqual(extract(svg)["fields"]["title"], SPEC["fields"]["title"])
    def test_missing_field_and_wrong_order_fail(self):
        s = dict(SPEC, fields={"title": "کتاب", "date": "2026", "venue": ""}); s["expected_order"] = ["ltr:date", "rtl:title", "rtl:venue"]
        v = [r["verdict"] for r in evaluate(s, render_card(s))]; self.assertEqual(v, ["pass", "fail", "fail"])
    def test_end_to_end_on_cleared_cases(self):
        with tempfile.TemporaryDirectory() as t:
            subprocess.run([sys.executable, "-m", "cultural_typographic_ai_evaluation", "slice", "inputs/synthetic_cases.json", "--specs", "fixtures/card_specs_m04.json", "--out", t], check=True, cwd=ROOT, env={"PYTHONPATH": str(ROOT / "src")}, capture_output=True)
            r = json.loads((pathlib.Path(t) / "report.json").read_text())["cases"]; self.assertTrue((pathlib.Path(t) / "C01.svg").exists())
        self.assertEqual(sorted(r), ["C01", "C02", "C03", "C04", "C05", "C06"])
        self.assertEqual([x["verdict"] for x in r["C01"]["automated_checks"]], ["pass"] * 3)
        neg = r["C01"]["negative_control_checks"][0]; self.assertEqual(neg["verdict"], "fail"); self.assertIn("ZWNJ", neg["evidence"])
        self.assertTrue(all(r[k]["automated_checks"] == [] and r[k]["gold_verdict"] is None for k in ["C03", "C04", "C05", "C06"]))
        self.assertIsNone(r["C03"]["annotation_template"]["aesthetic_ratings"][0]["rating"])
if __name__ == "__main__": unittest.main()
