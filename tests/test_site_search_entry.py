import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENUBAR_JS = ROOT / "docs" / "js" / "menubar.js"
SITE_SEARCH_JS = ROOT / "docs" / "js" / "site-search.js"
SITE_SEARCH_CSS = ROOT / "docs" / "css" / "site-search.css"

class SiteSearchEntryTests(unittest.TestCase):
    def test_site_search_assets_are_loaded_globally(self):
        js = MENUBAR_JS.read_text(encoding="utf-8")
        self.assertIn("/PSNOVA/js/site-search.js", js)
        self.assertIn("/PSNOVA/css/site-search.css", js)
        self.assertIn("data-psnova-site-search", js)

    def test_major_data_pages_are_searchable_as_entry_points(self):
        js = SITE_SEARCH_JS.read_text(encoding="utf-8")
        for path in (
            "/PSNOVA/pages/weapon.html",
            "/PSNOVA/pages/armor.html",
            "/PSNOVA/pages/material.html",
            "/PSNOVA/pages/enemy.html",
            "/PSNOVA/pages/specialability.html",
            "/PSNOVA/pages/trophy.html",
        ):
            with self.subTest(path=path):
                self.assertIn(path, js)

    def test_search_entry_is_accessible_and_dismissible(self):
        js = SITE_SEARCH_JS.read_text(encoding="utf-8")
        self.assertIn('id="site-data-search"', js)
        self.assertIn('aria-controls="site-search-results"', js)
        self.assertIn('role="listbox"', js)
        self.assertIn('event.key === "Escape"', js)

    def test_search_styles_use_existing_design_tokens(self):
        css = SITE_SEARCH_CSS.read_text(encoding="utf-8")
        self.assertIn("var(--surface)", css)
        self.assertIn("var(--border)", css)
        self.assertIn("var(--accent)", css)

if __name__ == "__main__":
    unittest.main()
