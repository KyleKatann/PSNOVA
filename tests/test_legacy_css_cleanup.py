import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE_CSS = ROOT / "docs" / "css" / "style.css"


class LegacyCssCleanupTests(unittest.TestCase):
    def test_style_css_is_only_the_modern_entrypoint(self):
        css = STYLE_CSS.read_text(encoding="utf-8")
        for path in (
            "/PSNOVA/css/modern.css",
            "/PSNOVA/css/wiki-table.css",
            "/PSNOVA/css/interaction.css",
            "/PSNOVA/css/affiliate.css",
            "/PSNOVA/css/site-search.css",
            "/PSNOVA/css/section-nav.css",
            "/PSNOVA/css/weapon-tools.css",
        ):
            with self.subTest(path=path):
                self.assertIn(path, css)

    def test_legacy_template_rules_do_not_return(self):
        css = STYLE_CSS.read_text(encoding="utf-8")
        for legacy in (
            "Template-Party",
            "linear-gradient(#FFF, #e5e5e5)",
            "font-family: Arial, sans-serif",
            "box-shadow: 1px 2px 5px",
            "max-width: 200%",
        ):
            with self.subTest(legacy=legacy):
                self.assertNotIn(legacy, css)

    def test_internal_legacy_jpegs_are_hidden_before_javascript_runs(self):
        css = STYLE_CSS.read_text(encoding="utf-8")
        self.assertIn('#main img[src$=".jpg"]', css)
        self.assertIn('/img/gigantes/gigantes.jpg', css)
        self.assertIn('display: none !important;', css)


if __name__ == "__main__":
    unittest.main()
