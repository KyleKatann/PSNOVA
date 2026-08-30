from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "docs" / "js" / "table-semantics.js"
MATERIAL = ROOT / "docs" / "pages" / "material.html"


class TableNameQuestionMarkCleanupTests(unittest.TestCase):
    def test_first_column_trailing_question_mark_is_stripped_at_runtime(self):
        script = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("stripTrailingQuestionMark(cells[0]);", script)
        self.assertIn('replace(/[?？]+\\s*$/, "")', script)

    def test_uncertain_non_name_values_are_not_targeted(self):
        material = MATERIAL.read_text(encoding="utf-8")
        self.assertIn("Lv180～？", material)
        self.assertIn("SH Lv126?～", material)


if __name__ == "__main__":
    unittest.main()
