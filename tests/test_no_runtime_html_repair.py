import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OLD_NORMALIZER = DOCS / "js" / "table-semantics.js"
TABLE_ENHANCEMENTS = DOCS / "js" / "menubar.js"
MENUBAR = TABLE_ENHANCEMENTS


class NoRuntimeHtmlRepairTests(unittest.TestCase):
    def test_runtime_table_normalizer_is_removed(self):
        self.assertFalse(
            OLD_NORMALIZER.exists(),
            "実行時にソースHTMLを修復してはならない。生HTMLまたは生成元を修正すること。",
        )

    def test_shared_bundle_contains_enhancement_only_table_logic(self):
        loader = MENUBAR.read_text(encoding="utf-8")
        self.assertIn("decorateSemanticDataTable", loader)
        self.assertIn("ensureScrollableTable", loader)
        self.assertNotIn("/PSNOVA/js/table-enhancements.js", loader)
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
                    "テーブル拡張JavaScriptでソースHTMLを修復または正規化してはならない。",
                )

        removed_attributes = set(
            re.findall(
                r'removeAttribute\("([^"]+)"\)',
                script,
            )
        )
        self.assertLessEqual(
            removed_attributes,
            {"aria-label", "aria-labelledby"},
            "実行時に切り替えてよいのはアクセシビリティ上の命名属性だけであり、"
            "ソースHTMLの属性を削除してはならない。",
        )

        self.assertIn("decorateSemanticDataTable", script)
        self.assertIn("ensureScrollableTable", script)


if __name__ == "__main__":
    unittest.main()
