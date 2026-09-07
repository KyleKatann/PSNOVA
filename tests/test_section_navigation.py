import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE_ENTRY = ROOT / "docs" / "css" / "style.css"
MENUBAR_JS = ROOT / "docs" / "js" / "menubar.js"
SECTION_NAV_JS = ROOT / "docs" / "js" / "section-nav.js"
SECTION_NAV_CSS = ROOT / "docs" / "css" / "section-nav.css"


class SectionNavigationTests(unittest.TestCase):
    def test_automatic_section_navigation_assets_stay_removed(self):
        js = MENUBAR_JS.read_text(encoding="utf-8")
        css = STYLE_ENTRY.read_text(encoding="utf-8")
        self.assertNotIn("section-nav.js", js)
        self.assertNotIn("section-nav.css", css)
        self.assertFalse(SECTION_NAV_JS.exists())
        self.assertFalse(SECTION_NAV_CSS.exists())


if __name__ == "__main__":
    unittest.main()
