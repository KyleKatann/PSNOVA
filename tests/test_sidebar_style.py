import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "docs" / "css" / "style.css"


class SidebarStyleTests(unittest.TestCase):
    def test_sidebar_is_clean_secondary_navigation(self):
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn("#sub nav {", css)
        self.assertIn("position: sticky;", css)
        self.assertIn("#sub .submenu {", css)
        self.assertIn("background: var(--surface);", css)
        self.assertIn("#sub .submenu a:hover", css)
        self.assertIn("background: var(--surface-hover);", css)

    def test_mobile_base_layout_prioritizes_main_content(self):
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn("#main {\n        width: 100%;\n        order: 1;", css)
        self.assertIn("#sub {\n        width: 100%;\n        flex-basis: auto;\n        order: 2;", css)
        self.assertIn("border-top: 0;", css)
        self.assertIn("#sub nav {\n        position: static;", css)


if __name__ == "__main__":
    unittest.main()
