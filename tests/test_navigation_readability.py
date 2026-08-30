from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "docs" / "css" / "style.css"
AGENT = ROOT / "Agent.md"


class NavigationReadabilityTests(unittest.TestCase):
    def test_navigation_font_size_baseline_is_not_undersized(self):
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn('nav#menubar ul li a,\n#menubar-s a {\n    font-size: 16px;', css)
        self.assertIn('#sub .submenu a {\n    font-size: 14px;', css)
        self.assertIn('#sub .submenu .weapon-submenu a {\n    font-size: 13px;', css)
        self.assertIn('#sub .submenu p {\n    font-size: 12px;', css)

    def test_navigation_readability_rule_is_recorded(self):
        guide = AGENT.read_text(encoding="utf-8")
        self.assertIn('16px for the top/mobile navigation', guide)
        self.assertIn('14px for primary sidebar links', guide)
        self.assertIn('13px for nested weapon links', guide)


if __name__ == "__main__":
    unittest.main()
