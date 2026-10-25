"""Regression tests for findings in docs/REVIEW_M01_M07.md (AI self-review)."""
import pathlib, sys, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
from cultural_typographic_ai_evaluation.aggregate import validate_annotation
class Review(unittest.TestCase):
    def test_identity_field_does_not_hide_other_errors(self):
        e = validate_annotation({"rater_id": "r", "rater_nationality": "x", "constraint_results": [], "aesthetic_ratings": [{"axis": "a", "rating": 9}]})
        self.assertIn("forbidden identity field rater_nationality", e); self.assertTrue(any("rating out of range" in x for x in e))
    def test_structural_errors_still_stop_early(self):
        self.assertIn("aesthetic_ratings must be a list of objects", validate_annotation({"rater_id": "r", "constraint_results": [], "aesthetic_ratings": 3}))
if __name__ == "__main__": unittest.main()
