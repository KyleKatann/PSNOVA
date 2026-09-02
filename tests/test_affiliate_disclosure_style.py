import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "docs" / "css" / "style.css"
BANNER = ROOT / "docs" / "js" / "affiliate-banner.js"


def affiliate_css():
    css = STYLE.read_text(encoding="utf-8")
    return css.split("/* === AFFILIATE / PR === */", 1)[1].split(
        "/* === SITE SEARCH === */",
        1,
    )[0]


class AffiliateDisclosureStyleTests(unittest.TestCase):
    def test_affiliate_css_is_owned_by_sitewide_bundle(self):
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn(".affiliate-banner {", css)
        self.assertNotIn("@import", css)

    def test_campaign_banner_is_visible_and_responsive(self):
        css = affiliate_css()

        self.assertIn(".affiliate-banner {", css)
        self.assertIn("border: 1px solid var(--border)", css)
        self.assertIn(".affiliate-banner-item img {", css)
        self.assertIn("width: 100%;", css)
        self.assertIn("height: 100%;", css)
        self.assertIn("object-fit: contain;", css)
        self.assertIn(".affiliate-banner-item:nth-child(n + 2)", css)
        self.assertNotIn("position: fixed", css)

    def test_banner_contains_explicit_pr_label(self):
        js = BANNER.read_text(encoding="utf-8")

        self.assertIn('class="affiliate-disclosure">PR</span>', js)
        self.assertIn("aria-label", js)
        self.assertIn("楽天市場のPR", js)


if __name__ == "__main__":
    unittest.main()
