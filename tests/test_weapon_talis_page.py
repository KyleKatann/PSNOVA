import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "pages" / "weapon" / "talis.html"


class TalisWeaponPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")

    def test_weapon_detail_structure(self):
        self.assertIn('<main id="main" class="weapon-detail-page">', self.html)
        self.assertIn(
            '<img class="weapon-type-icon" src="/PSNOVA/img/weapon/thalys.png"',
            self.html,
        )
        self.assertIn('<p class="page-lead">', self.html)
        self.assertIn('<div class="table-scroll">', self.html)
        self.assertIn(
            '<table class="weapon-data-table" '
            'data-weapon-static="true" data-weapon-type="タリス">',
            self.html,
        )

    def test_weapon_navigation(self):
        self.assertIn(
            'href="/PSNOVA/pages/weapon/rod.html" rel="prev">← ロッド</a>',
            self.html,
        )
        self.assertIn(
            'class="weapon-page-nav-index" '
            'href="/PSNOVA/pages/weapon.html">武器一覧</a>',
            self.html,
        )
        self.assertIn(
            'href="/PSNOVA/pages/weapon/wand.html" '
            'rel="next">ウォンド →</a>',
            self.html,
        )

    def test_legacy_weapon_markup_is_removed(self):
        self.assertNotIn('border="1"', self.html)
        self.assertNotIn('bgcolor=', self.html)
        self.assertNotIn('img/shop/weapon.jpg', self.html)

    def test_repo_assets_are_site_relative(self):
        absolute_refs = re.findall(
            r'(?:href|src)="https://kylekatann\.github\.io/PSNOVA/[^"]+"',
            self.html,
        )
        self.assertEqual(
            absolute_refs,
            [
                'href="https://kylekatann.github.io/PSNOVA/'
                'pages/weapon/talis.html"'
            ],
        )


if __name__ == "__main__":
    unittest.main()
