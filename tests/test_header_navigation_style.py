import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MENUBAR_JS = ROOT / "docs" / "js" / "menubar.js"
OPENCLOSE_JS = ROOT / "docs" / "js" / "openclose.js"


class HeaderNavigationTests(unittest.TestCase):
    def test_legacy_top_navigation_links_are_removed(self):
        js = MENUBAR_JS.read_text(encoding="utf-8")
        self.assertNotIn("著作権表示", js)
        self.assertNotIn("修正・加筆要望", js)
        self.assertNotIn("<nav id=\"menubar\">", js)
        self.assertNotIn("<nav id=\"menubar-s\">", js)
        self.assertIn("function menu() {}", js)

    def test_orphaned_mobile_menu_button_is_hidden(self):
        js = OPENCLOSE_JS.read_text(encoding="utf-8")
        self.assertIn("if (!menu)", js)
        self.assertIn("button.hidden = true;", js)
        self.assertIn('button.setAttribute("aria-hidden", "true");', js)


if __name__ == "__main__":
    unittest.main()
