import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "docs" / "pages"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"
SITEMAP = ROOT / "docs" / "sitemap.xml"


class TipsPageSplitTests(unittest.TestCase):
    def test_parent_page_links_three_categories(self):
        html = (PAGES / "tips-bugs.html").read_text(encoding="utf-8")
        self.assertIn("<h1>小技・小ネタ・バグ</h1>", html)
        for href in (
            "/PSNOVA/pages/tips.html",
            "/PSNOVA/pages/trivia.html",
            "/PSNOVA/pages/bugs.html",
        ):
            with self.subTest(href=href):
                self.assertIn(f'href="{href}"', html)

    def test_content_is_split_by_category(self):
        tips = (PAGES / "tips.html").read_text(encoding="utf-8")
        trivia = (PAGES / "trivia.html").read_text(encoding="utf-8")
        bugs = (PAGES / "bugs.html").read_text(encoding="utf-8")
        pso2 = (PAGES / "pso2.html").read_text(encoding="utf-8")

        self.assertIn("イベントスキップ", tips)
        self.assertNotIn("イズナの格言集", tips)
        self.assertNotIn("修正済みの不具合", tips)

        self.assertIn("イズナの格言集", trivia)
        self.assertNotIn("イベントスキップ", trivia)
        self.assertNotIn("修正済みの不具合", trivia)
        self.assertNotIn("PSO2との時系列関係", trivia)

        self.assertIn("PSO2との時系列関係", pso2)
        self.assertIn("A.P.(238/2/20) EP1開始", pso2)
        self.assertIn("A.P.(239/1/7) EP3開始", pso2)

        self.assertIn("修正済みの不具合", bugs)
        self.assertNotIn("イベントスキップ", bugs)
        self.assertNotIn("イズナの格言集", bugs)

    def test_sidebar_uses_parent_and_three_children(self):
        sidebar = SIDEBAR.read_text(encoding="utf-8")
        self.assertIn('class="has-submenu tips-data-item"', sidebar)
        self.assertIn(
            'class="tips-data-link" href="/PSNOVA/pages/tips-bugs.html">小技・小ネタ・バグ</a>',
            sidebar,
        )
        self.assertIn('class="weapon-submenu tips-submenu"', sidebar)
        for href in (
            "/PSNOVA/pages/tips.html",
            "/PSNOVA/pages/trivia.html",
            "/PSNOVA/pages/bugs.html",
        ):
            with self.subTest(href=href):
                self.assertIn(f'href="{href}"', sidebar)
        self.assertIn("var tipsChild =", sidebar)
        self.assertIn(
            'var tipsParentCurrent = tipsChild && linkPath === "/PSNOVA/pages/tips-bugs.html";',
            sidebar,
        )

    def test_sitemap_contains_parent_and_children(self):
        xml = SITEMAP.read_text(encoding="utf-8")
        for path in ("tips-bugs.html", "tips.html", "trivia.html", "bugs.html"):
            with self.subTest(path=path):
                self.assertIn(f"https://kylekatann.github.io/PSNOVA/pages/{path}", xml)


if __name__ == "__main__":
    unittest.main()
