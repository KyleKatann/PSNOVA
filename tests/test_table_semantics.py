import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENUBAR_JS = ROOT / "docs" / "js" / "menubar.js"
TABLE_SEMANTICS_JS = ROOT / "docs" / "js" / "table-semantics.js"


class TableSemanticTests(unittest.TestCase):
    def test_semantic_normalizer_is_loaded_globally(self):
        js = MENUBAR_JS.read_text(encoding="utf-8")
        self.assertIn("/PSNOVA/js/table-semantics.js", js)
        self.assertIn("data-psnova-table-semantics", js)

    def test_only_details_data_tables_are_normalized(self):
        js = TABLE_SEMANTICS_JS.read_text(encoding="utf-8")
        self.assertIn('querySelectorAll("details table")', js)
        self.assertNotIn('querySelectorAll("table")', js)

    def test_header_and_body_semantics_are_created(self):
        js = TABLE_SEMANTICS_JS.read_text(encoding="utf-8")
        self.assertIn('replaceElementTag(cell, "th")', js)
        self.assertIn('headerCell.setAttribute("scope", "col")', js)
        self.assertIn("table.createTHead()", js)
        self.assertIn('replaceElementTag(cell, "td")', js)

    def test_normalization_is_idempotent(self):
        js = TABLE_SEMANTICS_JS.read_text(encoding="utf-8")
        self.assertIn('table.dataset.psnovaSemantic === "true"', js)
        self.assertIn('table.dataset.psnovaSemantic = "true"', js)


if __name__ == "__main__":
    unittest.main()
