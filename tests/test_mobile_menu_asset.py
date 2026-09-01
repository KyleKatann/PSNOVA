import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "docs" / "css" / "style.css"


class MobileMenuAssetTests(unittest.TestCase):
    def test_mobile_menu_does_not_depend_on_legacy_sprite(self):
        css = STYLE.read_text(encoding="utf-8")

        self.assertNotIn(
            "../images/icon_menu.png",
            css,
        )


if __name__ == "__main__":
    unittest.main()
