import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "pages" / "burst-accelerator.html"
BASE = ROOT / "docs" / "pages" / "base.html"
SITEMAP = ROOT / "docs" / "sitemap.xml"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"


class BurstAcceleratorPageTests(unittest.TestCase):
    def page_html(self):
        return PAGE.read_text(encoding="utf-8")

    def test_page_is_reader_facing(self):
        html = self.page_html()

        self.assertIn("<h1>バースト加速装置</h1>", html)
        self.assertIn("狙ったグランバーストを出しやすくする拠点施設", html)
        self.assertIn("Lv1～5で配属できる人数が1～5人へ増えます", html)
        self.assertIn(
            "同じBURST特徴を持つクルーを複数配属すると、その特徴に対応するグランバーストが選ばれやすくなります",
            html,
        )
        self.assertIn("すでに発動している効果は、次のグランバーストでは選ばれません", html)
        self.assertIn("<h2>狙ったグランバーストを出しやすくするには</h2>", html)
        self.assertNotIn("<h2>まず結論</h2>", html)
        self.assertNotIn("<h2>同じBURST特徴を持つクルーを配属する</h2>", html)



    def test_noncombat_effects_use_player_facing_wording(self):
        html = self.page_html()

        expected = (
            ("BURST:経験値UP", "獲得経験値が増える"),
            ("BURST:アイテム", "アイテムが出やすくなる"),
            ("BURST:レアエネミー", "レアエネミーが出やすくなる"),
            ("BURST:レアドロップ", "レアドロップ率が上がる"),
        )
        for trait, effect in expected:
            with self.subTest(trait=trait):
                self.assertIn(f"<tr><td>{trait}</td><td>{effect}</td>", html)

    def test_combat_effect_wording_is_preserved(self):
        html = self.page_html()

        expected = (
            ("BURST:ワンモア", "「ワンモア」の発生率アップ"),
            ("BURST:ガッツ", "HP10%以上の時、致死ダメージを受けてもHP1で踏みとどまる"),
            ("BURST:ダメージカット", "エネミーから受けるダメージを減少"),
            ("BURST:コンバージョン", "ダメージを受けるとGPが回復"),
            ("BURST:クリティカル", "クリティカルの発生率アップ"),
            ("BURST:モータルブロウ", "打撃攻撃のダメージが2倍になる"),
        )
        for trait, effect in expected:
            with self.subTest(trait=trait):
                self.assertIn(f"<tr><td>{trait}</td><td>{effect}</td>", html)

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

    def test_footer_navigation_links_are_removed(self):
        html = self.page_html()

        self.assertNotIn("クルーの特徴一覧を見る", html)
        self.assertNotIn("拠点施設一覧へ戻る", html)

    def test_page_is_linked_from_base_sidebar_and_sitemap(self):
        path = "/PSNOVA/pages/burst-accelerator.html"
        base = BASE.read_text(encoding="utf-8")
        sidebar = SIDEBAR.read_text(encoding="utf-8")
        sitemap = SITEMAP.read_text(encoding="utf-8")

        self.assertIn(f'href="{path}">バースト加速装置 Lv.1</a>', base)
        self.assertIn("配属したBURST特徴に対応するグランバーストを出しやすくする", base)
        self.assertIn(f'<li><a href="{path}">バースト加速装置</a></li>', sidebar)
        self.assertIn(f'currentPath === "{path}"', sidebar)
        self.assertIn(f"https://kylekatann.github.io{path}", sitemap)

    def test_tables_have_reader_facing_captions(self):
        html = self.page_html()

        self.assertIn("<caption>BURST特徴ごとの発動時の効果と所持クルー</caption>", html)
        self.assertEqual(html.count("<caption>"), 1)


    def test_public_metadata_is_present(self):
        html = self.page_html()

        self.assertIn("<title>PSNOVA攻略サイト - バースト加速装置</title>", html)
        self.assertIn(
            '<link rel="canonical" href="https://kylekatann.github.io/PSNOVA/pages/burst-accelerator.html">',
            html,
        )
        head = html.split("</head>", 1)[0]
        self.assertNotIn("配属人数", head)


if __name__ == "__main__":
    unittest.main()
