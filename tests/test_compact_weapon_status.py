import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / "docs" / "js" / "weapon-tools.js"
CSS = ROOT / "docs" / "css" / "weapon-tools.css"


class CompactWeaponStatusTests(unittest.TestCase):
    def test_rarity_and_shop_cells_are_decorated_without_replacing_text(self):
        js = JS.read_text(encoding="utf-8")
        self.assertIn('classList.add("rarity-cell")', js)
        self.assertIn('setAttribute("data-rarity", String(rarityNumber))', js)
        self.assertIn('classList.add("shop-level-cell")', js)
        self.assertNotIn("cells[1].innerHTML", js)
        self.assertNotIn("cells[1].textContent =", js)

    def test_rarity_uses_restrained_css_badge(self):
        css = CSS.read_text(encoding="utf-8")
        self.assertIn(".rarity-cell::before", css)
        self.assertIn('content: "★"', css)
        self.assertIn("font-variant-numeric: tabular-nums", css)

    def test_existing_numeric_sort_inputs_are_preserved(self):
        js = JS.read_text(encoding="utf-8")
        self.assertIn("rarityNumber: rarityNumber", js)
        self.assertIn("shopNumber: shopNumber", js)
        self.assertIn("compareNullableNumbers(left.rarityNumber, right.rarityNumber", js)


if __name__ == "__main__":
    unittest.main()
