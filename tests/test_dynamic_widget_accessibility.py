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
        self.assertIn('aria-controls="site-search-results"', js)
        self.assertIn('aria-expanded="false"', js)
        self.assertIn('role="listbox"', js)
        self.assertIn('role="option"', js)
        self.assertIn('option.setAttribute("tabindex", "-1")', js)
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

    def test_site_search_discovers_pages_from_sitemap_at_runtime(self):
        js = SEARCH.read_text(encoding="utf-8")

        self.assertIn('var SITEMAP_URL = "/PSNOVA/sitemap.xml"', js)
        self.assertIn('fetch(SITEMAP_URL, { credentials: "same-origin" })', js)
        self.assertIn('parseFromString(xmlText, "application/xml")', js)
        self.assertIn('getElementsByTagNameNS("*", "loc")', js)
        self.assertNotIn('var pages = [', js)
        self.assertNotIn('var searchSources = [', js)

    def test_site_search_indexes_every_data_row_cell_and_supports_partial_text(self):
        js = SEARCH.read_text(encoding="utf-8")

        self.assertIn('Array.prototype.slice.call(row.cells).map', js)
        self.assertIn('var rowText = cells.join(" / ").trim()', js)
        self.assertIn('haystack.indexOf(normalizedQuery) !== -1', js)
        self.assertIn('new DOMParser().parseFromString(html, "text/html")', js)
        self.assertIn(
            'loadSourcesWithLimit(remoteSources, FETCH_CONCURRENCY)',
            js,
        )

    def test_site_search_result_preserves_exact_table_row_target(self):
        js = SEARCH.read_text(encoding="utf-8")

        self.assertIn('url.searchParams.set("site-search-table"', js)
        self.assertIn('url.searchParams.set("site-search-row"', js)
        self.assertIn('row.setAttribute("data-site-search-target", "true")', js)
        self.assertIn('cell.setAttribute("data-site-search-hit", "true")', js)
        self.assertIn('row.scrollIntoView({ block: "center", inline: "nearest" })', js)

    def test_site_search_marks_matching_text_with_site_accent(self):
        js = SEARCH.read_text(encoding="utf-8")

        self.assertIn('document.createElement("mark")', js)
        self.assertIn('mark.className = "site-search-match"', js)
        self.assertIn('mark.style.background = "var(--accent)"', js)
        self.assertIn('appendMarkedText(title, entry.label, query)', js)
        self.assertIn('highlightElementForQuery(cell, query)', js)

    def test_site_search_controls_stay_on_one_row(self):
        js = SEARCH.read_text(encoding="utf-8")

        self.assertIn('controls.style.display = "flex"', js)
        self.assertIn('input.style.flex = "1 1 0"', js)
        self.assertIn('input.style.minWidth = "0"', js)
        self.assertIn('button.style.flex = "0 0 auto"', js)
        self.assertIn('button.style.height = "42px"', js)

    def test_affiliate_links_receive_accessible_names(self):
        js = AFFILIATE.read_text(encoding="utf-8")

        self.assertIn("function (markup, index)", js)
        self.assertIn('aria-label="楽天市場の商品広告 ', js)
        self.assertIn("(index + 1)", js)


if __name__ == "__main__":
    unittest.main()
