import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS_DIR = ROOT / "docs" / "css"
STYLE_CSS = CSS_DIR / "style.css"


class LegacyCssCleanupTests(unittest.TestCase):
    def test_public_css_inventory_is_two_bundles_without_import_chain(self):
        names = {path.name for path in CSS_DIR.glob("*.css")}
        self.assertEqual(
            names,
            {
                "style.css",
                "page.css",
            },
        )

        for path in CSS_DIR.glob("*.css"):
            with self.subTest(path=path.name):
                self.assertNotIn("@import", path.read_text(encoding="utf-8"))

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

    def test_internal_jpeg_suppression_is_not_owned_by_css(self):
        css = STYLE_CSS.read_text(encoding="utf-8")

        self.assertNotIn('body:not(.homepage) #main img[src$=".jpg"]', css)
        self.assertNotIn('body:not(.homepage) #main img[src$=".jpeg"]', css)
        self.assertNotIn("Legacy large screenshots remain", css)


if __name__ == "__main__":
    unittest.main()
