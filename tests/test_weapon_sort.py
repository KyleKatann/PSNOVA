import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEAPON_TOOLS_JS = ROOT / "docs" / "js" / "weapon-tools.js"


class WeaponSortTests(unittest.TestCase):
    def test_numeric_sort_options_are_available(self):
        js = WEAPON_TOOLS_JS.read_text(encoding="utf-8")
        self.assertIn('id="weapon-sort"', js)
        for value in (
            'value="rarity-asc"', 'value="rarity-desc"',
            'value="attack-asc"', 'value="attack-desc"',
            'value="shop-asc"', 'value="shop-desc"',
        ):
            with self.subTest(value=value):
                self.assertIn(value, js)

    def test_sort_values_are_derived_from_existing_numeric_cells(self):
        js = WEAPON_TOOLS_JS.read_text(encoding="utf-8")
        self.assertIn("var rarityNumber = numericValue(rarityLabel)", js)
        self.assertIn("var shopNumber = numericValue(shopLabel)", js)
        self.assertIn("rarityNumber: rarityNumber", js)
        self.assertIn("shopNumber: shopNumber", js)
        self.assertIn("attackNumber: maxNumeric(cells, [2, 3, 4])", js)
        self.assertIn("compareNullableNumbers", js)

    def test_original_order_can_be_restored(self):
        js = WEAPON_TOOLS_JS.read_text(encoding="utf-8")
        self.assertIn("originalIndex: index", js)
        self.assertIn("left.originalIndex - right.originalIndex", js)
        self.assertIn("record.parent.appendChild(record.row);", js)


if __name__ == "__main__":
    unittest.main()
