import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE_ENTRY = ROOT / "docs" / "css" / "style.css"
MENUBAR_JS = ROOT / "docs" / "js" / "menubar.js"
WEAPON_TOOLS_JS = ROOT / "docs" / "js" / "weapon-tools.js"
WEAPON_TOOLS_CSS = ROOT / "docs" / "css" / "weapon-tools.css"
WEAPON_HTML = ROOT / "docs" / "pages" / "weapon.html"
KNUCKLE_HTML = ROOT / "docs" / "pages" / "weapon" / "knuckle.html"


class WeaponSearchTests(unittest.TestCase):
    def test_weapon_tools_load_for_catalog_and_weapon_children(self):
        js = MENUBAR_JS.read_text(encoding="utf-8")
        css = STYLE_ENTRY.read_text(encoding="utf-8")
        self.assertIn('/\\/pages\\/weapon(?:\\.html|\\/[^/]+\\.html)$/', js)
        self.assertIn("/PSNOVA/js/weapon-tools.js", js)
        self.assertIn('@import url("/PSNOVA/css/weapon-tools.css");', css)

    def test_weapon_name_search_filters_existing_rows(self):
        js = WEAPON_TOOLS_JS.read_text(encoding="utf-8")
        self.assertIn('id="weapon-search"', js)
        self.assertIn('normalize("NFKC")', js)
        self.assertIn("cells[0].textContent", js)
        self.assertIn("record.row.hidden = !visible;", js)
        self.assertIn('input.addEventListener("input", applyFilters)', js)
        self.assertIn("aria-live", js)

    def test_weapon_search_has_dedicated_lightweight_styles(self):
        css = WEAPON_TOOLS_CSS.read_text(encoding="utf-8")
        self.assertIn(".data-toolbar", css)
        self.assertIn('input[type="search"]', css)
        self.assertIn("tr[hidden]", css)

    def test_weapon_landing_page_is_catalog_not_embedded_data_copy(self):
        html = WEAPON_HTML.read_text(encoding="utf-8")
        self.assertIn('class="weapon-catalog"', html)
        self.assertEqual(11, html.count('class="weapon-card"'))
        self.assertNotIn("<table", html)
        self.assertNotIn("<details", html)

    def test_static_weapon_child_preserves_data_sentinels(self):
        html = KNUCKLE_HTML.read_text(encoding="utf-8")
        for value in ("ナックル", "エイトオンス", "ノヴァクローグ", "ファイバーロア"):
            with self.subTest(value=value):
                self.assertIn(value, html)


if __name__ == "__main__":
    unittest.main()
