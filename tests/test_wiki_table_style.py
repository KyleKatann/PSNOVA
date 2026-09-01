import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE_ENTRY = ROOT / "docs" / "css" / "style.css"
IMAGE_LAYOUT = ROOT / "docs" / "js" / "image-layout.js"
TABLE_ENHANCEMENTS = ROOT / "docs" / "js" / "table-enhancements.js"
TABLE_CSS = ROOT / "docs" / "css" / "wiki-table.css"


class WikiTableStyleTests(unittest.TestCase):
    def test_compact_table_layer_is_loaded_globally(self):
        css = STYLE_ENTRY.read_text(encoding="utf-8")
        self.assertIn('@import url("/PSNOVA/css/wiki-table.css");', css)

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
        self.assertIn('details > .table-scroll > table', css)
        self.assertNotIn('details.native-icon-table', css)
        self.assertNotIn('data-psnova-semantic', css)

    def test_current_table_density_palette_and_grid_are_preserved(self):
        css = TABLE_CSS.read_text(encoding="utf-8")
        self.assertIn('border-spacing: 0;', css)
        self.assertIn('padding: 5px;', css)
        self.assertIn('background: var(--accent-soft);', css)
        self.assertIn('border: 1px solid var(--border);', css)
        self.assertIn('border-right: 1px solid var(--border);', css)
        self.assertIn('border-bottom: 1px solid var(--border);', css)
        self.assertNotIn('#e0e8f0', css.lower())
        self.assertNotIn('#eef5ff', css.lower())

    def test_weapon_stat_cell_colors_are_preserved(self):
        css = TABLE_CSS.read_text(encoding="utf-8")
        self.assertIn('.weapon-stat-melee.has-value', css)
        self.assertIn('background: #fff0f0;', css)
        self.assertIn('.weapon-stat-ranged.has-value', css)
        self.assertIn('background: var(--accent-soft);', css)
        self.assertIn('.weapon-stat-tech.has-value', css)
        self.assertIn('background: #fffbe6;', css)
        self.assertIn('.weapon-stat-cell.is-empty', css)
        self.assertIn('background: #e7e9ee;', css)

    def test_weapon_runtime_native_icon_layer_is_removed(self):
        js = IMAGE_LAYOUT.read_text(encoding="utf-8")
        css = TABLE_CSS.read_text(encoding="utf-8")
        self.assertNotIn('details.classList.add("native-icon-table")', js)
        self.assertNotIn('details.style.setProperty("--native-table-icon"', js)
        self.assertNotIn('background-image: var(--native-table-icon);', css)
        self.assertNotIn('details.native-icon-table', css)

    def test_shared_table_enhancer_only_decorates_existing_semantic_tables(self):
        js = TABLE_ENHANCEMENTS.read_text(encoding="utf-8")
        self.assertIn('function decorateSemanticDataTable(table)', js)
        self.assertIn('if (!table || !table.tHead || !table.tBodies.length) return;', js)
        self.assertIn('classList.add("rarity-cell", band)', js)
        self.assertIn('stat-melee', js)
        self.assertIn('stat-ranged', js)
        self.assertIn('stat-tech', js)
        self.assertNotIn('table-semantics', js)
        self.assertNotIn('createTHead', js)

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
