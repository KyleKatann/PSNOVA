import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "pages" / "search-corps.html"


class SearchCorpsPageTests(unittest.TestCase):
    def page_html(self):
        return PAGE.read_text(encoding="utf-8")

    def test_public_tables_use_reader_facing_columns(self):
        html = self.page_html()

        for heading in ("派遣名", "必要人数", "必要日数", "通常報酬", "大成功時追加"):
            self.assertEqual(html.count(f'<th scope="col">{heading}</th>'), 7)
        self.assertEqual(html.count('<th scope="col">'), 35)

    def test_intro_and_basic_info_use_polite_style(self):
        html = self.page_html()

        self.assertIn("報酬を持ち帰らせることができます", html)
        self.assertIn("報酬を受け取れます", html)
        self.assertIn("すべて満たす必要があります", html)

    def test_great_success_rewards_remain(self):
        html = self.page_html()

        self.assertIn("大成功時は、通常報酬2種類の数量がそれぞれ2倍", html)
        self.assertIn("大成功時追加", html)
        self.assertEqual(html.count("<table>"), 7)
        self.assertEqual(html.count("<td>［"), 107)

    def test_base_return_link_is_removed(self):
        html = self.page_html()

        self.assertNotIn("拠点施設一覧へ戻る", html)
        self.assertNotIn('href="/PSNOVA/pages/base.html"', html)


if __name__ == "__main__":
    unittest.main()
