import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PAGES = DOCS / "pages"
SIDEBAR = DOCS / "js" / "sidebar.js"
SITEMAP = DOCS / "sitemap.xml"


class TipsContentRedistributionTests(unittest.TestCase):
    def test_old_tips_pages_are_removed(self):
        for path in ("tips-bugs.html", "tips.html", "trivia.html"):
            with self.subTest(path=path):
                self.assertFalse((PAGES / path).exists())

    def test_tips_content_is_redistributed(self):
        walkthrough = (PAGES / "walkthrough.html").read_text(encoding="utf-8")
        classes = (PAGES / "class.html").read_text(encoding="utf-8")
        specialability = (PAGES / "specialability.html").read_text(encoding="utf-8")
        gigantes = (PAGES / "gigantes.html").read_text(encoding="utf-8")
        npc = (PAGES / "npc.html").read_text(encoding="utf-8")
        costume = (PAGES / "appearance" / "costume.html").read_text(encoding="utf-8")

        for text in ("イベント操作", "【SELECT】ボタン", "テキストウィンドウを非表示"):
            with self.subTest(page="walkthrough", text=text):
                self.assertIn(text, walkthrough)

        for text in ("移動テクニック", "ストレイト", "ランブリングムーン"):
            with self.subTest(page="class", text=text):
                self.assertIn(text, classes)

        for text in ("<h2>状態異常</h2>", "グラン中毒", "インフェクション"):
            with self.subTest(page="specialability", text=text):
                self.assertIn(text, specialability)

        for text in (
            "各部位への有効攻撃",
            "装甲には打撃",
            "居眠りギガンテス",
        ):
            with self.subTest(page="gigantes", text=text):
                self.assertIn(text, gigantes)

        for text in (
            "友好度によるクエストクリア報酬への影響",
            "親友3人で経験値28500/グラン9345",
            "NPCとの会話",
            "ユノの宝石に書かれている文字",
            "イズナの格言集",
        ):
            with self.subTest(page="npc", text=text):
                self.assertIn(text, npc)

        self.assertIn("カラー変更に関する特殊な挙動", costume)
        self.assertIn("名称末尾に「◆」が付くDLCアイテム", costume)

    def test_pso2_timeline_remains_on_pso2_page(self):
        pso2 = (PAGES / "pso2.html").read_text(encoding="utf-8")
        self.assertIn("PSO2との時系列関係", pso2)
        self.assertIn("A.P.(238/2/20) EP1開始", pso2)
        self.assertIn("A.P.(239/1/7) EP3開始", pso2)

    def test_bugs_remains_as_standalone_page(self):
        bugs = (PAGES / "bugs.html").read_text(encoding="utf-8")
        self.assertIn("<h1>バグ</h1>", bugs)
        self.assertIn("修正済みの不具合", bugs)

    def test_sidebar_links_directly_to_bugs(self):
        sidebar = SIDEBAR.read_text(encoding="utf-8")
        self.assertIn(
            '<a href="/PSNOVA/pages/bugs.html">バグ・不具合</a>',
            sidebar,
        )
        for text in (
            "/PSNOVA/pages/tips-bugs.html",
            "/PSNOVA/pages/tips.html",
            "/PSNOVA/pages/trivia.html",
            "tips-data-item",
            "tips-data-link",
            "tips-submenu",
            "var tipsChild =",
            "var tipsParentCurrent =",
        ):
            with self.subTest(text=text):
                self.assertNotIn(text, sidebar)

    def test_sitemap_contains_only_bugs_page(self):
        xml = SITEMAP.read_text(encoding="utf-8")
        self.assertIn(
            "https://kylekatann.github.io/PSNOVA/pages/bugs.html",
            xml,
        )
        for path in ("tips-bugs.html", "tips.html", "trivia.html"):
            with self.subTest(path=path):
                self.assertNotIn(
                    f"https://kylekatann.github.io/PSNOVA/pages/{path}",
                    xml,
                )


if __name__ == "__main__":
    unittest.main()
