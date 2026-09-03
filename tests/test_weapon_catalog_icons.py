from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WEAPON_PAGE = ROOT / "docs" / "pages" / "weapon.html"
PAGE_STYLE = ROOT / "docs" / "css" / "page.css"
AGENT = ROOT / "Agent.md"

ICONS = {
    "ソード": "sword.png",
    "パルチザン": "partizan.png",
    "ダブルセイバー": "dsaber.png",
    "ナックル": "knuckle.png",
    "アサルトライフル": "rifle.png",
    "ツインマシンガン": "tmachineg.png",
    "ロッド": "rod.png",
    "タリス": "thalys.png",
    "ウォンド": "wand.png",
    "ヘイロウ": "halo.png",
    "パイル": "pile.png",
}


class WeaponCatalogIconTests(unittest.TestCase):
    def test_each_weapon_card_has_one_static_native_icon(self):
        html = WEAPON_PAGE.read_text(encoding="utf-8")
        self.assertEqual(11, html.count('class="weapon-card"'))
        for label, filename in ICONS.items():
            self.assertIn(
                f'<img src="/PSNOVA/img/weapon/{filename}" alt="" width="48" height="48"><span>{label}</span>',
                html,
            )

    def test_weapon_card_icons_are_forced_visible_by_page_css(self):
        css = PAGE_STYLE.read_text(encoding="utf-8")
        self.assertIn('#main .weapon-card img {', css)
        self.assertIn('display: block !important;', css)
        self.assertIn('visibility: visible;', css)
        self.assertIn('opacity: 1;', css)

    def test_catalog_icon_rule_is_recorded(self):
        guide = AGENT.read_text(encoding="utf-8")
        self.assertIn('catalog shows one existing native weapon PNG', guide)
        self.assertIn('must not regress to text-only cards', guide)


if __name__ == "__main__":
    unittest.main()
