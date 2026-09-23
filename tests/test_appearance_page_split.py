import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "docs" / "pages"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"
SITEMAP = ROOT / "docs" / "sitemap.xml"


class AppearancePageSplitTests(unittest.TestCase):
    def test_character_create_is_the_parent_page(self):
        html = (PAGES / "character-create.html").read_text(encoding="utf-8")
        self.assertIn("<h1>キャラクタークリエイト</h1>", html)
        self.assertIn("最初に決める項目", html)
        self.assertIn("ヘアスタイル・コスチューム・アクセサリー", html)
        for href in (
            "/PSNOVA/pages/appearance/hairstyle.html",
            "/PSNOVA/pages/appearance/costume.html",
            "/PSNOVA/pages/appearance/accessory.html",
        ):
            with self.subTest(href=href):
                self.assertIn(f'href="{href}"', html)

        self.assertFalse((PAGES / "appearance.html").exists())

        for path in (
            PAGES / "appearance" / "hairstyle.html",
            PAGES / "appearance" / "costume.html",
            PAGES / "appearance" / "accessory.html",
        ):
            with self.subTest(path=path):
                child = path.read_text(encoding="utf-8")
                self.assertIn("キャラクタークリエイトを参照。", child)
                self.assertNotIn(
                    '<a href="/PSNOVA/pages/character-create.html">キャラクタークリエイト</a>',
                    child,
                )

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

    def test_sidebar_uses_character_create_as_parent(self):
        sidebar = SIDEBAR.read_text(encoding="utf-8")
        self.assertIn('class="has-submenu appearance-data-item"', sidebar)
        self.assertIn(
            'class="appearance-data-link" href="/PSNOVA/pages/character-create.html">キャラクタークリエイト</a>',
            sidebar,
        )
        self.assertIn('class="weapon-submenu appearance-submenu"', sidebar)
        for href in (
            "/PSNOVA/pages/appearance/hairstyle.html",
            "/PSNOVA/pages/appearance/costume.html",
            "/PSNOVA/pages/appearance/accessory.html",
        ):
            with self.subTest(href=href):
                self.assertIn(f'href="{href}"', sidebar)
        self.assertIn("var appearanceChild =", sidebar)
        self.assertIn(
            'var appearanceParentCurrent = appearanceChild && linkPath === "/PSNOVA/pages/character-create.html";',
            sidebar,
        )
        self.assertNotIn('href="/PSNOVA/pages/appearance.html"', sidebar)

    def test_sitemap_uses_character_create_parent(self):
        xml = SITEMAP.read_text(encoding="utf-8")
        self.assertIn(
            "https://kylekatann.github.io/PSNOVA/pages/character-create.html",
            xml,
        )
        self.assertNotIn(
            "https://kylekatann.github.io/PSNOVA/pages/appearance.html",
            xml,
        )
        for path in (
            "appearance/hairstyle.html",
            "appearance/costume.html",
            "appearance/accessory.html",
        ):
            with self.subTest(path=path):
                self.assertIn(f"https://kylekatann.github.io/PSNOVA/pages/{path}", xml)


if __name__ == "__main__":
    unittest.main()
