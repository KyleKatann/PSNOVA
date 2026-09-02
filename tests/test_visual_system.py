import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "docs" / "css" / "style.css"
SIDEBAR_JS = ROOT / "docs" / "js" / "sidebar.js"


class VisualSystemTests(unittest.TestCase):
    def test_color_pattern_uses_psnova_specific_cool_palette(self):
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn("--nav-bg: #252d3a;", css)
        self.assertIn("--accent: #5661c9;", css)
        self.assertIn("--accent-soft: #eceefe;", css)
        self.assertIn("--link: #2f68a8;", css)
        self.assertNotIn("#ffcc00", css.lower())
        self.assertNotIn("#ffc400", css.lower())
        self.assertNotIn("#ffbf00", css.lower())

    def test_information_hierarchy_has_dark_nav_white_content_and_accent_states(self):
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn("background: var(--nav-bg);", css)
        self.assertIn("#main {", css)
        self.assertIn("background: var(--surface);", css)
        self.assertIn("border-left: 5px solid var(--accent);", css)
        self.assertIn("#sub .submenu a.is-current", css)
        self.assertIn("background: var(--accent-soft);", css)

    def test_sidebar_marks_current_page_semantically(self):
        js = SIDEBAR_JS.read_text(encoding="utf-8")
        self.assertIn("function markCurrentSidebarLink", js)
        self.assertIn('classList.toggle("is-current", exactCurrent)', js)
        self.assertIn('classList.toggle("is-parent-current", weaponParentCurrent)', js)
        self.assertIn('setAttribute("aria-current", "page")', js)


if __name__ == "__main__":
    unittest.main()
