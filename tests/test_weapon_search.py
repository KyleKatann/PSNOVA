import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENUBAR_JS = ROOT / "docs" / "js" / "menubar.js"
WEAPON_TOOLS_JS = ROOT / "docs" / "js" / "weapon-tools.js"
WEAPON_TOOLS_CSS = ROOT / "docs" / "css" / "weapon-tools.css"
WEAPON_HTML = ROOT / "docs" / "pages" / "weapon.html"

class WeaponSearchTests(unittest.TestCase):
    def test_weapon_tools_load_only_from_weapon_page_loader(self):
        js = MENUBAR_JS.read_text(encoding="utf-8")
        self.assertIn(r"/pages\/weapon\.html$", js)
        self.assertIn("/PSNOVA/js/weapon-tools.js", js)
        self.assertIn("/PSNOVA/css/weapon-tools.css", js)

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

    def test_weapon_data_sentinels_are_preserved(self):
        html = WEAPON_HTML.read_text(encoding="utf-8")
        for value in ("ソード", "アルバギガッシュ", "タルナーダ"):
            with self.subTest(value=value):
                self.assertIn(value, html)
        self.assertGreaterEqual(html.count("<table"), 10)

if __name__ == "__main__":
    unittest.main()
