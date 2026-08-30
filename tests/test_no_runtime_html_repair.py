import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OLD_NORMALIZER = DOCS / "js" / "table-semantics.js"
TABLE_ENHANCEMENTS = DOCS / "js" / "table-enhancements.js"
MENUBAR = DOCS / "js" / "menubar.js"


class NoRuntimeHtmlRepairTests(unittest.TestCase):
    def test_runtime_table_normalizer_is_removed(self):
        self.assertFalse(
            OLD_NORMALIZER.exists(),
            "Do not repair source HTML at runtime; fix the raw HTML or its generator instead.",
        )

    def test_shared_loader_uses_enhancement_only_table_script(self):
        loader = MENUBAR.read_text(encoding="utf-8")
        self.assertIn("/PSNOVA/js/table-enhancements.js", loader)
        self.assertNotIn("table-semantics.js", loader)
        self.assertNotIn("data-psnova-table-semantics", loader)

    def test_table_enhancements_do_not_repair_source_markup(self):
        script = TABLE_ENHANCEMENTS.read_text(encoding="utf-8")
        forbidden = (
            "createTHead",
            'createElement("thead")',
            'createElement("tbody")',
            'createElement("tr")',
            'createElement("th")',
            'createElement("td")',
            "replaceChild",
            "replaceElementTag",
            "removeAttribute(",
            "bgcolor",
            "stripLegacy",
            "stripTrailingQuestionMark",
            ".outerHTML",
        )
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(
                    token,
                    script,
                    "Table enhancement JavaScript must not repair or normalize source HTML.",
                )

        self.assertIn("decorateSemanticDataTable", script)
        self.assertIn("ensureScrollableTable", script)


if __name__ == "__main__":
    unittest.main()
