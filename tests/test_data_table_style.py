import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODERN_CSS = ROOT / "docs" / "css" / "modern.css"
STYLE_CSS = ROOT / "docs" / "css" / "style.css"
MOBILE_TABLE_CSS = ROOT / "docs" / "css" / "mobile-table.css"


class DataTableStyleTests(unittest.TestCase):
    def test_tables_are_flat_and_data_oriented(self):
        css = MODERN_CSS.read_text(encoding="utf-8")
        self.assertIn("/* Data tables */", css)
        self.assertIn("border-collapse: separate;", css)
        self.assertIn("box-shadow: none;", css)
        self.assertIn("font-family: inherit;", css)
        self.assertIn("text-transform: none;", css)

    def test_details_tables_share_consistent_container_style(self):
        css = MODERN_CSS.read_text(encoding="utf-8")
        self.assertIn("details > summary {", css)
        self.assertIn("details[open] > summary", css)
        self.assertIn("details > table {", css)

    def test_tables_scroll_horizontally_on_mobile(self):
        css = MODERN_CSS.read_text(encoding="utf-8")
        self.assertIn("overflow-x: auto;", css)
        self.assertIn("-webkit-overflow-scrolling: touch;", css)

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

    def test_mobile_all_internal_tables_freeze_only_first_column(self):
        css = MOBILE_TABLE_CSS.read_text(encoding="utf-8")
        self.assertIn("#main .table-scroll > table th:first-child", css)
        self.assertIn("#main .table-scroll > table td:first-child", css)
        self.assertIn("position: sticky;", css)
        self.assertIn("left: 0;", css)
        self.assertNotIn(":nth-child(2) {\n        position: sticky", css)


if __name__ == "__main__":
    unittest.main()
