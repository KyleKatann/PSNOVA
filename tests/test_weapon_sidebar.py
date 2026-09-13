import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIDEBAR_JS = ROOT / "docs" / "js" / "sidebar.js"
OPEN_CLOSE_JS = ROOT / "docs" / "js" / "openclose.js"
STYLE_CSS = ROOT / "docs" / "css" / "style.css"
MODERN_CSS = ROOT / "docs" / "css" / "modern.css"
INTERACTION_CSS = ROOT / "docs" / "css" / "interaction.css"


class WeaponSidebarTests(unittest.TestCase):
    def test_weapon_and_granarts_routes_are_compacted_into_one_group(self):
        js = SIDEBAR_JS.read_text(encoding="utf-8")

        self.assertIn(
            'class="weapon-data-link" href="/PSNOVA/pages/weapon.html">武器・GA</a>',
            js,
        )
        self.assertIn(
            'class="weapon-submenu weapon-ga-submenu" aria-label="武器・GA"',
            js,
        )
        self.assertNotIn(
            'href="/PSNOVA/pages/granarts.html">グランアーツ</a>',
            js,
        )

        weapons = {
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
        for filename, label in weapons.items():
            with self.subTest(label=label):
                self.assertIn(
                    f'class="weapon-route-main" href="/PSNOVA/pages/weapon/{filename}">{label}</a>',
                    js,
                )

        granarts = (
            "sword",
            "partizan",
            "doublesaber",
            "knuckle",
            "rifle",
            "tmachinegun",
            "halo",
            "pile",
        )
        for slug in granarts:
            with self.subTest(granarts=slug):
                self.assertIn(
                    f'class="weapon-route-related-link" href="/PSNOVA/pages/granarts/{slug}.html">GA</a>',
                    js,
                )

        self.assertEqual(
            3,
            js.count(
                'class="weapon-route-related-link weapon-route-tech-link" href="/PSNOVA/pages/technic.html">テクニック</a>'
            ),
        )

    def test_rendered_weapon_menu_uses_full_granarts_label_and_readable_two_columns(self):
        js = OPEN_CLOSE_JS.read_text(encoding="utf-8")
        self.assertIn('parentLink.textContent = "武器・グランアーツ";', js)
        self.assertIn('submenu.setAttribute("aria-label", "武器・グランアーツ");', js)
        self.assertIn('submenu.style.gridTemplateColumns = "repeat(2, minmax(0, 1fr))";', js)
        self.assertIn('row.style.display = "block";', js)
        self.assertIn('mainLink.style.whiteSpace = "nowrap";', js)
        self.assertIn('related.style.display = "block";', js)
        self.assertIn('related.style.minHeight = "0";', js)
        self.assertIn('related.style.fontSize = "9px";', js)
        self.assertIn('related.style.whiteSpace = "nowrap";', js)
        self.assertIn('granartsLink.textContent = "グランアーツ";', js)
        self.assertIn("normalizeWeaponGranartsMenu();", js)

    def test_existing_technic_menu_remains_separate(self):
        js = SIDEBAR_JS.read_text(encoding="utf-8")
        self.assertIn(
            '<a href="/PSNOVA/pages/technic.html">テクニック</a>',
            js,
        )
        self.assertIn(
            'class="weapon-submenu" aria-label="テクニック属性"',
            js,
        )
        for slug, label in (
            ("fire", "炎属性"),
            ("ice", "氷属性"),
            ("thunder", "雷属性"),
            ("wind", "風属性"),
            ("light", "光属性"),
            ("dark", "闇属性"),
        ):
            self.assertIn(
                f'href="/PSNOVA/pages/technic/{slug}.html">{label}</a>',
                js,
            )

    def test_weapon_submenu_style_has_one_owner(self):
        style = STYLE_CSS.read_text(encoding="utf-8")

        self.assertIn("#sub .weapon-submenu {", style)
        self.assertIn("list-style: none;", style)
        self.assertIn(
            "#sub .submenu .weapon-submenu a.is-current",
            style,
        )
        self.assertIn(
            "#sub .submenu a.is-parent-current",
            style,
        )
        self.assertIn(
            "#sub .submenu .weapon-ga-submenu .weapon-route-row {",
            style,
        )
        self.assertIn(
            "#sub .submenu .weapon-ga-submenu .weapon-route-related-link {",
            style,
        )

        self.assertFalse(MODERN_CSS.exists())
        self.assertFalse(INTERACTION_CSS.exists())


if __name__ == "__main__":
    unittest.main()
