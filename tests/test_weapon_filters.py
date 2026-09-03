import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEAPON_TOOLS_JS = ROOT / "docs" / "js" / "weapon-tools.js"
PAGE_CSS = ROOT / "docs" / "css" / "page.css"


class WeaponFilterTests(unittest.TestCase):
    def test_weapon_filters_are_created_from_existing_data(self):
        js = WEAPON_TOOLS_JS.read_text(encoding="utf-8")
        for control in (
            'id="weapon-type-filter"',
            'id="weapon-rarity-filter"',
            'id="weapon-shop-filter"',
        ):
            with self.subTest(control=control):
                self.assertIn(control, js)
        self.assertIn('uniqueInOrder(records, "type", "typeLabel")', js)
        self.assertIn('uniqueInOrder(records, "rarity", "rarityLabel")', js)
        self.assertIn('uniqueInOrder(records, "shopLevel", "shopLabel")', js)

    def test_filters_are_combined_with_name_search(self):
        js = WEAPON_TOOLS_JS.read_text(encoding="utf-8")
        self.assertIn("record.type === selectedType", js)
        self.assertIn("record.rarity === selectedRarity", js)
        self.assertIn("record.shopLevel === selectedShop", js)
        self.assertIn('typeFilter.addEventListener("change", applyFilters)', js)
        self.assertIn('rarityFilter.addEventListener("change", applyFilters)', js)
        self.assertIn('shopFilter.addEventListener("change", applyFilters)', js)

    def test_filter_controls_are_responsive(self):
        css = PAGE_CSS.read_text(encoding="utf-8")
        self.assertIn("/* === WEAPON PAGES === */", css)
        self.assertIn(".data-filter-grid", css)
        self.assertIn("grid-template-columns: repeat(3, minmax(0, 1fr));", css)
        self.assertIn("grid-template-columns: 1fr;", css)

    def test_hidden_row_rule_is_scoped_to_weapon_tables(self):
        css = PAGE_CSS.read_text(encoding="utf-8")
        self.assertIn(
            "#main .weapon-data-table tr[hidden] { display: none !important; }",
            css,
        )
        self.assertNotIn("\ntr[hidden] {", css)


if __name__ == "__main__":
    unittest.main()
