from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "docs" / "js" / "table-enhancements.js"
MATERIAL = ROOT / "docs" / "pages" / "material.html"


class TableNameQuestionMarkCleanupTests(unittest.TestCase):
    def test_runtime_table_enhancements_do_not_strip_source_question_marks(self):
        script = SCRIPT.read_text(encoding="utf-8")
        self.assertNotIn("stripTrailingQuestionMark", script)
        self.assertNotIn('replace(/[?？]+\\s*$/, "")', script)
        self.assertNotIn("textContent =", script)

    def test_uncertain_non_name_values_remain_in_static_source(self):
        material = MATERIAL.read_text(encoding="utf-8")
        self.assertIn("Lv180～？", material)
        self.assertIn("SH Lv126?～", material)


if __name__ == "__main__":
    unittest.main()
