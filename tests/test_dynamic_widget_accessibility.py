import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SEARCH = ROOT / "docs" / "js" / "site-search.js"
AFFILIATE = ROOT / "docs" / "js" / "affiliate-banner.js"


class DynamicWidgetAccessibilityTests(unittest.TestCase):
    def test_site_search_uses_editable_combobox_semantics(self):
        js = SEARCH.read_text(encoding="utf-8")

        self.assertIn(
            'id="site-data-search" type="search" '
            'role="combobox" aria-autocomplete="list"',
            js,
        )
        self.assertIn(
            'aria-controls="site-search-results"',
            js,
        )
        self.assertIn(
            'aria-expanded="false"',
            js,
        )
        self.assertIn(
            'role="listbox"',
            js,
        )

    def test_affiliate_links_receive_accessible_names(self):
        js = AFFILIATE.read_text(encoding="utf-8")

        self.assertIn(
            "function (markup, index)",
            js,
        )
        self.assertIn(
            'aria-label="楽天市場の商品広告 ',
            js,
        )
        self.assertIn(
            "(index + 1)",
            js,
        )


if __name__ == "__main__":
    unittest.main()
