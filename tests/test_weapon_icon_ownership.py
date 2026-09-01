import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
WEAPON_DIR = DOCS / "pages" / "weapon"

ICONS = {
    "sword": "sword.png",
    "partizan": "partizan.png",
    "doublesaber": "dsaber.png",
    "knuckle": "knuckle.png",
    "rifle": "rifle.png",
    "tmachinegun": "tmachineg.png",
    "rod": "rod.png",
    "talis": "thalys.png",
    "wand": "wand.png",
    "halo": "halo.png",
    "pile": "pile.png",
}


class WeaponIconOwnershipTests(unittest.TestCase):
    def test_detail_heading_icons_are_owned_by_static_html(self):
        for slug, icon in ICONS.items():
            with self.subTest(slug=slug):
                html = (
                    WEAPON_DIR / f"{slug}.html"
                ).read_text(
                    encoding="utf-8"
                )

                self.assertEqual(
                    1,
                    html.count(
                        f"/PSNOVA/img/weapon/{icon}"
                    ),
                )

    def test_runtime_weapon_icon_injection_is_removed(self):
        image_layout = (
            DOCS / "js" / "image-layout.js"
        ).read_text(
            encoding="utf-8"
        )

        menubar = (
            DOCS / "js" / "menubar.js"
        ).read_text(
            encoding="utf-8"
        )

        wiki_css = (
            DOCS / "css" / "wiki-table.css"
        ).read_text(
            encoding="utf-8"
        )

        self.assertFalse(
            (
                DOCS
                / "js"
                / "weapon-icons.js"
            ).exists()
        )

        self.assertNotIn(
            "weapon-icons.js",
            menubar,
        )
        self.assertNotIn(
            "var weaponIcons",
            image_layout,
        )
        self.assertNotIn(
            "native-icon-table",
            image_layout,
        )
        self.assertNotIn(
            "native-icon-table",
            wiki_css,
        )


if __name__ == "__main__":
    unittest.main()
