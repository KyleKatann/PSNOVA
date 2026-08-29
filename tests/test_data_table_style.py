import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODERN_CSS = ROOT / "docs" / "css" / "modern.css"

class DataTableStyleTests(unittest.TestCase):
    def test_tables_are_flat_and_data_oriented(self):
        css = MODERN_CSS.read_text(encoding="utf-8")
        self.assertIn("/* Data tables */", css)
        self.assertIn("border-collapse: separate;", css)
        self.assertIn("box-shadow: none;", css)
        self.assertIn("font-family: inherit;", css)
        self.assertIn("text-transform: none;", css)

    def test_details_tables_share_consistent_container_style(self):
        css = MODERN_CSS.read_text(encoding="utf-8")
        self.assertIn("details > summary {", css)
        self.assertIn("details[open] > summary", css)
        self.assertIn("details > table {", css)

    def test_tables_scroll_horizontally_on_mobile(self):
        css = MODERN_CSS.read_text(encoding="utf-8")
        self.assertIn("overflow-x: auto;", css)
        self.assertIn("-webkit-overflow-scrolling: touch;", css)

if __name__ == "__main__":
    unittest.main()
