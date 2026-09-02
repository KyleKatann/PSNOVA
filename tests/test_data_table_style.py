import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "docs" / "css" / "style.css"
TABLE_JS = ROOT / "docs" / "js" / "table-enhancements.js"


class DataTableStyleTests(unittest.TestCase):
    def test_tables_are_flat_and_data_oriented(self):
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn("border-collapse: separate;", css)
        self.assertIn("box-shadow: none;", css)
        self.assertIn("font-family: inherit;", css)

    def test_details_tables_share_consistent_container_style(self):
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn("details > summary {", css)
        self.assertIn("details[open] > summary", css)
        self.assertIn("details > table {", css)

    def test_table_scroll_wrapper_owns_horizontal_scrolling(self):
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn("#main .table-scroll {", css)
        self.assertIn("overflow-x: auto;", css)
        self.assertIn("-webkit-overflow-scrolling: touch;", css)
        self.assertIn("body:not(.homepage) #main table {", css)
        self.assertIn("display: table;", css)
        self.assertIn("overflow: visible;", css)

    def test_mobile_table_rules_follow_shared_table_style(self):
        css = STYLE.read_text(encoding="utf-8")
        shared_index = css.index("/* === SHARED DATA TABLES === */")
        mobile_index = css.index("/* === MOBILE TABLE OVERRIDES === */")
        self.assertLess(shared_index, mobile_index)

    def test_mobile_internal_tables_do_not_auto_wrap(self):
        css = STYLE.read_text(encoding="utf-8")
        mobile = css.split("/* === MOBILE TABLE OVERRIDES === */", 1)[1].split(
            "/* === INTERACTION AND RESPONSIVE NAV === */",
            1,
        )[0]

        self.assertIn("@media screen and (max-width: 800px)", mobile)
        self.assertIn("body:not(.homepage) #main .table-scroll > table th", mobile)
        self.assertIn("body:not(.homepage) #main .table-scroll > table td", mobile)
        self.assertIn("white-space: nowrap;", mobile)
        self.assertIn("width: max-content;", mobile)
        self.assertIn("min-width: 100%;", mobile)

    def test_mobile_internal_tables_have_no_frozen_columns(self):
        css = STYLE.read_text(encoding="utf-8")
        mobile = css.split("/* === MOBILE TABLE OVERRIDES === */", 1)[1].split(
            "/* === INTERACTION AND RESPONSIVE NAV === */",
            1,
        )[0]
        js = TABLE_JS.read_text(encoding="utf-8")

        self.assertNotIn("position: sticky;", mobile)
        self.assertNotIn("mobile-key-cell", mobile)
        self.assertNotIn("mobile-key-cell", js)
        self.assertNotIn("data-mobile-key-column", js)
        self.assertNotIn("identifyingColumnIndex", js)
        self.assertNotIn("decorateMobileKeyColumn", js)


if __name__ == "__main__":
    unittest.main()
