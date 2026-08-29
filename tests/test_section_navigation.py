import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENUBAR_JS = ROOT / "docs" / "js" / "menubar.js"
SECTION_NAV_JS = ROOT / "docs" / "js" / "section-nav.js"
SECTION_NAV_CSS = ROOT / "docs" / "css" / "section-nav.css"

class SectionNavigationTests(unittest.TestCase):
    def test_section_navigation_assets_are_loaded(self):
        js = MENUBAR_JS.read_text(encoding="utf-8")
        self.assertIn("/PSNOVA/js/section-nav.js", js)
        self.assertIn("/PSNOVA/css/section-nav.css", js)

    def test_navigation_is_generated_from_existing_headings(self):
        js = SECTION_NAV_JS.read_text(encoding="utf-8")
        self.assertIn('querySelectorAll("h3, details > summary")', js)
        self.assertIn('aria-label", "ページ内目次"', js)
        self.assertIn('href="#', js)
        self.assertIn("items.length < 3", js)

    def test_section_navigation_wraps_on_narrow_screens(self):
        css = SECTION_NAV_CSS.read_text(encoding="utf-8")
        self.assertIn("flex-wrap: wrap", css)
        self.assertIn("@media screen and (max-width: 560px)", css)

if __name__ == "__main__":
    unittest.main()
