import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIDEBAR_JS = ROOT / "docs" / "js" / "sidebar.js"
INTERACTION_CSS = ROOT / "docs" / "css" / "interaction.css"


class WeaponSidebarTests(unittest.TestCase):
    def test_all_weapon_types_are_nested_below_weapon_data(self):
        js = SIDEBAR_JS.read_text(encoding="utf-8")
        self.assertIn('class="weapon-data-link" href="/PSNOVA/pages/weapon.html">武器データ</a>', js)
        self.assertIn('class="weapon-submenu" aria-label="武器種"', js)

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
                self.assertIn(f'/PSNOVA/pages/weapon/{filename}\">{label}</a>', js)

    def test_weapon_submenu_is_visually_indented(self):
        css = INTERACTION_CSS.read_text(encoding="utf-8")
        self.assertIn("#sub .submenu .weapon-submenu", css)
        self.assertIn("padding: 4px 0 6px 14px;", css)
        self.assertIn("font-size: 12px;", css)
        self.assertIn("#sub .submenu .weapon-submenu a.is-current", css)
        self.assertIn(".weapon-data-link.is-parent-current", css)


if __name__ == "__main__":
    unittest.main()
