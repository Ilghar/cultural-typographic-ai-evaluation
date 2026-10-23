import pathlib, sys, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from cultural_typographic_ai_evaluation import failure, checks, aggregate as ag
class M07(unittest.TestCase):
    def test_adversarial_suite_all_pass(self):
        r = failure.run(); self.assertEqual(r["passed"], r["n"], [x for x in r["rows"] if not x["pass"]])
    def test_invisible_text_is_not_a_present_field(self):
        for v in ("\u200b", "\u200c\u200c", "\u202b", None, 0, " \u00a0"):
            with self.subTest(v=repr(v)): self.assertEqual(checks.required_fields(["t"], {"t": v})["verdict"], "fail")
    def test_numeric_claims_in_any_script_fail(self):
        base = 'flowchart LR\n  a["A"]'
        for claim in ("50%", "۵۰٪", "12.5 %", "30 percent", "۴۰ درصد"):
            with self.subTest(claim=claim): self.assertEqual(checks.diagram_fidelity(["A"], base + f'\n  a -.->|"{claim}"| a')["verdict"], "fail")
        self.assertEqual(checks.diagram_fidelity(["A"], base)["verdict"], "pass")
    def test_disagreement_and_adjudication_flags(self):
        A = lambda rid, v: {"rater_id": rid, "case_id": "C", "constraint_results": [{"constraint_id": "k", "verdict": v}], "aesthetic_ratings": []}
        r = ag.aggregate([A("a", "pass"), A("b", "uncertain"), A("c", "not_applicable")])["constraints"]["k"]
        self.assertFalse(r["disagreement"]); self.assertTrue(r["needs_adjudication"])
        r = ag.aggregate([A("a", "pass"), A("a", "fail")]); self.assertEqual(r["n_valid_annotations"], 1); self.assertEqual(len(r["rejected_annotations"]), 1)
if __name__ == "__main__": unittest.main()
