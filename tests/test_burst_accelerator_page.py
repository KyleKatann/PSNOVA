import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "pages" / "burst-accelerator.html"
BASE = ROOT / "docs" / "pages" / "base.html"
TRAITS = ROOT / "docs" / "pages" / "traits.html"
SITEMAP = ROOT / "docs" / "sitemap.xml"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"


class BurstAcceleratorPageTests(unittest.TestCase):
    def page_html(self):
        return PAGE.read_text(encoding="utf-8")

    def test_page_is_reader_facing(self):
        html = self.page_html()

        self.assertIn("<h1>バースト加速装置</h1>", html)
        self.assertIn("Lv1～5で配属できる人数が1～5人へ増えます", html)
        self.assertIn("抽選上の重みが1増えます", html)
        self.assertIn("すでに発動中の効果は次回候補から除外", html)

        for internal_term in (
            "500200",
            "500211",
            "parameter910",
            "parameter921",
            "910100",
            "Type14",
            "GacyaNPC_Size",
            "effect1",
            "0x8174",
            "SP08_140_030_ed",
            "9050010",
            "9090090",
            "Pat_01_3",
            "PR_1320_orc",
        ):
            with self.subTest(internal_term=internal_term):
                self.assertNotIn(internal_term, html)

    def test_facility_levels_match_audited_data(self):
        html = self.page_html()
        expected = (
            ("1", "500", "1人"),
            ("2", "1,000", "2人"),
            ("3", "2,500", "3人"),
            ("4", "5,000", "4人"),
            ("5", "10,000", "5人"),
        )
        for row in expected:
            fragment = "<tr>" + "".join(f"<td>{v}</td>" for v in row) + "</tr>"
            with self.subTest(row=row):
                self.assertIn(fragment, html)

    def test_probability_examples_match_runtime_weight_model(self):
        html = self.page_html()

        self.assertIn("レアドロップが選ばれる確率は2/5 = 40%", html)
        self.assertIn("<tr><td>1</td><td>50%</td><td>25%</td><td>25%</td></tr>", html)
        self.assertIn("<tr><td>2</td><td>60%</td><td>40%</td><td>40%</td></tr>", html)
        self.assertIn("<tr><td>3</td><td>66.67%</td><td>50%</td><td>50%</td></tr>", html)
        self.assertIn("<tr><td>4</td><td>71.43%</td><td>57.14%</td><td>50%</td></tr>", html)
        self.assertIn("<tr><td>5</td><td>71.43%</td><td>57.14%</td><td>50%</td></tr>", html)
        self.assertIn("余った枠へ別のBURST特徴を置くと分母が増えるため、空けておく方が高確率", html)

    def test_old_125_percent_interpretation_is_explicitly_rejected(self):
        html = self.page_html()

        self.assertIn("「ハズレ62.5%」ではない", html)
        self.assertIn("それぞれ約33.33%", html)
        self.assertNotIn("配属なしではハズレ62.5%", html)

    def test_burst_item_effect_is_draw_count_not_rate(self):
        html = self.page_html()
        traits = TRAITS.read_text(encoding="utf-8")

        self.assertIn("<tr><td>BURST:アイテム</td><td>ドロップ抽選回数を1回追加</td>", html)
        self.assertIn("<tr><td>BURST:アイテム</td><td>ドロップ抽選回数を1回追加</td></tr>", traits)
        self.assertNotIn("<tr><td>BURST:アイテム</td><td>アイテムのドロップ率アップ</td></tr>", traits)

    def test_current_holder_counts_are_reflected(self):
        html = self.page_html()

        expected_rows = {
            "BURST:経験値UP": "ハツェル、ルービン、カーミル、サーラル",
            "BURST:アイテム": "セドゥム、ヨウゲン、カーク、アマネ",
            "BURST:レアエネミー": "ターラー、エーレ、セレネ、ユーリ",
            "BURST:レアドロップ": "エッセル、ペダル、シャオリン、ネオン",
            "BURST:ワンモア": "レギスタン、アイム、ティーン",
            "BURST:ガッツ": "イスタル、ナージエ、トレーズ、ナリサ",
            "BURST:ダメージカット": "サフェード、オボロ、プレイア",
            "BURST:コンバージョン": "ノーヴィーク、アルテ、イリーナ、ペトク",
            "BURST:クリティカル": "ノライク、ドゥーベン、オルガ、ジャニス",
            "BURST:モータルブロウ": "レスタム、ノヴァイア、ネイザン、エフェス",
        }
        for trait, crew in expected_rows.items():
            with self.subTest(trait=trait):
                self.assertIn(f"<td>{trait}</td>", html)
                self.assertIn(f"<td>{crew}</td>", html)

        self.assertIn("「BURST:原生種」「BURST:ダーカー」", html)
        self.assertIn("所持者を確認できません", html)

    def test_page_is_linked_from_base_sidebar_and_sitemap(self):
        path = "/PSNOVA/pages/burst-accelerator.html"
        base = BASE.read_text(encoding="utf-8")
        sidebar = SIDEBAR.read_text(encoding="utf-8")
        sitemap = SITEMAP.read_text(encoding="utf-8")

        self.assertIn(f'href="{path}">バースト加速装置 Lv.1</a>', base)
        self.assertIn(f'<li><a href="{path}">バースト加速装置</a></li>', sidebar)
        self.assertIn(f'currentPath === "{path}"', sidebar)
        self.assertIn(f"https://kylekatann.github.io{path}", sitemap)

    def test_public_metadata_is_present(self):
        html = self.page_html()

        self.assertIn("<title>PSNOVA攻略サイト - バースト加速装置</title>", html)
        self.assertIn(
            '<link rel="canonical" href="https://kylekatann.github.io/PSNOVA/pages/burst-accelerator.html">',
            html,
        )


if __name__ == "__main__":
    unittest.main()
