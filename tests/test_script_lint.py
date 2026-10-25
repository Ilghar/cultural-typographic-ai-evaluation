import json, pathlib, subprocess, sys, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from cultural_typographic_ai_evaluation.script_lint import lint_text, lint_document
FX = ROOT / "tests/fixtures/script_lint"
def rules(t): return [f["rule"] for f in lint_text(t)]
class Rules(unittest.TestCase):
    def test_yeh_kaf(self):
        self.assertEqual(rules("ميخواهم كتاب").count("PS001"), 1); self.assertIn("PS002", rules("كتاب"))
        self.assertIn("PS001", rules("على"))
    def test_zwnj(self):
        self.assertEqual(rules("کتاب\u200cها"), [])
        self.assertIn("PS003", rules("کتاب\u200c\u200cها")); self.assertIn("PS003", rules("و \u200cخانه"))
        self.assertIn("PS003", rules("خانه\u200cها") + rules("در\u200cها"))
        self.assertEqual(rules("خانه\u200cها"), [])  # heh is dual-joining: valid
        self.assertIn("PS003", rules("در\u200cها"))
    def test_bidi_and_digits(self):
        self.assertEqual(rules("\u202bسلام\u202c"), ["PS004", "PS004"])
        self.assertIn("PS005", rules("1403 ۱۴۰۳")); self.assertNotIn("PS005", rules("۱۴۰۳"))
    def test_mi_prefix(self):
        self.assertIn("PS006", rules("میخواهم")); self.assertNotIn("PS006", rules("می\u200cخواهم"))
class Docs(unittest.TestCase):
    def test_fixtures(self):
        d = lint_document(json.loads((FX / "dirty.json").read_text("utf-8")))
        self.assertEqual(d["counts"], {"PS001": 1, "PS002": 1, "PS003": 3, "PS004": 2, "PS005": 1, "PS006": 1})
        self.assertTrue(lint_document(json.loads((FX / "clean.json").read_text("utf-8")))["clean"])
    def test_cli_exit_codes(self):
        run = lambda f: subprocess.run([sys.executable, "-m", "cultural_typographic_ai_evaluation.script_lint", str(FX / f), "--json", "--fields", "output"],
                                       cwd=ROOT, env={"PYTHONPATH": str(ROOT / "src")}, capture_output=True, text=True)
        self.assertEqual(run("dirty.json").returncode, 1); self.assertEqual(run("clean.json").returncode, 0)
        self.assertEqual(run("missing.json").returncode, 2)
if __name__ == "__main__": unittest.main()
