import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "pages" / "item-detector.html"
BASE = ROOT / "docs" / "pages" / "base.html"


class ItemDetectorPageTests(unittest.TestCase):
    def page_html(self):
        return PAGE.read_text(encoding="utf-8")

    def test_page_uses_reader_facing_drop_terms(self):
        html = self.page_html()

        self.assertIn("「ダウジンガー」は通常アイテム、「ラッキライザー」はレアアイテムを出やすくします", html)
        self.assertIn("<tr><td>ダウジンガー</td><td>通常アイテム</td><td>+100%</td></tr>", html)
        self.assertIn("<tr><td>ラッキライザー</td><td>レアアイテム</td><td>+100%</td></tr>", html)
        self.assertIn('<th scope="col">効果</th>', html)

        for internal_term in (
            "通常枠",
            "レア枠",
            "最終的なアイテム取得率まで完全に独立",
        ):
            with self.subTest(internal_term=internal_term):
                self.assertNotIn(internal_term, html)

    def test_base_uses_same_reader_facing_terms(self):
        base = BASE.read_text(encoding="utf-8")

        self.assertIn("通常アイテム・レアアイテムを出やすくする", base)
        self.assertIn("ダウジンガーで通常アイテム、ラッキライザーでレアアイテムをさらに出やすくする", base)
        self.assertNotIn("特徴【ダウジンガー】【ラッキライザー】", base)

    def test_metadata_does_not_claim_assignment_count_table(self):
        html = self.page_html()
        head = html.split("</head>", 1)[0]

        self.assertNotIn("配属人数", head)
        self.assertIn("ダウジンガー・ラッキライザーによる通常アイテムとレアアイテムへの効果", head)


if __name__ == "__main__":
    unittest.main()
