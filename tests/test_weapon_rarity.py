import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEAPON_PAGES = {
    "rod.html": "ロッド",
    "talis.html": "タリス",
}


class WeaponRarityTests(unittest.TestCase):
    def test_rarity_is_not_zero_padded(self):
        for filename, weapon_type in WEAPON_PAGES.items():
            html = (ROOT / "docs" / "pages" / "weapon" / filename).read_text(encoding="utf-8")
            legacy_section = re.search(
                rf"<summary>{re.escape(weapon_type)}</summary>(.*?)</details>",
                html,
                re.DOTALL,
            )
            scope = legacy_section.group(1) if legacy_section else html

            with self.subTest(filename=filename):
                self.assertNotRegex(
                    scope,
                    r"<tr><(?:th|td)>[^<]+</(?:th|td)><(?:th|td)>0[1-9]</(?:th|td)>",
                )


if __name__ == "__main__":
    unittest.main()
