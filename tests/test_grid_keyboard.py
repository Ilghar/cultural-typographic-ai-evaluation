import pathlib, sys, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from cultural_typographic_ai_evaluation.grid import check_grid
from cultural_typographic_ai_evaluation.keyboard import check_keys, PERSIAN_32
A4 = {"unit": "pt", "page": {"w": 595.276, "h": 841.89}, "columns": 6, "rows": 9, "gutter": 12}
class Grid(unittest.TestCase):
    def test_recorded_inside_margin_drift_is_caught(self):
        s = dict(A4, margins={"top": 36, "bottom": 36, "inside": 37.89, "outside": 36}, equal_margins=["top", "bottom", "inside", "outside"])
        r = check_grid(s); self.assertEqual(r["verdict"], "fail"); self.assertIn("37.89", r["findings"][0]["evidence"])
    def test_square_module_solution_passes(self):
        # 6x6 modules of 60pt with 12pt gutters on a 420x420 text area: square and on a 12pt baseline
        s = {"unit": "pt", "page": {"w": 492, "h": 492}, "margins": {"top": 36, "bottom": 36, "inside": 36, "outside": 36},
             "columns": 6, "rows": 6, "gutter": 12, "baseline": 12, "square_modules": True, "equal_margins": ["top", "bottom", "inside", "outside"]}
        r = check_grid(s); self.assertEqual(r["verdict"], "pass", r); self.assertEqual(r["derived"]["module"], [60.0, 60.0])
    def test_non_square_and_off_baseline_fail(self):
        s = dict(A4, margins={"top": 36, "bottom": 36, "inside": 36, "outside": 36}, square_modules=True, baseline=12)
        r = check_grid(s); self.assertEqual(r["verdict"], "fail"); self.assertEqual({f["check"] for f in r["findings"] if f["verdict"] == "fail"}, {"square_modules", "baseline_rhythm"})
    def test_malformed_inputs_never_raise(self):
        for bad in [{}, {"unit": "in"}, dict(A4, margins={"top": float("nan"), "bottom": 1, "inside": 1, "outside": 1}),
                    dict(A4, columns=True, margins={"top": 1, "bottom": 1, "inside": 1, "outside": 1}),
                    dict(A4, gutter=500, margins={"top": 1, "bottom": 1, "inside": 1, "outside": 1})]:
            self.assertEqual(check_grid(bad)["verdict"], "fail")
    def test_mm_converts_to_pt(self):
        s = {"unit": "mm", "page": {"w": 100, "h": 100}, "margins": {"top": 0, "bottom": 0, "inside": 0, "outside": 0}, "columns": 1, "rows": 1, "gutter": 0}
        self.assertAlmostEqual(check_grid(s)["derived"]["module_pt"][0], 283.465, places=2)
class Keyboard(unittest.TestCase):
    def test_full_correct_alphabet_passes(self):
        self.assertEqual(check_keys({i: ch for i, ch in enumerate(PERSIAN_32)})["verdict"], "pass")
    def test_duplicates_lookalikes_and_missing(self):
        keys = {i: ch for i, ch in enumerate(PERSIAN_32)}; keys[30] = "\u0643"; keys[31] = "\u062f"; keys[40] = "\u062f"
        kinds = {f["kind"] for f in check_keys(keys)["findings"]}
        self.assertEqual(kinds, {"arabic_lookalike", "duplicate", "missing"})
    def test_latin_and_empty_keys_flagged(self):
        r = check_keys({"q": "D", "w": "", "e": None}, require_full_alphabet=False)
        self.assertEqual(sorted(f["kind"] for f in r["findings"]), ["empty", "empty", "not_a_persian_letter"])
    def test_32_distinct_letters(self):
        self.assertEqual(len(set(PERSIAN_32)), 32)
if __name__ == "__main__": unittest.main()
