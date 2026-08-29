import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODERN_CSS = ROOT / "docs" / "css" / "modern.css"


class HeaderNavigationStyleTests(unittest.TestCase):
    def test_desktop_navigation_is_flat_flexible_layout(self):
        css = MODERN_CSS.read_text(encoding="utf-8")
        self.assertIn("nav#menubar ul {", css)
        self.assertIn("display: flex;", css)
        self.assertIn("box-shadow: none;", css)
        self.assertIn("background: var(--surface);", css)
        self.assertIn("border: 1px solid var(--border);", css)

    def test_legacy_fixed_navigation_dimensions_are_overridden(self):
        css = MODERN_CSS.read_text(encoding="utf-8")
        self.assertIn("height: auto;", css)
        self.assertIn("float: none;", css)
        self.assertIn("width: auto;", css)

    def test_mobile_navigation_has_readable_touch_targets(self):
        css = MODERN_CSS.read_text(encoding="utf-8")
        self.assertIn("#menubar-s a {", css)
        self.assertIn("padding: 12px 14px;", css)
        self.assertIn("#menubar-s li + li", css)


if __name__ == "__main__":
    unittest.main()
