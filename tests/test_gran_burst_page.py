import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "pages" / "gran-burst.html"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"
SITEMAP = ROOT / "docs" / "sitemap.xml"


class GranBurstPageTests(unittest.TestCase):
    def page_html(self):
        return PAGE.read_text(encoding="utf-8")

    def test_page_explains_chain_and_normal_attack_behavior(self):
        html = self.page_html()

        self.assertIn("<h1>グランバーストの仕組み</h1>", html)
        self.assertIn("チェインが高いほどゲージが増えやすい", html)
        self.assertIn("<tr><td>100～139</td><td>1.0</td></tr>", html)
        self.assertIn("<tr><td>140以上</td><td>1.1</td></tr>", html)
        self.assertIn("139回で99.0、140回目で100.1", html)
        self.assertIn(
            "攻撃力、実際に与えたダメージ、弱点への命中、属性弱点、クリティカルの有無では増えません",
            html,
        )

    def test_twin_machinegun_is_presented_as_normal_attack_candidate(self):
        html = self.page_html()

        self.assertIn("ツインマシンガンは4回・4回・5回の合計13ヒット", html)
        self.assertIn(
            "<tr><td>ツインマシンガン</td><td>4</td><td>4</td><td>5</td><td>13</td></tr>",
            html,
        )
        self.assertIn("通常攻撃だけでゲージをためる用途では、ツインマシンガンが最有力です", html)
        self.assertIn("見た目のヒット数すべてが個別のゲージ加算になるとは限りません", html)

    def test_tmg_gran_arts_burst_multipliers_are_reader_facing(self):
        html = self.page_html()

        expected = (
            ("エルダーリベリオン", "2.32"),
            ("ダンシングスイープ", "2.01"),
            ("インフィニティファイア", "1.79"),
            ("リバースタップ", "1.34"),
            ("サテライトエイム", "1.02"),
            ("エリアルシューティング", "1.00"),
            ("バレットスコール", "0.55"),
        )
        for name, multiplier in expected:
            with self.subTest(name=name):
                self.assertIn(f"<tr><td>{name}</td><td>{multiplier}</td></tr>", html)

        self.assertIn("倍率だけで「最速の技」とは決まりません", html)

    def test_internal_analysis_information_is_not_exposed(self):
        html = self.page_html()

        for internal_term in (
            "FND-",
            "EVD-",
            "Pa.csv",
            "PileSettings",
            "ID522",
            "AttackBurstMultiplier",
            "category7",
            "code0x",
            "selector",
            "runtime",
            "native",
            "distinct contribution",
            "0x81",
        ):
            with self.subTest(internal_term=internal_term):
                self.assertNotIn(internal_term, html)

    def test_page_has_navigation_and_metadata(self):
        page_path = "/PSNOVA/pages/gran-burst.html"
        html = self.page_html()
        sidebar = SIDEBAR.read_text(encoding="utf-8")
        sitemap = SITEMAP.read_text(encoding="utf-8")

        self.assertIn("<title>PSNOVA攻略サイト - グランバーストの仕組み</title>", html)
        self.assertIn(
            '<link rel="canonical" href="https://kylekatann.github.io/PSNOVA/pages/gran-burst.html">',
            html,
        )
        self.assertIn(
            f'<li><a href="{page_path}">グランバーストの仕組み</a></li>',
            sidebar,
        )
        self.assertIn(f"https://kylekatann.github.io{page_path}", sitemap)


if __name__ == "__main__":
    unittest.main()
