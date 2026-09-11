import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENUBAR = ROOT / "docs" / "js" / "menubar.js"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"
BANNER = MENUBAR


class AffiliateLinkTests(unittest.TestCase):
    def test_rotating_rakuten_banner_is_bundled_globally(self):
        menubar = MENUBAR.read_text(encoding="utf-8")
        self.assertIn("function renderBannerItems()", menubar)
        self.assertIn("function insertBanner()", menubar)
        self.assertNotIn("/PSNOVA/js/affiliate-banner.js", menubar)
        self.assertNotIn("data-psnova-affiliate-banner", menubar)

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

    def test_rakuten_ranking_widget_uses_requested_configuration(self):
        js = BANNER.read_text(encoding="utf-8")

        for token in (
            'rakuten_design=\"slide\"',
            'rakuten_affiliateId=\"1684437a.b247fdb8.1684437b.b272d4f6\"',
            'rakuten_items=\"ranking\"',
            'rakuten_genreId=\"566382\"',
            'rakuten_size=\"728x200\"',
            'rakuten_target=\"_blank\"',
            'rakuten_theme=\"gray\"',
            'rakuten_border=\"off\"',
            'rakuten_auto_mode=\"on\"',
            'rakuten_genre_title=\"off\"',
            'rakuten_recommend=\"on\"',
            'rakuten_ts=\"1789147399706\"',
            'https://xml.affiliate.rakuten.co.jp/widget/js/rakuten_widget.js?20230106',
        ):
            with self.subTest(token=token):
                self.assertIn(token, js)

    def test_ranking_widget_uses_primary_slot_and_campaign_moves_to_main_bottom(self):
        js = BANNER.read_text(encoding="utf-8")

        primary = 'insertAtPrimaryPosition(section, createRakutenWidget());'
        bottom = 'main.appendChild(createCampaignBanner());'
        self.assertIn(primary, js)
        self.assertIn(bottom, js)
        self.assertLess(js.index(primary), js.index(bottom))

    def test_old_sidebar_text_ad_is_removed(self):
        js = SIDEBAR.read_text(encoding="utf-8")
        self.assertNotIn('class="affiliate-links"', js)
        self.assertNotIn('楽天市場でゲーム関連商品を探す', js)
        self.assertNotIn('hb.afl.rakuten.co.jp', js)


if __name__ == "__main__":
    unittest.main()
