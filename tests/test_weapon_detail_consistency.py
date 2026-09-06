import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEAPON_DIR = ROOT / "docs" / "pages" / "weapon"
CSS = ROOT / "docs" / "css" / "page.css"

PAGES = {
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


class WeaponDetailConsistencyTests(unittest.TestCase):
    def test_all_weapon_pages_share_static_structure(self):
        for slug, name in PAGES.items():
            with self.subTest(slug=slug):
                html = (WEAPON_DIR / f"{slug}.html").read_text(
                    encoding="utf-8"
                )

                self.assertIn(
                    f"<title>PSNOVA攻略サイト - {name}</title>",
                    html,
                )
                self.assertIn(
                    '<main id="main" class="weapon-detail-page">',
                    html,
                )
                self.assertIn(
                    '<div class="table-scroll">',
                    html,
                )
                self.assertIn(
                    f'data-weapon-type="{name}"',
                    html,
                )
                self.assertNotIn("<details>", html)

    def test_weapon_pages_keep_only_catalog_navigation(self):
        for slug in PAGES:
            with self.subTest(slug=slug):
                html = (WEAPON_DIR / f"{slug}.html").read_text(
                    encoding="utf-8"
                )

                self.assertIn(
                    '<a class="weapon-page-nav-index" href="/PSNOVA/pages/weapon.html">武器一覧</a>',
                    html,
                )
                self.assertNotIn('rel="prev"', html)
                self.assertNotIn('rel="next"', html)

    def test_detail_table_header_remains_in_normal_flow(self):
        css = CSS.read_text(encoding="utf-8")

        self.assertNotIn(
            ".weapon-data-table thead th",
            css,
        )
        self.assertNotIn(
            "--weapon-table-header-sticky-top",
            css,
        )
        self.assertNotIn(
            "top: 76px;",
            css,
        )


if __name__ == "__main__":
    unittest.main()
