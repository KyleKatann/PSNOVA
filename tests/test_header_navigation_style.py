import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODERN_CSS = ROOT / "docs" / "css" / "modern.css"


class HeaderNavigationStyleTests(unittest.TestCase):
    def test_desktop_navigation_uses_strong_contrast_bar(self):
        css = MODERN_CSS.read_text(encoding="utf-8")
        self.assertIn("nav#menubar {", css)
        self.assertIn("background: var(--nav-bg);", css)
        self.assertIn("border: 1px solid var(--nav-bg-strong);", css)
        self.assertIn("nav#menubar ul {", css)
        self.assertIn("display: flex;", css)
        self.assertIn("height: auto;", css)

    def test_navigation_links_have_clear_touch_and_active_affordance(self):
        css = MODERN_CSS.read_text(encoding="utf-8")
        self.assertIn("padding: 13px 18px 12px;", css)
        self.assertIn("border-bottom: 3px solid transparent;", css)
        self.assertIn("border-bottom-color: var(--accent);", css)

    def test_legacy_fixed_navigation_dimensions_are_overridden(self):
        css = MODERN_CSS.read_text(encoding="utf-8")
        self.assertIn("float: none;", css)
        self.assertIn("width: auto;", css)

    def test_mobile_navigation_has_readable_touch_targets(self):
        css = MODERN_CSS.read_text(encoding="utf-8")
        self.assertIn("#menubar-s a {", css)
        self.assertIn("padding: 12px 14px;", css)
        self.assertIn("#menubar-s li + li", css)


if __name__ == "__main__":
    unittest.main()
