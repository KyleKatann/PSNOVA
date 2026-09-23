import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "pages" / "rare-drop.html"


class RareDropPageTests(unittest.TestCase):
    def page_html(self):
        return PAGE.read_text(encoding="utf-8")

    def test_normal_item_drop_rate_is_explained_for_players(self):
        html = self.page_html()

        self.assertIn(
            "レアアイテムだけを狙う場合、アイテムドロップ率を上げてもレアドロップ率そのものは上がりません",
            html,
        )
        self.assertIn("テンプテーションを付けた武器を持つ必要はありません", html)

    def test_gran_burst_item_drop_is_qualitative(self):
        html = self.page_html()

        self.assertIn("アイテム</td><td>アイテムが出やすくなる", html)
        self.assertIn("レアアイテム狙いでも有効", html)
        self.assertNotIn("ドロップ抽選を1回追加", html)
        self.assertNotIn("追加される1回", html)
        self.assertNotIn("レアドロップアップ", html)
        self.assertNotIn("アイテムドロップアップ", html)

    def test_multiplayer_bonus_does_not_expose_internal_counts(self):
        html = self.page_html()

        self.assertIn("参加するプレイヤーが増えるほどアイテムを入手できる機会が増えます", html)
        self.assertIn("同行NPCを増やしても、この効果は得られません", html)
        for hidden_count in ("+2回", "+3回", "+4回", "追加される抽選回数"):
            with self.subTest(hidden_count=hidden_count):
                self.assertNotIn(hidden_count, html)

    def test_output_limit_is_explained_in_player_facing_language(self):
        html = self.page_html()

        self.assertIn("敵1体から落ちるアイテム数には上限", html)
        self.assertNotIn("最大出現個数", html)
        self.assertNotIn("成功アイテム数", html)

    def test_requested_section_structure(self):
        html = self.page_html()

        self.assertNotIn("「レアエネミー出現率アップ」は別の効果", html)
        self.assertIn('<aside class="npc-password-warning" role="note"', html)
        self.assertIn("<strong>よくある勘違い</strong>", html)
        self.assertIn("background:#fff1f1", html)
        self.assertIn("border-left:4px solid #c83f3f", html)
        self.assertIn("</aside>\n\n                    <h3>捕獲しても不利にはならない</h3>", html)
        self.assertIn("<h3>捕獲しても不利にはならない</h3>", html)
        self.assertIn("<h3>通常アイテムのドロップ率を上げすぎない</h3>", html)
        self.assertNotIn("<h3>レアだけを狙う場合の配置</h3>", html)
        self.assertIn("<h2>結論：レアドロップ率を最大まで上げる</h2>", html)
        self.assertNotIn("<h3>バースト加速装置で狙った効果を出しやすくする</h3>", html)

        self.assertLess(
            html.index("<h2>結論：レアドロップ率を最大まで上げる</h2>"),
            html.index("<strong>よくある勘違い</strong>"),
        )
        self.assertNotIn("エネミーレーダー</a>を参照してください", html)
        self.assertNotIn("バースト加速装置</a>を参照してください", html)
        self.assertNotIn("アイテム探知装置</a>を参照してください", html)

    def test_conclusion_covers_all_practical_methods(self):
        html = self.page_html()

        for term in (
            "アイテム探知装置+ラッキライザー5人",
            "ギガババロア または ギガ骨の髄まで定食",
            "レイヴァン同行",
            "ブーストエネミー",
            "グランバースト「レアドロップ」",
            "グランバースト「アイテム」",
            "マルチプレイ",
            "部位破壊",
            "バースト加速装置",
        ):
            with self.subTest(term=term):
                self.assertIn(term, html)

    def test_internal_analysis_terms_are_not_public(self):
        html = self.page_html()

        for internal_term in (
            "ID513",
            "ID514",
            "effect3",
            "effect5",
            "param0x77",
            "0x8176D958",
            "敵固有枠",
            "通常枠1",
            "通常枠2",
            "通常枠3",
            "通常枠4",
            "地域ドロップ",
            "基本判定回数",
            "ドロップ行",
        ):
            with self.subTest(internal_term=internal_term):
                self.assertNotIn(internal_term, html)


if __name__ == "__main__":
    unittest.main()
