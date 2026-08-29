import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENUBAR = ROOT / "docs" / "js" / "menubar.js"
AFFILIATE_CSS = ROOT / "docs" / "css" / "affiliate.css"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"


class AffiliateDisclosureStyleTests(unittest.TestCase):
    def test_affiliate_css_is_loaded_globally(self):
        js = MENUBAR.read_text(encoding="utf-8")
        self.assertIn("/PSNOVA/css/affiliate.css", js)
        self.assertIn("data-psnova-affiliate", js)

    def test_pr_disclosure_is_visible_but_restrained(self):
        css = AFFILIATE_CSS.read_text(encoding="utf-8")
        self.assertIn(".affiliate-disclosure", css)
        self.assertIn("font-size: 10px", css)
        self.assertIn("border-top: 1px solid var(--border)", css)
        self.assertNotIn("position: fixed", css)

    def test_sidebar_contains_explicit_pr_label(self):
        js = SIDEBAR.read_text(encoding="utf-8")
        self.assertIn('class="affiliate-disclosure">PR</span>', js)


if __name__ == "__main__":
    unittest.main()
