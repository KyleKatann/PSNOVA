import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "docs" / "pages"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"
SITEMAP = ROOT / "docs" / "sitemap.xml"


class AppearancePageSplitTests(unittest.TestCase):
    def test_parent_page_links_to_three_detail_pages(self):
        html = (PAGES / "appearance.html").read_text(encoding="utf-8")
        for href in (
            "/PSNOVA/pages/appearance/hairstyle.html",
            "/PSNOVA/pages/appearance/costume.html",
            "/PSNOVA/pages/appearance/accessory.html",
        ):
            with self.subTest(href=href):
                self.assertIn(f'href="{href}"', html)

    def test_content_is_split_by_category(self):
        hairstyle = (PAGES / "appearance" / "hairstyle.html").read_text(encoding="utf-8")
        costume = (PAGES / "appearance" / "costume.html").read_text(encoding="utf-8")
        accessory = (PAGES / "appearance" / "accessory.html").read_text(encoding="utf-8")

        self.assertIn("ミディアムレイヤー", hairstyle)
        self.assertNotIn("クローズクォーター", hairstyle)
        self.assertNotIn("ゴーグル", hairstyle)

        self.assertIn("クローズクォーター", costume)
        self.assertIn("ディスタ・シリーズ", costume)
        self.assertNotIn("ミディアムレイヤー", costume)
        self.assertNotIn("ゴーグル", costume)

        self.assertIn("ゴーグル", accessory)
        self.assertNotIn("ミディアムレイヤー", accessory)
        self.assertNotIn("クローズクォーター", accessory)

    def test_sidebar_uses_parent_child_navigation(self):
        sidebar = SIDEBAR.read_text(encoding="utf-8")
        self.assertIn('class="has-submenu appearance-data-item"', sidebar)
        self.assertIn('class="appearance-data-link" href="/PSNOVA/pages/appearance.html"', sidebar)
        self.assertIn('class="weapon-submenu appearance-submenu"', sidebar)
        for href in (
            "/PSNOVA/pages/appearance/hairstyle.html",
            "/PSNOVA/pages/appearance/costume.html",
            "/PSNOVA/pages/appearance/accessory.html",
        ):
            with self.subTest(href=href):
                self.assertIn(f'href="{href}"', sidebar)
        self.assertIn("var appearanceChild =", sidebar)
        self.assertIn("appearanceParentCurrent", sidebar)

    def test_sitemap_contains_split_pages(self):
        xml = SITEMAP.read_text(encoding="utf-8")
        for path in (
            "appearance/hairstyle.html",
            "appearance/costume.html",
            "appearance/accessory.html",
        ):
            with self.subTest(path=path):
                self.assertIn(f"https://kylekatann.github.io/PSNOVA/pages/{path}", xml)


if __name__ == "__main__":
    unittest.main()
