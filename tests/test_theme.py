"""Light/dark theme: WCAG AA contrast for every text/background token pair in both themes, and the
generated pages carry both themes, the system fallback and an accessible, persisted toggle."""
import pathlib, re, sys, unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "tools"))
from cultural_typographic_ai_evaluation import theme
import export_site

class Theme(unittest.TestCase):
    def test_contrast_pairs_meet_wcag_aa_in_both_themes(self):
        for mode in ("light", "dark"):
            for fg, bg, minimum in theme.PAIRS:
                r = theme.contrast(theme.TOKENS[mode][fg], theme.TOKENS[mode][bg])
                self.assertGreaterEqual(r, minimum, f"{mode}: {fg} on {bg} = {r:.2f}")
    def test_contrast_formula_reference_values(self):
        self.assertAlmostEqual(theme.contrast("#000000", "#ffffff"), 21.0, places=2)
        self.assertAlmostEqual(theme.contrast("#777777", "#ffffff"), 4.48, places=2)
    def test_studio_tokens_unchanged(self):
        self.assertEqual(theme.TOKENS["dark"]["canvas"], "#4a434c"); self.assertEqual(theme.TOKENS["dark"]["ink"], "#f4eef3")
        self.assertEqual(theme.TOKENS["light"]["canvas"], "#f3f1f6"); self.assertEqual(theme.TOKENS["light"]["accent"], "#c97a98")
    def test_generated_page_has_both_themes_and_toggle(self):
        h = (ROOT / "site/index.html").read_text(encoding="utf-8")
        self.assertIn("prefers-color-scheme:dark", h); self.assertIn(".ilg-case[data-theme=dark]", h)
        self.assertIn(":not([data-theme=light])", h)
        self.assertIn('<button type="button" class="ilg-theme-toggle" aria-pressed="false" hidden>', h)
        self.assertIn("localStorage", h); self.assertNotIn("http", h.split("<main>")[0].replace("http://www.w3.org", ""))
        css = re.search(r"<style>(.*?)</style>", h, re.S).group(1); rest = css[len(theme.css(".ilg-case")):]
        self.assertEqual(re.findall(r"#[0-9a-fA-F]{3,6}\b", rest), [], "page colours must come from theme tokens")



class Readme(unittest.TestCase):
    def test_readme_commands_block_in_sync(self):
        import json
        p = json.loads((ROOT / "site/project.json").read_text(encoding="utf-8")); t = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(export_site.render_readme_block(p), t)
if __name__ == "__main__": unittest.main()
