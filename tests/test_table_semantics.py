import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENUBAR_JS = ROOT / "docs" / "js" / "menubar.js"
TABLE_ENHANCEMENTS_JS = ROOT / "docs" / "js" / "table-enhancements.js"
OLD_TABLE_SEMANTICS_JS = ROOT / "docs" / "js" / "table-semantics.js"


class TableSemanticTests(unittest.TestCase):
    def test_runtime_semantic_normalizer_stays_removed(self):
        loader = MENUBAR_JS.read_text(encoding="utf-8")
        self.assertFalse(OLD_TABLE_SEMANTICS_JS.exists())
        self.assertNotIn("table-semantics.js", loader)
        self.assertNotIn("data-psnova-table-semantics", loader)
        self.assertIn("/PSNOVA/js/table-enhancements.js", loader)

    def test_table_enhancements_only_decorate_existing_semantics(self):
        js = TABLE_ENHANCEMENTS_JS.read_text(encoding="utf-8")
        self.assertIn("decorateSemanticDataTable", js)
        self.assertIn("ensureScrollableTable", js)
        self.assertIn('querySelectorAll("#main table")', js)
        self.assertIn('wrapper.className = "table-scroll"', js)
        self.assertIn('wrapper.setAttribute("tabindex", "0")', js)
        self.assertIn('wrapper.setAttribute("role", "region")', js)
        self.assertIn("findTableRegionLabelSource", js)
        self.assertIn('wrapper.setAttribute("aria-labelledby"', js)
        self.assertIn(
            'wrapper.setAttribute("aria-label", "データ表")',
            js,
        )

    def test_table_enhancements_do_not_create_semantic_structure(self):
        js = TABLE_ENHANCEMENTS_JS.read_text(encoding="utf-8")
        for token in (
            "createTHead",
            'createElement("thead")',
            'createElement("tbody")',
            'createElement("tr")',
            'createElement("th")',
            'createElement("td")',
            "replaceElementTag",
        ):
            with self.subTest(token=token):
                self.assertNotIn(token, js)


if __name__ == "__main__":
    unittest.main()
