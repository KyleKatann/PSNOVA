import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEAPON_DIR = ROOT / "docs" / "pages" / "weapon"
ICON_DIR = ROOT / "docs" / "img" / "weapon"

PAGES = {
    "sword": ("ソード", "sword.png"),
    "partizan": ("パルチザン", "partizan.png"),
    "doublesaber": ("ダブルセイバー", "dsaber.png"),
    "rifle": ("アサルトライフル", "rifle.png"),
    "tmachinegun": ("ツインマシンガン", "tmachineg.png"),
    "rod": ("ロッド", "rod.png"),
    "wand": ("ウォンド", "wand.png"),
    "halo": ("ヘイロウ", "halo.png"),
    "pile": ("パイル", "pile.png"),
}

ORDER = [
    ("sword", "ソード"),
    ("partizan", "パルチザン"),
    ("doublesaber", "ダブルセイバー"),
    ("knuckle", "ナックル"),
    ("rifle", "アサルトライフル"),
    ("tmachinegun", "ツインマシンガン"),
    ("rod", "ロッド"),
    ("talis", "タリス"),
    ("wand", "ウォンド"),
    ("halo", "ヘイロウ"),
    ("pile", "パイル"),
]


class RemainingWeaponDetailPageTests(unittest.TestCase):
    def test_pages_use_static_detail_structure(self):
        for filename, (name, icon) in PAGES.items():
            with self.subTest(filename=filename):
                html = (WEAPON_DIR / f"{filename}.html").read_text(
                    encoding="utf-8"
                )

                self.assertIn(
                    f"<title>PSNOVA攻略サイト - {name}</title>",
                    html,
                )
                self.assertIn(
                    f'https://kylekatann.github.io/PSNOVA/'
                    f'pages/weapon/{filename}.html',
                    html,
                )
                self.assertIn(
                    '<div id="main" class="weapon-detail-page">',
                    html,
                )
                self.assertIn(
                    f'src="/PSNOVA/img/weapon/{icon}"',
                    html,
                )
                self.assertTrue((ICON_DIR / icon).is_file())

                self.assertIn('<p class="page-lead">', html)
                self.assertIn(
                    '<nav class="weapon-page-nav" '
                    'aria-label="武器種ナビゲーション">',
                    html,
                )
                self.assertIn(
                    'class="weapon-page-nav-index" '
                    'href="/PSNOVA/pages/weapon.html"',
                    html,
                )
                self.assertIn('<div class="table-scroll">', html)
                self.assertIn(
                    f'<table class="weapon-data-table" '
                    f'data-weapon-static="true" '
                    f'data-weapon-type="{name}">',
                    html,
                )

                self.assertEqual(html.count("<thead>"), 1)
                self.assertEqual(html.count("<tbody>"), 1)

                self.assertNotIn("<details>", html)
                self.assertNotIn("ショップLv", html)
                self.assertNotIn('bgcolor=', html)
                self.assertNotIn('border="1"', html)
                self.assertNotIn(
                    'border-collapse: collapse',
                    html,
                )
                self.assertNotIn(
                    "img/shop/weapon.jpg",
                    html,
                )

                self.assertNotRegex(
                    html,
                    r"<tr><td>[^<]+</td><td>0[1-9]</td>",
                )

                absolute_self_urls = re.findall(
                    r'https://kylekatann\.github\.io/PSNOVA/',
                    html,
                )
                self.assertEqual(len(absolute_self_urls), 1)

    def test_navigation_matches_weapon_order(self):
        index_by_file = {
            filename: index
            for index, (filename, _name) in enumerate(ORDER)
        }

        for filename, (name, _icon) in PAGES.items():
            with self.subTest(filename=filename):
                html = (WEAPON_DIR / f"{filename}.html").read_text(
                    encoding="utf-8"
                )

                index = index_by_file[filename]

                if index > 0:
                    prev_file, prev_name = ORDER[index - 1]
                    self.assertIn(
                        f'href="/PSNOVA/pages/weapon/'
                        f'{prev_file}.html" rel="prev">'
                        f'← {prev_name}</a>',
                        html,
                    )

                if index < len(ORDER) - 1:
                    next_file, next_name = ORDER[index + 1]
                    self.assertIn(
                        f'href="/PSNOVA/pages/weapon/'
                        f'{next_file}.html" rel="next">'
                        f'{next_name} →</a>',
                        html,
                    )

    def test_table_header_is_semantic(self):
        expected = (
            '<tr>'
            '<th scope="col">名前</th>'
            '<th scope="col">レアリティ</th>'
            '<th scope="col">打撃力</th>'
            '<th scope="col">射撃力</th>'
            '<th scope="col">法撃力</th>'
            '<th scope="col">ショップレベル</th>'
            '<th scope="col">必要素材</th>'
            '<th scope="col">備考</th>'
            '</tr>'
        )

        for filename in PAGES:
            with self.subTest(filename=filename):
                html = (WEAPON_DIR / f"{filename}.html").read_text(
                    encoding="utf-8"
                )
                self.assertIn(expected, html)


if __name__ == "__main__":
    unittest.main()
