import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "docs" / "pages"

WEAPONS = {
    "sword": "ソード",
    "partizan": "パルチザン",
    "doublesaber": "ダブルセイバー",
    "knuckle": "ナックル",
    "rifle": "アサルトライフル",
    "tmachinegun": "ツインマシンガン",
    "rod": "ロッド",
    "talis": "タリス",
    "wand": "ウォンド",
    "halo": "ヘイロウ",
    "pile": "パイル",
}


class WeaponPageSplitTests(unittest.TestCase):
    def test_weapon_index_is_lightweight_catalog(self):
        html = (PAGES / "weapon.html").read_text(encoding="utf-8")
        self.assertIn('class="weapon-catalog"', html)
        self.assertNotIn("<details>", html)
        self.assertNotIn('meta name="keywords"', html)

        for slug, label in WEAPONS.items():
            self.assertIn(
                f"/PSNOVA/pages/weapon/{slug}.html",
                html,
            )
            self.assertIn(label, html)

    def test_weapon_child_routes_are_static(self):
        for slug, label in WEAPONS.items():
            with self.subTest(slug=slug):
                path = PAGES / "weapon" / f"{slug}.html"
                self.assertTrue(path.exists())

                html = path.read_text(encoding="utf-8")

                self.assertIn(
                    '<div id="main" class="weapon-detail-page">',
                    html,
                )
                self.assertIn(
                    f'data-weapon-type="{label}"',
                    html,
                )

                self.assertNotIn("<details", html)
                self.assertNotIn("<summary", html)
                self.assertNotIn(
                    'meta name="keywords"',
                    html,
                )

    def test_weapon_tools_has_no_legacy_child_adapter(self):
        js = (
            ROOT / "docs" / "js" / "weapon-tools.js"
        ).read_text(encoding="utf-8")

        for slug, label in WEAPONS.items():
            self.assertIn(
                f'slug: "{slug}"',
                js,
            )
            self.assertIn(
                f'label: "{label}"',
                js,
            )

        for token in (
            "prepareLegacyChildPage",
            "details.remove();",
            "selected.open = true;",
            'querySelectorAll("details")',
            "section.details",
        ):
            with self.subTest(token=token):
                self.assertNotIn(token, js)

    def test_shared_navigation_understands_weapon_children(self):
        menubar = (
            ROOT / "docs" / "js" / "menubar.js"
        ).read_text(encoding="utf-8")

        sidebar = (
            ROOT / "docs" / "js" / "sidebar.js"
        ).read_text(encoding="utf-8")

        self.assertIn(
            'weapon(?:\\.html|\\/[^/]+\\.html)',
            menubar,
        )
        self.assertIn(
            "weaponChild",
            sidebar,
        )
        self.assertIn(
            "/PSNOVA/pages/weapon.html",
            sidebar,
        )


if __name__ == "__main__":
    unittest.main()
