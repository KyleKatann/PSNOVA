import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "docs" / "css"


class TableVisualRegressionTests(unittest.TestCase):
    def test_compact_table_style_does_not_depend_on_runtime_semantic_marker(self):
        css = (CSS / "wiki-table.css").read_text(encoding="utf-8")
        self.assertNotIn("data-psnova-semantic", css)
        self.assertIn("#main table {", css)
        self.assertIn("border-spacing: 0;", css)
        self.assertIn("background: var(--surface);", css)
        self.assertIn("background: var(--accent-soft);", css)
        self.assertIn("border: 1px solid var(--border);", css)
        self.assertNotIn("#eef5ff", css.lower())
        self.assertNotIn("#e0e8f0", css.lower())

    def test_weapon_table_visual_encoding_is_kept_in_shared_table_css(self):
        css = (CSS / "wiki-table.css").read_text(encoding="utf-8")
        self.assertIn('.rarity-cell[data-rarity-band="blue"]', css)
        self.assertIn('.rarity-cell[data-rarity-band="violet"]', css)
        self.assertIn('.weapon-stat-melee.has-value', css)
        self.assertIn('background: #fff0f0;', css)
        self.assertIn('.weapon-stat-ranged.has-value', css)
        self.assertIn('background: var(--accent-soft);', css)
        self.assertIn('.weapon-stat-tech.has-value', css)
        self.assertIn('background: #fffbe6;', css)
        self.assertIn('.weapon-stat-cell.is-empty', css)
        self.assertIn('background: #e7e9ee;', css)


if __name__ == "__main__":
    unittest.main()
