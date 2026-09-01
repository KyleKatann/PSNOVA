import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIDEBAR_JS = ROOT / "docs" / "js" / "sidebar.js"
MODERN_CSS = ROOT / "docs" / "css" / "modern.css"
INTERACTION_CSS = ROOT / "docs" / "css" / "interaction.css"


class WeaponSidebarTests(unittest.TestCase):
    def test_all_weapon_types_are_nested_below_weapon_data(self):
        js = SIDEBAR_JS.read_text(encoding="utf-8")

        self.assertIn(
            'class="weapon-data-link" href="/PSNOVA/pages/weapon.html">武器データ</a>',
            js,
        )
        self.assertIn(
            'class="weapon-submenu" aria-label="武器種"',
            js,
        )

        expected = {
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

        for filename, label in expected.items():
            with self.subTest(label=label):
                self.assertIn(
                    f'/PSNOVA/pages/weapon/{filename}">{label}</a>',
                    js,
                )

    def test_weapon_submenu_style_has_one_owner(self):
        modern = MODERN_CSS.read_text(
            encoding="utf-8"
        )
        interaction = INTERACTION_CSS.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "#sub .weapon-submenu {",
            modern,
        )
        self.assertIn(
            "list-style: none;",
            modern,
        )
        self.assertIn(
            "#sub .submenu .weapon-submenu a.is-current",
            modern,
        )
        self.assertIn(
            "#sub .submenu a.is-parent-current",
            modern,
        )

        self.assertNotIn(
            ".weapon-submenu",
            interaction,
        )


if __name__ == "__main__":
    unittest.main()
