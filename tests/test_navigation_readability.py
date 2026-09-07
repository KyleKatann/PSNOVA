from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "docs" / "css" / "style.css"


class NavigationReadabilityTests(unittest.TestCase):
    def test_navigation_font_size_baseline_is_not_undersized(self):
        css = STYLE.read_text(encoding="utf-8")

        self.assertIn("nav#menubar ul li a {", css)
        self.assertIn("#menubar-s a {", css)
        self.assertIn("font-size: 16px;", css)
        self.assertIn("#sub .submenu a {", css)
        self.assertIn("font-size: 14px;", css)
        self.assertIn("#sub .submenu .weapon-submenu a {", css)
        self.assertIn("font-size: 13px;", css)
        self.assertIn("#sub .submenu p {", css)
        self.assertIn("font-size: 12px;", css)


if __name__ == "__main__":
    unittest.main()
