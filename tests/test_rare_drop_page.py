import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "pages" / "rare-drop.html"


class RareDropPageTests(unittest.TestCase):
    def page_html(self):
        return PAGE.read_text(encoding="utf-8")

    def test_normal_item_drop_rate_does_not_boost_rare_slot(self):
        html = self.page_html()

        self.assertIn("通常枠に作用する「アイテムドロップ率アップ」はレア枠には作用しません", html)
        self.assertIn("テンプテーションを付けた武器を持ってもレア枠の当選率は上がらない", html)
        self.assertIn("レアドロップ率を上げる目的では装備する意味はありません", html)

    def test_gran_burst_item_drop_adds_a_full_lottery(self):
        html = self.page_html()

        self.assertIn("追加される1回は通常枠だけを判定するものではありません", html)
        self.assertIn("レア枠を含む5枠の抽選をもう1回行う効果", html)
        self.assertIn("追加された抽選でも、最初にレアドロップ率アップ後のレア枠を判定します", html)
        self.assertIn("追加抽選まで実行されればレアを引ける機会が1回増えます", html)

    def test_output_cap_exception_is_explained(self):
        html = self.page_html()

        self.assertIn("1体の敵から出せる成功アイテム数の上限", html)
        self.assertIn("必ずレア判定が1回増えるとは限りません", html)

    def test_internal_analysis_identifiers_are_not_public(self):
        html = self.page_html()

        for internal_term in (
            "ID513",
            "ID514",
            "effect3",
            "effect5",
            "param0x77",
            "0x8176D958",
        ):
            with self.subTest(internal_term=internal_term):
                self.assertNotIn(internal_term, html)


if __name__ == "__main__":
    unittest.main()
