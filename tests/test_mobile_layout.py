import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SIDEBAR_JS = ROOT / "docs" / "js" / "sidebar.js"


class MobileLayoutTests(unittest.TestCase):
    def test_mobile_layout_prioritizes_main_content(self):
        js = SIDEBAR_JS.read_text(encoding="utf-8")
        self.assertIn('window.matchMedia("(max-width: 800px)")', js)
        self.assertIn('contents.insertBefore(main, sub);', js)
        self.assertIn('window.addEventListener("DOMContentLoaded", prioritizeMainOnMobile', js)
        self.assertIn('window.addEventListener("resize", prioritizeMainOnMobile', js)


if __name__ == "__main__":
    unittest.main()
