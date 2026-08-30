import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENUBAR = ROOT / "docs" / "js" / "menubar.js"
IMAGE_LAYOUT = ROOT / "docs" / "js" / "image-layout.js"
TABLE_CSS = ROOT / "docs" / "css" / "wiki-table.css"


class WikiTableStyleTests(unittest.TestCase):
    def test_compact_table_layer_is_loaded_globally(self):
        js = MENUBAR.read_text(encoding="utf-8")
        self.assertIn('/PSNOVA/css/wiki-table.css', js)
        self.assertIn('data-psnova-wiki-table', js)

    def test_semantic_data_tables_use_compact_gridded_style(self):
        css = TABLE_CSS.read_text(encoding="utf-8")
        self.assertIn('table[data-psnova-semantic="true"]', css)
        self.assertIn('border-spacing: 1px;', css)
        self.assertIn('padding: 6px 7px;', css)
        self.assertIn('background: #c9e7f8;', css)
        self.assertIn('background: #f2f7fc;', css)

    def test_weapon_tables_receive_native_icon_variable(self):
        js = IMAGE_LAYOUT.read_text(encoding="utf-8")
        css = TABLE_CSS.read_text(encoding="utf-8")
        self.assertIn('details.classList.add("native-icon-table")', js)
        self.assertIn('details.style.setProperty("--native-table-icon"', js)
        self.assertIn('background-image: var(--native-table-icon);', css)
        self.assertIn('tbody td:first-child::before', css)

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
