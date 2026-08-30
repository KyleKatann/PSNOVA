import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE_ENTRY = ROOT / "docs" / "css" / "style.css"
AFFILIATE_CSS = ROOT / "docs" / "css" / "affiliate.css"
BANNER = ROOT / "docs" / "js" / "affiliate-banner.js"


class AffiliateDisclosureStyleTests(unittest.TestCase):
    def test_affiliate_css_is_loaded_globally(self):
        css = STYLE_ENTRY.read_text(encoding="utf-8")
        self.assertIn('@import url("/PSNOVA/css/affiliate.css");', css)

    def test_campaign_banner_is_visible_and_responsive(self):
        css = AFFILIATE_CSS.read_text(encoding="utf-8")
        self.assertIn(".affiliate-banner {", css)
        self.assertIn("border: 1px solid var(--border)", css)
        self.assertIn(".affiliate-banner-body img {", css)
        self.assertIn("max-width: 100%", css)
        self.assertIn("height: auto", css)
        self.assertNotIn("position: fixed", css)

    def test_banner_contains_explicit_pr_label(self):
        js = BANNER.read_text(encoding="utf-8")
        self.assertIn('class=\"affiliate-disclosure\">PR</span>', js)
        self.assertIn('aria-label', js)
        self.assertIn('楽天市場のPR', js)


if __name__ == "__main__":
    unittest.main()
