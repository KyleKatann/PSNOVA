import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODERN_CSS = ROOT / "docs" / "css" / "modern.css"
WIKI_TABLE_CSS = ROOT / "docs" / "css" / "wiki-table.css"
STYLE_CSS = ROOT / "docs" / "css" / "style.css"
MOBILE_TABLE_CSS = ROOT / "docs" / "css" / "mobile-table.css"
TABLE_JS = ROOT / "docs" / "js" / "table-enhancements.js"
WEAPON = ROOT / "docs" / "pages" / "weapon" / "knuckle.html"
ENEMY = ROOT / "docs" / "pages" / "enemy.html"
GIGANTES = ROOT / "docs" / "pages" / "gigantes.html"


class DataTableStyleTests(unittest.TestCase):
    def test_tables_are_flat_and_data_oriented(self):
        css = MODERN_CSS.read_text(encoding="utf-8")
        self.assertIn("border-collapse: separate;", css)
        self.assertIn("box-shadow: none;", css)
        self.assertIn("font-family: inherit;", css)

    def test_details_tables_share_consistent_container_style(self):
        css = MODERN_CSS.read_text(encoding="utf-8")
        self.assertIn("details > summary {", css)
        self.assertIn("details[open] > summary", css)
        self.assertIn("details > table {", css)

    def test_table_scroll_wrapper_owns_horizontal_scrolling(self):
        css = WIKI_TABLE_CSS.read_text(encoding="utf-8")
        mobile = MOBILE_TABLE_CSS.read_text(encoding="utf-8")
        self.assertIn("#main .table-scroll {", css)
        self.assertIn("overflow-x: auto;", css)
        self.assertIn("-webkit-overflow-scrolling: touch;", css)
        self.assertIn("body:not(.homepage) #main table {", mobile)
        self.assertIn("display: table;", mobile)
        self.assertIn("overflow: visible;", mobile)

    def test_mobile_table_rules_are_loaded_after_shared_table_style(self):
        css = STYLE_CSS.read_text(encoding="utf-8")
        wiki_index = css.index('@import url("/PSNOVA/css/wiki-table.css");')
        mobile_index = css.index('@import url("/PSNOVA/css/mobile-table.css");')
        self.assertLess(wiki_index, mobile_index)

    def test_mobile_internal_tables_do_not_auto_wrap(self):
        css = MOBILE_TABLE_CSS.read_text(encoding="utf-8")
        self.assertIn("@media screen and (max-width: 800px)", css)
        self.assertIn("body:not(.homepage) #main .table-scroll > table th", css)
        self.assertIn("body:not(.homepage) #main .table-scroll > table td", css)
        self.assertIn("white-space: nowrap;", css)
        self.assertIn("width: max-content;", css)
        self.assertIn("min-width: 100%;", css)

    def test_mobile_sticky_column_uses_logical_key_class_not_dom_first_child(self):
        css = MOBILE_TABLE_CSS.read_text(encoding="utf-8")
        js = TABLE_JS.read_text(encoding="utf-8")
        self.assertIn(".mobile-key-cell", css)
        self.assertIn("position: sticky;", css)
        self.assertIn("left: 0;", css)
        self.assertNotIn("table th:first-child", css)
        self.assertNotIn("table td:first-child", css)
        self.assertIn("function identifyingColumnIndex", js)
        self.assertIn('/名$/.test(label)', js)
        self.assertIn("cell.rowSpan", js)
        self.assertIn("data-mobile-key-column", js)

    def test_weapon_enemy_and_gigantes_resolve_name_column_from_their_headers(self):
        weapon = WEAPON.read_text(encoding="utf-8")
        enemy = ENEMY.read_text(encoding="utf-8")
        gigantes = GIGANTES.read_text(encoding="utf-8")

        self.assertIn('<th scope="col">名前</th>', weapon)
        self.assertIn('<tr><th bgcolor="#87cefa">名前</th>', enemy)
        self.assertIn('<tr><th scope="col">種別</th><th scope="col">名前</th>', gigantes)
        self.assertIn('rowspan="3"', gigantes)


if __name__ == "__main__":
    unittest.main()
