import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "docs" / "css" / "page.css"
STYLE = ROOT / "docs" / "css" / "style.css"
JS = ROOT / "docs" / "js" / "weapon-tools.js"
MENUBAR = ROOT / "docs" / "js" / "menubar.js"


class StickyDataUiTests(unittest.TestCase):
    def test_desktop_toolbar_stays_visible_after_scroll_on_fine_pointer(self):
        css = CSS.read_text(encoding="utf-8")

        self.assertIn(
            "@media screen and (min-width: 801px) and (hover: hover) and (pointer: fine) {",
            css,
        )
        self.assertIn(
            ".data-toolbar { position: sticky; top: 8px; z-index: 30; box-shadow: none; }",
            css,
        )
        self.assertNotIn(
            "#main.weapon-detail-page .data-toolbar",
            css,
        )

    def test_detail_table_header_stays_in_normal_flow(self):
        css = CSS.read_text(encoding="utf-8")

        self.assertNotIn(
            ".weapon-data-table thead th",
            css,
        )
        self.assertNotIn(
            "--weapon-table-header-sticky-top",
            css,
        )

    def test_touch_desktop_site_keeps_tables_inside_scroll_wrappers(self):
        css = CSS.read_text(encoding="utf-8")
        shared = STYLE.read_text(encoding="utf-8")
        menubar = MENUBAR.read_text(encoding="utf-8")

        self.assertIn(
            "@media screen and (min-width: 801px) and (pointer: coarse) {",
            css,
        )
        self.assertIn(
            "#main.weapon-detail-page .table-scroll > .weapon-data-table",
            css,
        )
        self.assertIn(
            "#main .gigantes-table-scroll",
            shared,
        )
        self.assertIn(
            "min-width: 1100px;",
            shared,
        )
        self.assertIn(
            'var isGigantesPage = /\\/pages\\/gigantes\\.html$/.test(path);',
            menubar,
        )

    def test_weapon_tools_do_not_compute_sticky_header_offsets(self):
        js = JS.read_text(encoding="utf-8")

        self.assertNotIn(
            "--weapon-table-header-sticky-top",
            js,
        )
        self.assertNotIn(
            "toolbar.getBoundingClientRect().height",
            js,
        )
        self.assertNotIn(
            "new ResizeObserver(",
            js,
        )

    def test_legacy_details_sticky_selector_is_removed(self):
        css = CSS.read_text(encoding="utf-8")

        self.assertNotIn(
            "#main .data-toolbar ~ "
            "details table thead th",
            css,
        )
        self.assertNotIn(
            "weapon-child-pending",
            css,
        )

    def test_mobile_layout_rules_remain(self):
        css = CSS.read_text(encoding="utf-8")

        self.assertIn(
            "@media screen and "
            "(max-width: 700px)",
            css,
        )
        self.assertIn(
            "@media screen and "
            "(max-width: 560px)",
            css,
        )


if __name__ == "__main__":
    unittest.main()
