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
        self.assertIn("レアエネミーとブーストエネミーの出現率を上げる拠点施設", html)
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

    def test_facility_level_table_matches_audited_report(self):
        html = self.page_html()

        expected_rows = (
            ("1", "500", "1人", "1人"),
            ("2", "1,000", "2人", "2人"),
            ("3", "2,500", "3人", "3人"),
            ("4", "5,000", "4人", "4人"),
            ("5", "10,000", "5人", "5人"),
        )

        for row in expected_rows:
            fragment = "<tr>" + "".join(f"<td>{value}</td>" for value in row) + "</tr>"
            with self.subTest(row=row):
                self.assertIn(fragment, html)

    def test_effect_tier_table_matches_audited_report(self):
        html = self.page_html()

        expected_rows = (
            ("0人", "×1.50", "×2.50", "7.5%"),
            ("1人", "×1.75", "×2.75", "8.25%"),
            ("2人", "×2.00", "×3.00", "9%"),
            ("3人", "×3.00", "×4.00", "12%"),
            ("4人", "×4.00", "×5.00", "15%"),
            ("5人", "×7.00", "×8.00", "24%"),
        )

        for row in expected_rows:
            fragment = "<tr>" + "".join(f"<td>{value}</td>" for value in row) + "</tr>"
            with self.subTest(row=row):
                self.assertIn(fragment, html)

    def test_rare_and_boost_explanations_keep_distinct_semantics(self):
        html = self.page_html()

        self.assertIn("通常の出現判定とは別に行われる追加のレア化判定", html)
        self.assertIn("最終的なレアエネミー出現率へそのまま掛けるものではありません", html)
        self.assertIn("ブーストエネミーは表の倍率が最終的な出現率に反映されます", html)
        self.assertIn("基礎3%のため、「野生の勘」5人では24%", html)

    def test_maximum_effect_limits_match_audited_report(self):
        html = self.page_html()

        self.assertIn("<h2>最大時の実効率</h2>", html)
        self.assertIn("基礎レア発生率が20%に設定されているラッピーのみ", html)
        self.assertIn("20% × 7.00 = 140%相当", html)
        self.assertIn("最終的なレアエネミー出現率が100%になるという意味ではありません", html)
        self.assertIn("最大でも24%", html)
        self.assertIn("エネミーレーダー単独でブーストエネミー出現率を100%にはできません", html)

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
        self.assertIn(f'<li><a href="{path}">エネミーレーダー</a></li>', sidebar)
        self.assertIn(f"https://kylekatann.github.io{path}", sitemap)

    def test_public_metadata_is_present(self):
        html = self.page_html()

        self.assertIn("<title>PSNOVA攻略サイト - エネミーレーダー</title>", html)
        self.assertIn(
            '<link rel="canonical" href="https://kylekatann.github.io/PSNOVA/pages/enemy-radar.html">',
            html,
        )


if __name__ == "__main__":
    unittest.main()
