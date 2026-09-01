import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEAPON_DIR = ROOT / "docs" / "pages" / "weapon"
CSS = ROOT / "docs" / "css" / "weapon-tools.css"

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
                    '<div id="main" class="weapon-detail-page">',
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

    def test_detail_toolbar_is_not_sticky(self):
        css = CSS.read_text(encoding="utf-8")

        self.assertIn(
            "#main.weapon-detail-page .data-toolbar {",
            css,
        )
        self.assertIn(
            "position: static;",
            css,
        )

    def test_detail_table_header_remains_sticky(self):
        css = CSS.read_text(encoding="utf-8")

        self.assertIn(
            "#main.weapon-detail-page .data-toolbar ~ "
            ".table-scroll > .weapon-data-table thead th",
            css,
        )
        self.assertIn("top: 8px;", css)

    def test_desktop_navigation_columns_are_explicit(self):
        css = CSS.read_text(encoding="utf-8")

        self.assertIn(
            '.weapon-page-nav a[rel="prev"] { grid-column: 1; }',
            css,
        )
        self.assertIn(
            ".weapon-page-nav-index { grid-column: 2; }",
            css,
        )
        self.assertIn(
            '.weapon-page-nav a[rel="next"] { grid-column: 3; }',
            css,
        )


if __name__ == "__main__":
    unittest.main()
