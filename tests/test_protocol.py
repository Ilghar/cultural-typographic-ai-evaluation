"""The proposed evaluation protocol stays proposed, linked, and free of new numbers."""
import re, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/EVALUATION_PROTOCOL.md"


class ProtocolDoc(unittest.TestCase):
    def setUp(self):
        self.text = DOC.read_text(encoding="utf-8")

    def test_marked_proposed_and_cites_sources(self):
        self.assertIn("**Status: proposed, not run.**", self.text)
        self.assertIn("https://proceedings.mlr.press/v81/buolamwini18a.html", self.text)
        self.assertIn("https://research.google/pubs/consensus-and-subjectivity-of-skin-tone-annotation-for-ml-fairness/", self.text)

    def test_only_existing_numbers(self):
        # Fractions in the doc must be the already-measured M06 results.
        self.assertEqual(sorted(set(re.findall(r"\b\d+/\d+\b", self.text))), ["0/4", "15/15"])

    def test_linked_from_datasheet_and_results(self):
        for rel, link in [("data/collection_v1/DATASHEET.md", "../../docs/EVALUATION_PROTOCOL.md"), ("docs/RESULTS.md", "EVALUATION_PROTOCOL.md")]:
            src = ROOT / rel
            self.assertIn(f"({link})", src.read_text(encoding="utf-8"))
            self.assertTrue((src.parent / link).resolve().is_file())


if __name__ == "__main__":
    unittest.main()
