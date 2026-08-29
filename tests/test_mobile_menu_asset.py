import re
import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "docs" / "css" / "style.css"


class MobileMenuAssetTests(unittest.TestCase):
    def test_mobile_menu_icon_reference_exists(self):
        css = STYLE.read_text(encoding="utf-8")
        match = re.search(r"url\((?:['\"]?)(\.\./images/icon_menu\.png)(?:['\"]?)\)", css)
        self.assertIsNotNone(match, "mobile menu CSS should reference ../images/icon_menu.png")

        target = (STYLE.parent / match.group(1)).resolve()
        self.assertTrue(target.is_file(), f"referenced mobile menu icon is missing: {target}")

    def test_mobile_menu_icon_is_expected_sprite_size(self):
        target = ROOT / "docs" / "images" / "icon_menu.png"
        data = target.read_bytes()
        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        width, height = struct.unpack(">II", data[16:24])
        self.assertEqual((width, height), (50, 100))


if __name__ == "__main__":
    unittest.main()
