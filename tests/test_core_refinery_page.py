import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "pages" / "core-refinery.html"
BASE = ROOT / "docs" / "pages" / "base.html"
TRAITS = ROOT / "docs" / "pages" / "traits.html"
SHARON = ROOT / "docs" / "pages" / "promise-order" / "sharon.html"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"
SITEMAP = ROOT / "docs" / "sitemap.xml"


class CoreRefineryPageTests(unittest.TestCase):
    def page_html(self):
        return PAGE.read_text(encoding="utf-8")

    def test_page_is_reader_facing(self):
        html = self.page_html()

        self.assertIn("<h1>コア精錬所</h1>", html)
        self.assertIn("最大5人のクルーを配属できます", html)
        self.assertIn("特殊能力の強化レシピを増やす「精錬所チーフ」", html)



    def test_reducer_values_and_holders(self):
        html = self.page_html()

        expected = (
            ("コア工作士", "-5%", "ブラック、ヒーベスト、キャサリン、ルーティ、ラティス"),
            ("コア鋳造士", "-10%", "ディーヴァス、ターシャ、ティセリア"),
            ("コア精錬士", "-20%", "クシード、ヴァルメン"),
        )
        for name, effect, crew in expected:
            with self.subTest(name=name):
                self.assertIn(f"<td>{name}</td><td>{effect}</td><td>{crew}</td>", html)

    def test_max_reduction_and_chief_can_coexist(self):
        html = self.page_html()

        self.assertIn("消費グランエナジーを70%軽減", html)
        self.assertIn("実際に支払う量は30%", html)
        self.assertIn("<tr><td>ディーヴァス</td><td>コア鋳造士 + 精錬所チーフ</td><td>-10%</td></tr>", html)
        self.assertIn("最大70%軽減と機能拡張を同時に有効化できます", html)

    def test_chief_expands_upgrade_recipes(self):
        html = self.page_html()

        self.assertIn("コア特殊能力強化で利用できる強化レシピが増えます", html)

    def test_chief_holders(self):
        html = self.page_html()

        self.assertIn("<tr><td>ディーヴァス</td><td>コア鋳造士 (-10%)</td></tr>", html)
        self.assertIn("<tr><td>ルーティ</td><td>コア工作士 (-5%)</td></tr>", html)
        self.assertIn("<tr><td>リューフィ</td><td>-</td></tr>", html)
        self.assertNotIn("<h2>精錬所チーフの所持者</h2>", html)

    def test_all_core_evolve_recipes_are_published(self):
        html = self.page_html()
        start = html.index("<h2>全強化レシピ</h2>")
        end = html.index("<h2>解放条件</h2>", start)
        section = html[start:end]

        rows = re.findall(
            r"<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>",
            section,
        )

        self.assertEqual(331, len(rows))
        self.assertEqual(242, sum(normal != "-" for _, normal, _ in rows))
        self.assertTrue(all(chief != "-" for _, _, chief in rows))
        self.assertEqual(
            89,
            sum(normal == "-" and chief != "-" for _, normal, chief in rows),
        )
        self.assertEqual(
            56,
            sum(
                normal != "-" and normal != chief
                for _, normal, chief in rows
            ),
        )

        self.assertIn(
            ("パワーⅠ", "×3：パワーⅡ", "×3：パワーⅡ"),
            rows,
        )
        self.assertIn(
            ("パワーⅤ", "×5：シュートⅤ", "×3：パワーⅥ"),
            rows,
        )
        self.assertIn(
            ("パワーⅥ", "-", "×5：シュートⅥ"),
            rows,
        )
        self.assertIn(
            ("対グラン中毒", "-", "×5：ハイパーバースト"),
            rows,
        )

    def test_unlock_promise(self):
        html = self.page_html()

        self.assertIn("シャロンの約束「コア精錬研究」", html)
        self.assertIn("グランピース(雷属性)」99個", html)
        self.assertIn("グランピース(光属性)」99個", html)

    def test_existing_pages_are_corrected(self):
        base = BASE.read_text(encoding="utf-8")
        traits = TRAITS.read_text(encoding="utf-8")
        sharon = SHARON.read_text(encoding="utf-8")

        self.assertIn('<a href="/PSNOVA/pages/core-refinery.html">コア精錬所 Lv.5</a></td><td>4×4</td>', base)
        self.assertNotIn("コア精錬所 Lv.5</td><td>4×3</td>", base)

        self.assertIn("<tr><td>コア精錬士</td><td>精錬所エナジー減 -20%</td><td>コア精錬所</td></tr>", traits)
        self.assertNotIn("製錬所エナジー減", traits)
        self.assertNotIn("コア精錬士</td><td>精錬所エナジー減 -15%", traits)
        self.assertIn("精錬所チーフでコア特殊能力強化の強化レシピを拡張", base)

        self.assertIn("施設「コア精錬所」追加", sharon)
        self.assertNotIn("施設「コア製錬所」追加", sharon)

    def test_links_are_present(self):
        path = "/PSNOVA/pages/core-refinery.html"
        sidebar = SIDEBAR.read_text(encoding="utf-8")
        sitemap = SITEMAP.read_text(encoding="utf-8")

        self.assertIn(f'<li><a href="{path}">コア精錬所</a></li>', sidebar)
        self.assertIn(f'currentPath === "{path}"', sidebar)
        self.assertIn(f"https://kylekatann.github.io{path}", sitemap)

    def test_tables_have_captions(self):
        html = self.page_html()

        self.assertEqual(html.count("<caption>"), 4)
        self.assertNotIn("<caption>コア精錬所の施設情報</caption>", html)
        self.assertIn("<caption>消費グランエナジーを軽減する特徴と所持クルー</caption>", html)
        self.assertIn("<caption>最大70%軽減を実現する配属例</caption>", html)
        self.assertIn("<caption>精錬所チーフを持つクルー</caption>", html)
        self.assertIn("<caption>コア特殊能力強化の全レシピ</caption>", html)

    def test_public_metadata(self):
        html = self.page_html()

        self.assertIn("<title>PSNOVA攻略サイト - コア精錬所</title>", html)
        self.assertIn(
            '<link rel="canonical" href="https://kylekatann.github.io/PSNOVA/pages/core-refinery.html">',
            html,
        )


if __name__ == "__main__":
    unittest.main()
