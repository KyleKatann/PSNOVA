import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENUBAR = ROOT / "docs" / "js" / "menubar.js"
IMAGE_LAYOUT = ROOT / "docs" / "js" / "image-layout.js"
TABLE_SEMANTICS = ROOT / "docs" / "js" / "table-semantics.js"
TABLE_CSS = ROOT / "docs" / "css" / "wiki-table.css"


class WikiTableStyleTests(unittest.TestCase):
    def test_compact_table_layer_is_loaded_globally(self):
        js = MENUBAR.read_text(encoding="utf-8")
        self.assertIn('/PSNOVA/css/wiki-table.css', js)
        self.assertIn('data-psnova-wiki-table', js)

    def test_every_table_scroll_wrapper_supports_touch_horizontal_scrolling(self):
        css = TABLE_CSS.read_text(encoding="utf-8")
        self.assertIn('#main .table-scroll', css)
        self.assertIn('max-width: 100%;', css)
        self.assertIn('overflow-x: auto;', css)
        self.assertIn('-webkit-overflow-scrolling: touch;', css)
        self.assertIn('overscroll-behavior-inline: contain;', css)
        self.assertIn('touch-action: pan-x pan-y;', css)

    def test_mobile_table_itself_is_not_a_nested_scroll_container(self):
        css = TABLE_CSS.read_text(encoding="utf-8")
        self.assertIn('#main .table-scroll > table', css)
        self.assertIn('display: table;', css)
        self.assertIn('overflow: visible;', css)
        self.assertIn('white-space: normal;', css)

    def test_details_table_selectors_work_after_scroll_wrapper_is_inserted(self):
        css = TABLE_CSS.read_text(encoding="utf-8")
        self.assertIn('details > .table-scroll > table[data-psnova-semantic="true"]', css)
        self.assertIn('details.native-icon-table > .table-scroll > table[data-psnova-semantic="true"]', css)

    def test_archived_table_density_and_base_colors_are_preserved(self):
        css = TABLE_CSS.read_text(encoding="utf-8")
        self.assertIn('table[data-psnova-semantic="true"]', css)
        self.assertIn('background: #ccd5dd;', css)
        self.assertIn('border-spacing: 1px;', css)
        self.assertIn('padding: 5px;', css)
        self.assertIn('background: #e0e8f0;', css)
        self.assertIn('background: #eef5ff;', css)

    def test_archived_weapon_and_armor_stat_cell_colors_are_preserved(self):
        css = TABLE_CSS.read_text(encoding="utf-8")
        self.assertIn('.weapon-stat-melee.has-value', css)
        self.assertIn('background: #ffcccc;', css)
        self.assertIn('.weapon-stat-ranged.has-value', css)
        self.assertIn('background: #ccddff;', css)
        self.assertIn('.weapon-stat-tech.has-value', css)
        self.assertIn('background: #ffffcc;', css)
        self.assertIn('.weapon-stat-cell.is-empty', css)
        self.assertIn('background: #e0e0e0;', css)
        self.assertIn('background: snow;', css)

    def test_weapon_tables_receive_native_icon_variable(self):
        js = IMAGE_LAYOUT.read_text(encoding="utf-8")
        css = TABLE_CSS.read_text(encoding="utf-8")
        self.assertIn('details.classList.add("native-icon-table")', js)
        self.assertIn('details.style.setProperty("--native-table-icon"', js)
        self.assertIn('background-image: var(--native-table-icon);', css)
        self.assertIn('tbody td:first-child::before', css)

    def test_shared_semantic_decorator_supplies_rarity_and_stat_classes(self):
        js = TABLE_SEMANTICS.read_text(encoding="utf-8")
        self.assertIn('data-rarity-band', js)
        self.assertIn('weapon-stat-melee', js)
        self.assertIn('weapon-stat-ranged', js)
        self.assertIn('weapon-stat-tech', js)
        self.assertIn('shop-level-cell', js)

    def test_archived_rarity_color_bands_are_present(self):
        css = TABLE_CSS.read_text(encoding="utf-8")
        for band, color in (
            ('blue', 'deepskyblue'),
            ('green', 'limegreen'),
            ('red', 'orangered'),
            ('orange', 'orange'),
            ('violet', 'violet'),
        ):
            with self.subTest(band=band):
                self.assertIn(f'data-rarity-band="{band}"', css)
                self.assertIn(f'color: {color};', css)

    def test_all_native_weapon_icon_assets_exist(self):
        for filename in (
            "sword.png", "partizan.png", "dsaber.png", "knuckle.png",
            "rifle.png", "tmachineg.png", "rod.png", "thalys.png",
            "wand.png", "halo.png", "pile.png",
        ):
            with self.subTest(filename=filename):
                self.assertTrue((ROOT / "docs" / "img" / "weapon" / filename).exists())


if __name__ == "__main__":
    unittest.main()
