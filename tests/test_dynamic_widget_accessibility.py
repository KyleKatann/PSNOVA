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
        self.assertIn(
            'role="option" tabindex="-1" aria-selected="false"',
            js,
        )
        self.assertIn(
            'input.setAttribute(\n                "aria-activedescendant"',
            js,
        )

    def test_site_search_has_submit_and_keyboard_navigation(self):
        js = SEARCH.read_text(encoding="utf-8")

        self.assertIn(
            '<button class="site-search-submit" type="submit">検索</button>',
            js,
        )
        self.assertIn('form.addEventListener("submit"', js)
        self.assertIn('event.key === "ArrowDown"', js)
        self.assertIn('event.key === "ArrowUp"', js)
        self.assertIn('event.key === "Escape"', js)
        self.assertIn("window.location.assign", js)

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
