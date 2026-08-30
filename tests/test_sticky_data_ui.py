import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "docs" / "css" / "weapon-tools.css"


class StickyDataUiTests(unittest.TestCase):
    def test_toolbar_is_sticky_on_desktop(self):
        css = CSS.read_text(encoding="utf-8")
        self.assertIn("@media screen and (min-width: 801px)", css)
        self.assertIn(".data-toolbar", css)
        self.assertIn("position: sticky", css)
        self.assertIn("top: 8px", css)

    def test_table_header_is_sticky_only_after_weapon_toolbar(self):
        css = CSS.read_text(encoding="utf-8")
        self.assertIn("#main .data-toolbar ~ details table thead th", css)
        self.assertNotIn("#main details table thead th", css)
        self.assertIn("top: 76px", css)

    def test_mobile_layout_rules_remain(self):
        css = CSS.read_text(encoding="utf-8")
        self.assertIn("@media screen and (max-width: 700px)", css)
        self.assertIn("@media screen and (max-width: 560px)", css)


if __name__ == "__main__":
    unittest.main()
