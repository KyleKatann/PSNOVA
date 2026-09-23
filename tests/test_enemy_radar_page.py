import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "pages" / "enemy-radar.html"
BASE = ROOT / "docs" / "pages" / "base.html"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"
SITEMAP = ROOT / "docs" / "sitemap.xml"


class EnemyRadarPageTests(unittest.TestCase):
    def page_html(self):
        return PAGE.read_text(encoding="utf-8")

    def test_page_is_reader_facing(self):
        html = self.page_html()

        self.assertIn("<h1>エネミーレーダー</h1>", html)
        self.assertIn("レアエネミーとブーストエネミーを出やすくする拠点施設", html)
        self.assertIn("特徴「野生の勘」", html)

        for internal_term in (
            "909100",
            "ID516",
            "ID517",
            "499200",
            "GacyaNPC_Size",
            "Type13",
            "SP08_120_030_ed",
            "SP07_210_050_ed",
            "9050010",
            "9090090",
            "Pat_01_3",
            "PR_1320_orc",
        ):
            with self.subTest(internal_term=internal_term):
                self.assertNotIn(internal_term, html)


    def test_effect_tier_table_matches_audited_report(self):
        html = self.page_html()

        expected_rows = (
            ("0人", "+50%"),
            ("1人", "+75%"),
            ("2人", "+100%"),
            ("3人", "+200%"),
            ("4人", "+300%"),
            ("5人", "+600%"),
        )

        for row in expected_rows:
            fragment = "<tr>" + "".join(f"<td>{value}</td>" for value in row) + "</tr>"
            with self.subTest(row=row):
                self.assertIn(fragment, html)

    def test_public_effect_table_only_shows_requested_columns(self):
        html = self.page_html()

        self.assertIn("<th scope=\"col\">「野生の勘」人数</th>", html)
        self.assertIn("<th scope=\"col\">効果</th>", html)
        self.assertNotIn("<th scope=\"col\">出現率アップ</th>", html)
        self.assertNotIn("<th scope=\"col\">レアエネミー追加判定</th>", html)
        self.assertNotIn("<th scope=\"col\">内部計算</th>", html)
        self.assertNotIn("<th scope=\"col\">基礎3%時の実出現率</th>", html)

    def test_effect_explanations_are_reader_facing_and_non_numeric(self):
        html = self.page_html()

        self.assertIn("レアエネミーを出やすくする効果です", html)
        self.assertIn("ブーストエネミーを出やすくする効果です", html)
        self.assertIn("もともとレアエネミーにならない敵には効果がありません", html)
        self.assertIn("もともとブーストエネミーにならない敵には効果がありません", html)
        self.assertIn("最大まで強化しても確定ではない", html)
        for removed_detail in (
            "通常の出現判定とは別の判定",
            "元の発生率が設定されていない",
            "最大時の実効率",
            "×1.50～×7.00",
            "×2.50～×8.00",
            "3% × 8.00 = 24%",
            "20% × 7.00 = 140%相当",
            "基礎3%時の実出現率",
        ):
            with self.subTest(removed_detail=removed_detail):
                self.assertNotIn(removed_detail, html)

    def test_base_return_link_is_removed(self):
        html = self.page_html()

        self.assertNotIn("拠点施設一覧へ戻る", html)


    def test_trait_crew_list_is_complete(self):
        html = self.page_html()

        for name in (
            "ノヴァイア",
            "ノライク",
            "イーヴァス",
            "プリシュ",
            "セレネ",
            "アティ",
            "ファイム",
        ):
            with self.subTest(name=name):
                self.assertIn(f"<li>{name}</li>", html)

        section = html.split("<h2>「野生の勘」を持つクルー</h2>", 1)[1]
        section = section.split("</ul>", 1)[0]
        self.assertEqual(len(re.findall(r"<li>.*?</li>", section)), 7)

    def test_page_is_linked_from_base_sidebar_and_sitemap(self):
        path = "/PSNOVA/pages/enemy-radar.html"

        base = BASE.read_text(encoding="utf-8")
        sidebar = SIDEBAR.read_text(encoding="utf-8")
        sitemap = SITEMAP.read_text(encoding="utf-8")

        self.assertIn(f'href="{path}">エネミーレーダー Lv.1</a>', base)
        self.assertIn("レアエネミー・ブーストエネミーを出やすくする", base)
        self.assertIn("特徴【野生の勘】を持つクルーを配属すると、さらに出やすくなる", base)
        self.assertIn(f'<li><a href="{path}">エネミーレーダー</a></li>', sidebar)
        self.assertIn(f"https://kylekatann.github.io{path}", sitemap)

    def test_public_metadata_is_present(self):
        html = self.page_html()

        self.assertIn("<title>PSNOVA攻略サイト - エネミーレーダー</title>", html)
        self.assertIn(
            '<link rel="canonical" href="https://kylekatann.github.io/PSNOVA/pages/enemy-radar.html">',
            html,
        )
        head = html.split("</head>", 1)[0]
        self.assertNotIn("配属人数", head)


if __name__ == "__main__":
    unittest.main()
