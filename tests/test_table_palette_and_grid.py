from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "docs" / "css" / "style.css"
AGENT = ROOT / "Agent.md"


class TablePaletteAndGridTests(unittest.TestCase):
    def test_table_blue_uses_shared_accent_soft_token(self):
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn("background: var(--accent-soft);", css)
        self.assertNotIn("#e0e8f0", css.lower())
        self.assertNotIn("#eef5ff", css.lower())

    def test_table_grid_is_subtle_shared_border(self):
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn("border: 1px solid var(--border);", css)
        self.assertIn("border-right: 1px solid var(--border);", css)
        self.assertIn("border-bottom: 1px solid var(--border);", css)
        self.assertIn("border-spacing: 0;", css)

    def test_agent_records_palette_invariant(self):
        guide = AGENT.read_text(encoding="utf-8")
        self.assertIn("All pale-blue UI surfaces used by data tables", guide)
        self.assertIn("var(--accent-soft)", guide)
        self.assertIn("restrained 1px grid lines", guide)


if __name__ == "__main__":
    unittest.main()
