import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE_SEMANTICS_JS = ROOT / "docs" / "js" / "table-semantics.js"


class TablePresentationCleanupTests(unittest.TestCase):
    def test_cleanup_is_limited_to_details_data_tables(self):
        js = TABLE_SEMANTICS_JS.read_text(encoding="utf-8")
        self.assertIn('querySelectorAll("details table")', js)
        self.assertNotIn('querySelectorAll("table")', js)

    def test_deprecated_table_attributes_are_removed(self):
        js = TABLE_SEMANTICS_JS.read_text(encoding="utf-8")
        for attribute in ("border", "cellpadding", "cellspacing", "bgcolor", "align", "valign"):
            with self.subTest(attribute=attribute):
                self.assertIn('"' + attribute + '"', js)
        self.assertIn("removeAttribute(attribute)", js)

    def test_legacy_inline_table_presentation_is_removed(self):
        js = TABLE_SEMANTICS_JS.read_text(encoding="utf-8")
        self.assertIn('style.removeProperty("border-collapse")', js)
        self.assertIn('style.removeProperty("background-color")', js)
        self.assertIn('style.removeProperty("border")', js)


if __name__ == "__main__":
    unittest.main()
