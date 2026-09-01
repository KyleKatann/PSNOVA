import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE_ENHANCEMENTS_JS = ROOT / "docs" / "js" / "table-enhancements.js"


class TablePresentationCleanupTests(unittest.TestCase):
    def test_runtime_enhancements_do_not_remove_source_attributes(self):
        js = TABLE_ENHANCEMENTS_JS.read_text(encoding="utf-8")
        self.assertNotIn("removeAttribute(", js)
        self.assertNotIn("bgcolor", js)
        self.assertNotIn("cellpadding", js)
        self.assertNotIn("cellspacing", js)
        self.assertNotIn("valign", js)

    def test_runtime_enhancements_do_not_rewrite_inline_presentation(self):
        js = TABLE_ENHANCEMENTS_JS.read_text(encoding="utf-8")
        self.assertNotIn("style.removeProperty", js)
        self.assertNotIn("border-collapse", js)
        self.assertNotIn("background-color", js)


if __name__ == "__main__":
    unittest.main()
