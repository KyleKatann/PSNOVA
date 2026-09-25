import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "pages" / "gran-burst.html"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"
SITEMAP = ROOT / "docs" / "sitemap.xml"


class GranBurstPageTests(unittest.TestCase):
    def page_html(self):
        return PAGE.read_text(encoding="utf-8")

    def test_page_explains_mechanics_without_exposing_internal_values(self):
        html = self.page_html()

        self.assertIn("<h1>グランバーストの仕組み</h1>", html)
        self.assertIn("チェインが高いほどゲージが増えやすい", html)
        self.assertIn(
            "攻撃を当ててチェインを伸ばすほど、その後の攻撃でグランバーストゲージが増えやすくなります",
            html,
        )
        self.assertIn(
            "攻撃力、実際に与えたダメージ、弱点への命中、属性弱点、クリティカルの有無では増えません",
            html,
        )
        self.assertIn(
            "グランアーツは技ごとにグランバーストゲージの伸びやすさが異なります",
            html,
        )

        for removed_value in (
            "100～139",
            "140以上",
            "139回で99.0",
            "140回目で100.1",
            ">2.32<",
            ">2.01<",
            ">1.79<",
            ">1.34<",
            ">1.02<",
            ">1.00<",
            ">0.55<",
        ):
            with self.subTest(removed_value=removed_value):
                self.assertNotIn(removed_value, html)

    def test_normal_attack_table_only_presents_hit_count_data(self):
        html = self.page_html()

        self.assertIn("ツインマシンガンは4回・4回・5回の合計13ヒット", html)
        self.assertIn(
            "<tr><td>ツインマシンガン</td><td>4</td><td>4</td><td>5</td><td>13</td></tr>",
            html,
        )
        self.assertIn(
            "通常攻撃だけでゲージをためる用途では、ツインマシンガンが最有力です",
            html,
        )
        self.assertIn(
            "見た目のヒット数すべてが個別のゲージ加算になるとは限りません",
            html,
        )

    def test_all_weapon_types_are_present_and_ga_weapons_show_the_highest_gauge_pa(self):
        html = self.page_html()

        expected = (
            ("ソード", "オーバーエンド"),
            ("パルチザン", "オーバースライサー"),
            ("ダブルセイバー", "イリュージョンレイヴ"),
            ("ナックル", "ヘルクラッシュ"),
            ("アサルトライフル", "リフレクトイージス"),
            ("ツインマシンガン", "エルダーリベリオン"),
            ("ロッド", "なし（テクニック）"),
            ("タリス", "なし（テクニック）"),
            ("ウォンド", "なし（テクニック）"),
            ("ヘイロウ", "レゾナンスキャノン"),
            ("パイル", "パイルストーム"),
        )
        for weapon, pa in expected:
            with self.subTest(weapon=weapon):
                self.assertIn(f"<tr><td>{weapon}</td><td>{pa}</td></tr>", html)

        self.assertIn(
            "<caption>全武器種のグランアーツ確認表</caption>",
            html,
        )
        self.assertIn("全11武器種を下表にまとめ", html)
        self.assertIn("ロッド、タリス、ウォンドにはグランアーツがなく、テクニックを使用します", html)
        self.assertNotIn("<th scope=\"col\">倍率</th>", html)
        self.assertNotIn("ゲージ倍率の高い", html)
        self.assertNotIn("ゲージ補正が最も高い", html)

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
