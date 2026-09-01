import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEAPON_PAGES = (
    "rod.html",
    "talis.html",
    "wand.html",
    "halo.html",
    "pile.html",
)


class WeaponRarityTests(unittest.TestCase):
    def test_rarity_is_not_zero_padded(self):
        for filename in WEAPON_PAGES:
            html = (ROOT / "docs" / "pages" / "weapon" / filename).read_text(encoding="utf-8")
            with self.subTest(filename=filename):
                self.assertNotRegex(html, r"<tr><th>[^<]+</th><th>0[1-9]</th>")


if __name__ == "__main__":
    unittest.main()
