import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "docs" / "css" / "style.css"
MENUBAR_JS = ROOT / "docs" / "js" / "menubar.js"
SITE_SEARCH_JS = ROOT / "docs" / "js" / "site-search.js"


class SiteSearchEntryTests(unittest.TestCase):
    def test_site_search_assets_are_loaded_globally(self):
        js = MENUBAR_JS.read_text(encoding="utf-8")
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn("/PSNOVA/js/site-search.js", js)
        self.assertIn(".site-search {", css)
        self.assertIn("data-psnova-site-search", js)
        self.assertNotIn("@import", css)

    def test_site_search_mounts_without_removed_menubar(self):
        js = SITE_SEARCH_JS.read_text(encoding="utf-8")
        self.assertIn('document.getElementById("container")', js)
        self.assertIn('container.querySelector(":scope > header")', js)
        self.assertIn("container.insertBefore(wrapper, header.nextSibling)", js)
        self.assertNotIn('document.getElementById("menubar")', js)
        self.assertNotIn("primaryNav", js)

    def test_major_data_pages_are_searchable_as_entry_points(self):
        js = SITE_SEARCH_JS.read_text(encoding="utf-8")
        for path in (
            "/PSNOVA/pages/class.html",
            "/PSNOVA/pages/skill.html",
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
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn("var(--surface)", css)
        self.assertIn("var(--border)", css)
        self.assertIn("var(--accent)", css)


if __name__ == "__main__":
    unittest.main()
