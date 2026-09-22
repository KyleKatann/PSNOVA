import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "pages" / "gran-booster.html"
BASE = ROOT / "docs" / "pages" / "base.html"
TRAITS = ROOT / "docs" / "pages" / "traits.html"
SITEMAP = ROOT / "docs" / "sitemap.xml"


class GranBoosterPageTests(unittest.TestCase):
    def page_html(self):
        return PAGE.read_text(encoding="utf-8")

    def test_page_is_reader_facing(self):
        html = self.page_html()

        self.assertIn("<h1>グランブースター</h1>", html)
        self.assertIn("獲得するグランエナジーを増やし、GP消費量を軽減する拠点施設", html)
        self.assertIn("グラン予報士", html)
        self.assertIn("上級グラン予報士", html)

        for internal_term in (
            "497200",
            "497201",
            "parameter902",
            "907100",
            "907110",
            "ID901",
            "ID509",
            "Type12",
            "GacyaNPC_Size",
            "SP07_120_025_ed",
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
            ("1", "500", "1人", "獲得グラン +15% / GP消費 -2%"),
            ("2", "1,000", "2人", "獲得グラン +25% / GP消費 -4%"),
            ("3", "2,500", "3人", "獲得グラン +35% / GP消費 -6%"),
            ("4", "5,000", "4人", "獲得グラン +45% / GP消費 -8%"),
            ("5", "10,000", "5人", "獲得グラン +55% / GP消費 -10%"),
        )

        for row in expected_rows:
            fragment = "<tr>" + "".join(f"<td>{value}</td>" for value in row) + "</tr>"
            with self.subTest(row=row):
                self.assertIn(fragment, html)

    def test_effect_tiers_match_audited_report(self):
        html = self.page_html()

        expected_rows = (
            ("0", "+5%", "変化なし"),
            ("1", "+10%", "-1%"),
            ("2", "+15%", "-2%"),
            ("3", "+20%", "-3%"),
            ("4", "+25%", "-4%"),
            ("5", "+30%", "-5%"),
            ("6", "+35%", "-6%"),
            ("7", "+40%", "-7%"),
            ("8", "+45%", "-8%"),
            ("9", "+50%", "-9%"),
            ("10", "+55%", "-10%"),
        )

        for row in expected_rows:
            fragment = "<tr>" + "".join(f"<td>{value}</td>" for value in row) + "</tr>"
            with self.subTest(row=row):
                self.assertIn(fragment, html)

    def test_baseline_and_trait_weights_are_explicit(self):
        html = self.page_html()

        self.assertIn("施設を設置しただけでも獲得グランエナジーは5%増加", html)
        self.assertIn("「グラン予報士」は効果値を1、「上級グラン予報士」は2増やします", html)
        self.assertIn("合計10で最大", html)
        self.assertIn("<tr><td>グラン予報士</td><td>+1</td><td>獲得グラン +5% / GP消費 -1%</td></tr>", html)
        self.assertIn("<tr><td>上級グラン予報士</td><td>+2</td><td>獲得グラン +10% / GP消費 -2%</td></tr>", html)

    def test_trait_crew_lists_are_complete(self):
        html = self.page_html()

        normal = ("ブライン", "ゴーティス", "スライブ", "フェニディー", "レナ", "ロザリア", "ホオヅキ")
        advanced = ("ミマサギ", "ツヴァイ", "エスト", "セレネ", "ルミア", "ペトク")

        for name in normal + advanced:
            with self.subTest(name=name):
                self.assertIn(f"<li>{name}</li>", html)

        section = html.split("<h2>グラン予報士を持つクルー</h2>", 1)[1]
        section = section.split("<h2>最大効果にするには</h2>", 1)[0]
        self.assertEqual(len(re.findall(r"<li>.*?</li>", section)), 13)

    def test_traits_page_keeps_matching_trait_values(self):
        traits = TRAITS.read_text(encoding="utf-8")

        self.assertIn("<tr><td>グラン予報士</td><td>Gブースター効果 +1</td><td>グランブースター</td><td>消費GP -1% / 入手グラン +5%</td></tr>", traits)
        self.assertIn("<tr><td>上級グラン予報士</td><td>Gブースター効果 +2</td><td>グランブースター</td><td>消費GP -2% / 入手グラン +10%</td></tr>", traits)

    def test_page_is_linked_from_base_and_sitemap(self):
        path = "/PSNOVA/pages/gran-booster.html"

        base = BASE.read_text(encoding="utf-8")
        sitemap = SITEMAP.read_text(encoding="utf-8")

        self.assertIn(f'href="{path}">グランブースター Lv.1</a>', base)
        self.assertIn(f"https://kylekatann.github.io{path}", sitemap)

    def test_public_metadata_is_present(self):
        html = self.page_html()

        self.assertIn("<title>PSNOVA攻略サイト - グランブースター</title>", html)
        self.assertIn(
            '<link rel="canonical" href="https://kylekatann.github.io/PSNOVA/pages/gran-booster.html">',
            html,
        )


if __name__ == "__main__":
    unittest.main()
