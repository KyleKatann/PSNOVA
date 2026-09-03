import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / "docs" / "js" / "weapon-tools.js"
TABLE_JS = ROOT / "docs" / "js" / "table-enhancements.js"
STYLE = ROOT / "docs" / "css" / "style.css"
PAGE_CSS = ROOT / "docs" / "css" / "page.css"


class CompactWeaponStatusTests(unittest.TestCase):
    def test_rarity_and_shop_cells_are_decorated_without_replacing_text(self):
        js = JS.read_text(encoding="utf-8")
        self.assertIn('classList.add("rarity-cell")', js)
        self.assertIn('setAttribute("data-rarity", String(rarityNumber))', js)
        self.assertIn('classList.add("shop-level-cell")', js)
        self.assertNotIn("cells[1].innerHTML", js)
        self.assertNotIn("cells[1].textContent =", js)

    def test_weapon_rarity_presentation_has_one_sitewide_css_owner(self):
        style = STYLE.read_text(encoding="utf-8")
        page_css = PAGE_CSS.read_text(encoding="utf-8")

        self.assertIn("#main table .rarity-cell::before", style)
        self.assertIn('content: "★"', style)
        self.assertIn('data-rarity="1"', style)
        self.assertIn('data-rarity="15"', style)
        self.assertIn("font-variant-numeric: tabular-nums", style)
        self.assertIn("rarity-source-star::before", style)
        self.assertNotIn("data-rarity-band", style)

        self.assertNotIn(".rarity-cell", page_css)
        self.assertNotIn("data-rarity", page_css)

    def test_shared_tables_reuse_weapon_rarity_contract_without_rewriting_source(self):
        js = TABLE_JS.read_text(encoding="utf-8")

        self.assertIn('cell.classList.add("rarity-cell")', js)
        self.assertIn('cell.setAttribute("data-rarity", String(rarity))', js)
        self.assertIn('cell.classList.add("rarity-source-star")', js)
        self.assertIn('cell.textContent.indexOf("★") !== -1', js)
        self.assertNotIn("data-rarity-band", js)
        self.assertNotIn("rarity-high", js)
        self.assertNotIn("rarity-mid", js)
        self.assertNotIn("rarity-low", js)
        self.assertNotIn("cell.textContent =", js)
        self.assertNotIn("cell.innerHTML", js)

    def test_existing_numeric_sort_inputs_are_preserved(self):
        js = JS.read_text(encoding="utf-8")
        self.assertIn("rarityNumber: rarityNumber", js)
        self.assertIn("shopNumber: shopNumber", js)
        self.assertIn("compareNullableNumbers(left.rarityNumber, right.rarityNumber", js)


if __name__ == "__main__":
    unittest.main()
