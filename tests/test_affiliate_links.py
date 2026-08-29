import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"


class AffiliateLinkTests(unittest.TestCase):
    def test_rakuten_banner_is_replaced_with_contextual_text_link(self):
        js = SIDEBAR.read_text(encoding="utf-8")
        self.assertIn('class="affiliate-links"', js)
        self.assertIn("楽天市場でゲーム関連商品を探す", js)
        self.assertNotIn("https://hbb.afl.rakuten.co.jp/", js)
        self.assertNotIn("<img", js)

    def test_affiliate_link_keeps_sponsored_disclosure_relationship(self):
        js = SIDEBAR.read_text(encoding="utf-8")
        self.assertIn('rel="nofollow sponsored noopener"', js)
        self.assertIn('class="affiliate-disclosure">PR</span>', js)


if __name__ == "__main__":
    unittest.main()
