import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENUBAR = ROOT / "docs" / "js" / "menubar.js"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"
BANNER = ROOT / "docs" / "js" / "affiliate-banner.js"


class AffiliateLinkTests(unittest.TestCase):
    def test_rotating_rakuten_banner_is_loaded_globally(self):
        menubar = MENUBAR.read_text(encoding="utf-8")
        self.assertIn('/PSNOVA/js/affiliate-banner.js', menubar)
        self.assertIn('data-psnova-affiliate-banner', menubar)

    def test_six_rakuten_campaign_banners_are_available(self):
        js = BANNER.read_text(encoding="utf-8")
        self.assertEqual(js.count('https://hb.afl.rakuten.co.jp/hsc/'), 6)
        self.assertEqual(js.count('https://hbb.afl.rakuten.co.jp/hsb/'), 6)
        self.assertEqual(js.count('rel=\"nofollow sponsored noopener\"'), 6)

    def test_banner_rotates_by_day_and_page(self):
        js = BANNER.read_text(encoding="utf-8")
        self.assertIn('Math.floor(Date.now() / 86400000)', js)
        self.assertIn('pathHash(window.location.pathname)', js)
        self.assertIn('class=\"affiliate-disclosure\">PR</span>', js)

    def test_old_sidebar_text_ad_is_removed(self):
        js = SIDEBAR.read_text(encoding="utf-8")
        self.assertNotIn('class="affiliate-links"', js)
        self.assertNotIn('楽天市場でゲーム関連商品を探す', js)
        self.assertNotIn('hb.afl.rakuten.co.jp', js)


if __name__ == "__main__":
    unittest.main()
