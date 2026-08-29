import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE_CSS = ROOT / "docs" / "css" / "style.css"


class LegacyCssCleanupTests(unittest.TestCase):
    def test_oversized_duplicate_image_rule_is_removed(self):
        css = STYLE_CSS.read_text(encoding="utf-8")
        self.assertNotIn("max-width: 200%", css)
        self.assertNotIn("max-width:200%", css)
        self.assertIn("max-width: 100%", css.replace("max-width:100%", "max-width: 100%"))

    def test_duplicate_global_table_design_block_is_removed(self):
        css = STYLE_CSS.read_text(encoding="utf-8")
        self.assertNotIn("box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1)", css)
        self.assertNotIn("font-family: Arial, sans-serif", css)
        self.assertNotIn("background-color: #e6f7ff", css)

    def test_base_table_reset_remains(self):
        css = STYLE_CSS.read_text(encoding="utf-8")
        compact = "".join(css.split())
        self.assertIn("table{border-collapse:collapse;font-size:100%;border-spacing:0;}", compact)


if __name__ == "__main__":
    unittest.main()
