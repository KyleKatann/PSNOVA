import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MENUBAR_JS = ROOT / "docs" / "js" / "menubar.js"
OPENCLOSE_JS = ROOT / "docs" / "js" / "openclose.js"
SIDEBAR_JS = ROOT / "docs" / "js" / "sidebar.js"
INTERACTION_CSS = ROOT / "docs" / "css" / "interaction.css"


class HeaderNavigationTests(unittest.TestCase):
    def test_legacy_top_navigation_links_are_removed(self):
        js = MENUBAR_JS.read_text(encoding="utf-8")
        self.assertNotIn("著作権表示", js)
        self.assertNotIn("修正・加筆要望", js)
        self.assertNotIn("<nav id=\"menubar\">", js)
        self.assertNotIn("<nav id=\"menubar-s\">", js)
        self.assertNotIn("function menu()", js)

    def test_header_button_falls_back_to_contents_drawer(self):
        js = OPENCLOSE_JS.read_text(encoding="utf-8")
        self.assertIn('menuId === "menubar-s"', js)
        self.assertIn('document.getElementById("sub")', js)
        self.assertIn('button.setAttribute("aria-controls", menu.id)', js)
        self.assertIn('"攻略メニューを開閉"', js)
        self.assertIn('document.body.classList.toggle("mobile-nav-open", open)', js)

    def test_mobile_contents_is_off_canvas_until_opened(self):
        css = INTERACTION_CSS.read_text(encoding="utf-8")
        self.assertIn("#sub.is-open", css)
        self.assertIn("transform: translateX(105%);", css)
        self.assertIn("transform: translateX(0);", css)
        self.assertIn("#mobile-nav-backdrop.is-open", css)
        self.assertIn("body.mobile-nav-open .nav-fix-pos-pagetop a", css)

    def test_sidebar_uses_compact_japanese_title_without_duplicate_trophy_group(self):
        js = SIDEBAR_JS.read_text(encoding="utf-8")
        self.assertIn("<h2>攻略メニュー</h2>", js)
        self.assertNotIn("<h2>Contents</h2>", js)
        self.assertNotIn("<li><p>トロフィー</p></li>", js)
        self.assertEqual(js.count('>トロフィー</a>'), 1)
        self.assertNotIn("prioritizeMainOnMobile", js)


if __name__ == "__main__":
    unittest.main()
