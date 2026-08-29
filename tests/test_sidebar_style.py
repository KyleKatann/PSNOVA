import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODERN_CSS = ROOT / "docs" / "css" / "modern.css"

class SidebarStyleTests(unittest.TestCase):
    def test_sidebar_is_clean_secondary_navigation(self):
        css = MODERN_CSS.read_text(encoding="utf-8")
        self.assertIn("#sub nav {", css)
        self.assertIn("position: sticky;", css)
        self.assertIn("#sub .submenu {", css)
        self.assertIn("background: var(--surface);", css)
        self.assertIn("#sub .submenu a:hover", css)
        self.assertIn("background: var(--surface-muted);", css)

    def test_sidebar_returns_to_normal_flow_on_mobile(self):
        css = MODERN_CSS.read_text(encoding="utf-8")
        self.assertIn("#sub nav {\n        position: static;", css)
        self.assertIn("border-top: 1px solid var(--border);", css)

if __name__ == "__main__":
    unittest.main()
