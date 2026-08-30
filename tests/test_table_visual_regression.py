import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "docs" / "css"


class TableVisualRegressionTests(unittest.TestCase):
    def test_compact_table_style_does_not_depend_on_runtime_semantic_marker(self):
        css = (CSS / "wiki-table.css").read_text(encoding="utf-8")
        self.assertNotIn('data-psnova-semantic', css)
        self.assertIn('#main table {', css)
        self.assertIn('border-spacing: 1px;', css)
        self.assertIn('background: #eef5ff;', css)
        self.assertIn('tr:first-child > th[bgcolor]', css)

    def test_weapon_table_visual_encoding_is_kept_in_css(self):
        css = (CSS / "weapon-tools.css").read_text(encoding="utf-8")
        self.assertIn('.rarity-cell[data-rarity="1"]', css)
        self.assertIn('.rarity-cell[data-rarity="15"]', css)
        self.assertIn(':nth-child(3):not([bgcolor]):not(:empty)', css)
        self.assertIn('background: #ffcccc;', css)
        self.assertIn('background: #ccddff;', css)
        self.assertIn('background: #ffffcc;', css)
        self.assertIn('background: snow;', css)


if __name__ == "__main__":
    unittest.main()
