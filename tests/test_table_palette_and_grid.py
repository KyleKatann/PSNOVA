from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "docs" / "css" / "style.css"
PAGE_STYLE = ROOT / "docs" / "css" / "page.css"


class TablePaletteAndGridTests(unittest.TestCase):
    def test_table_blue_uses_shared_accent_soft_token(self):
        css = STYLE.read_text(encoding="utf-8")
        page_css = PAGE_STYLE.read_text(encoding="utf-8")

        self.assertIn("background: var(--accent-soft);", css)
        for legacy_color in ("#e0e8f0", "#eef5ff", "#f5f6ff"):
            self.assertNotIn(legacy_color, css.lower())
            self.assertNotIn(legacy_color, page_css.lower())

        self.assertRegex(
            page_css,
            r"#main\.technic-detail-page \.technic-level-table caption \{[^}]*"
            r"background: var\(--accent-soft\);",
        )
        self.assertRegex(
            page_css,
            r"#main\.technic-detail-page \.technic-level-table thead th \{[^}]*"
            r"background: var\(--accent-soft\);",
        )
        self.assertRegex(
            page_css,
            r"#main\.technic-detail-page \.technic-level-table tbody tr:first-child > th,"
            r"[^}]*background: var\(--accent-soft\);",
        )

    def test_table_grid_is_subtle_shared_border(self):
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn("border: 1px solid var(--border);", css)
        self.assertIn("border-right: 1px solid var(--border);", css)
        self.assertIn("border-bottom: 1px solid var(--border);", css)
        self.assertIn("border-spacing: 0;", css)


if __name__ == "__main__":
    unittest.main()
