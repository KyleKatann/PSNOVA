import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEAPON_DIR = ROOT / "docs" / "pages" / "weapon"

WEAPON_PAGES = {
    "sword.html": "ソード",
    "partizan.html": "パルチザン",
    "doublesaber.html": "ダブルセイバー",
    "knuckle.html": "ナックル",
    "rifle.html": "アサルトライフル",
    "tmachinegun.html": "ツインマシンガン",
    "rod.html": "ロッド",
    "talis.html": "タリス",
    "wand.html": "ウォンド",
    "halo.html": "ヘイロウ",
    "pile.html": "パイル",
}


class WeaponRarityTests(unittest.TestCase):
    def test_rarity_is_not_zero_padded_on_any_weapon_page(self):
        self.assertEqual(
            11,
            len(WEAPON_PAGES),
        )

        for filename, weapon_type in WEAPON_PAGES.items():
            with self.subTest(filename=filename):
                html = (
                    WEAPON_DIR / filename
                ).read_text(
                    encoding="utf-8"
                )

                table = re.search(
                    rf'<table '
                    rf'class="weapon-data-table"'
                    rf'[^>]*'
                    rf'data-weapon-type="'
                    rf'{re.escape(weapon_type)}"'
                    rf'[^>]*>'
                    rf'(.*?)'
                    rf'</table>',
                    html,
                    re.DOTALL,
                )

                self.assertIsNotNone(table)

                self.assertNotRegex(
                    table.group(1),
                    r"<tr>"
                    r"<td>[^<]+</td>"
                    r"<td>0[1-9]</td>",
                )


if __name__ == "__main__":
    unittest.main()
