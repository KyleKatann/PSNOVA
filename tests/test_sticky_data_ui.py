import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "docs" / "css" / "weapon-tools.css"
JS = ROOT / "docs" / "js" / "weapon-tools.js"


class StickyDataUiTests(unittest.TestCase):
    def test_desktop_toolbar_stays_visible_after_scroll(self):
        css = CSS.read_text(
            encoding="utf-8"
        )

        match = re.search(
            r"@media screen and \(min-width: 801px\) \{"
            r"(?P<body>.*?)"
            r"\n\}",
            css,
            re.S,
        )

        self.assertIsNotNone(match)

        body = match.group("body")

        self.assertIn(
            ".data-toolbar { position: sticky; top: 8px; z-index: 30; box-shadow: none; }",
            body,
        )
        self.assertNotIn(
            "#main.weapon-detail-page .data-toolbar",
            css,
        )

    def test_detail_table_header_remains_vertically_sticky(self):
        css = CSS.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "#main .data-toolbar ~ "
            ".table-scroll > "
            ".weapon-data-table thead th",
            css,
        )

        self.assertIn(
            "position: sticky;",
            css,
        )
        self.assertIn(
            "top: var(--weapon-table-header-sticky-top, 180px);",
            css,
        )
        self.assertNotIn(
            "top: 76px;",
            css,
        )

    def test_table_header_offset_tracks_rendered_toolbar_height(self):
        js = JS.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "toolbar.getBoundingClientRect().height",
            js,
        )
        self.assertIn(
            "toolbarStyle.marginBottom",
            js,
        )
        self.assertIn(
            "--weapon-table-header-sticky-top",
            js,
        )
        self.assertIn(
            "new ResizeObserver(",
            js,
        )

    def test_legacy_details_sticky_selector_is_removed(self):
        css = CSS.read_text(
            encoding="utf-8"
        )

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
        css = CSS.read_text(
            encoding="utf-8"
        )

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
