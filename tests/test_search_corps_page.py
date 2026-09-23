import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "pages" / "search-corps.html"


class SearchCorpsPageTests(unittest.TestCase):
    def page_html(self):
        return PAGE.read_text(encoding="utf-8")

    def test_rate_information_is_not_public(self):
        html = self.page_html()

        self.assertNotIn("大成功率", html)
        self.assertNotIn("基礎疲労率", html)
        self.assertNotIn("怪我率アップ", html)
        self.assertNotIn("<td>5%</td>", html)
        self.assertNotIn("<td>6%</td>", html)
        self.assertNotIn("<td>8%</td>", html)
        self.assertNotIn("<td>10%</td>", html)
        self.assertNotIn("<td>20%</td>", html)
        self.assertNotIn("<td>30%</td>", html)

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
