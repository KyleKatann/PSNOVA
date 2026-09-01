import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "docs" / "css" / "weapon-tools.css"


class StickyDataUiTests(unittest.TestCase):
    def test_detail_toolbar_scrolls_normally(self):
        css = CSS.read_text(
            encoding="utf-8"
        )

        match = re.search(
            r"#main\.weapon-detail-page "
            r"\.data-toolbar \{"
            r"(?P<body>.*?)"
            r"\}",
            css,
            re.S,
        )

        self.assertIsNotNone(match)

        body = match.group("body")

        self.assertIn(
            "position: static;",
            body,
        )
        self.assertIn(
            "top: auto;",
            body,
        )
        self.assertNotIn(
            "position: sticky",
            body,
        )

    def test_detail_table_header_remains_vertically_sticky(self):
        css = CSS.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "#main.weapon-detail-page "
            ".data-toolbar ~ "
            ".table-scroll > "
            ".weapon-data-table thead th",
            css,
        )

        self.assertIn(
            "position: sticky;",
            css,
        )
        self.assertIn(
            "top: 8px;",
            css,
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
