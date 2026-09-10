from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
WEAPON_PAGE = ROOT / "docs" / "pages" / "weapon.html"
GRANARTS_PAGE = ROOT / "docs" / "pages" / "granarts.html"
PAGE_STYLE = ROOT / "docs" / "css" / "page.css"

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

GRANARTS_ICONS = {
    "ソード": ("sword", "sword.png"),
    "パルチザン": ("partizan", "partizan.png"),
    "ダブルセイバー": ("doublesaber", "dsaber.png"),
    "ナックル": ("knuckle", "knuckle.png"),
    "アサルトライフル": ("rifle", "rifle.png"),
    "ツインマシンガン": ("tmachinegun", "tmachineg.png"),
    "ヘイロウ": ("halo", "halo.png"),
    "パイル": ("pile", "pile.png"),
}

PAGE_STYLE_LINK = (
    '<link rel="stylesheet" href="/PSNOVA/css/page.css" '
    'data-psnova-page-style="true">'
)


class WeaponCatalogIconTests(unittest.TestCase):
    def test_each_weapon_card_has_one_static_native_icon(self):
        html = WEAPON_PAGE.read_text(encoding="utf-8")
        self.assertEqual(11, html.count('class="weapon-card"'))
        for label, filename in ICONS.items():
            pattern = (
                rf'<img src="/PSNOVA/img/weapon/{re.escape(filename)}" '
                rf'alt="" width="48" height="48"(?: loading="lazy")?>'
                rf'<span>{re.escape(label)}</span>'
            )
            self.assertRegex(html, pattern)

    def test_granarts_uses_same_catalog_card_contract_as_weapon_page(self):
        weapon_html = WEAPON_PAGE.read_text(encoding="utf-8")
        granarts_html = GRANARTS_PAGE.read_text(encoding="utf-8")

        self.assertEqual(1, weapon_html.count(PAGE_STYLE_LINK))
        self.assertEqual(1, granarts_html.count(PAGE_STYLE_LINK))
        self.assertEqual(1, granarts_html.count('class="weapon-catalog"'))
        self.assertEqual(8, granarts_html.count('class="weapon-card"'))

        for label, (slug, filename) in GRANARTS_ICONS.items():
            pattern = (
                rf'<a class="weapon-card" '
                rf'href="/PSNOVA/pages/granarts/{re.escape(slug)}\.html">'
                rf'<img src="/PSNOVA/img/weapon/{re.escape(filename)}" '
                rf'alt="" width="48" height="48">'
                rf'<span>{re.escape(label)}</span></a>'
            )
            self.assertRegex(granarts_html, pattern)

    def test_weapon_card_icons_are_forced_visible_by_page_css(self):
        css = PAGE_STYLE.read_text(encoding="utf-8")
        self.assertIn('#main .weapon-card img {', css)
        self.assertIn('display: block !important;', css)
        self.assertIn('visibility: visible;', css)
        self.assertIn('opacity: 1;', css)


if __name__ == "__main__":
    unittest.main()
