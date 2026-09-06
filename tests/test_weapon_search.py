import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEAPON_HTML = ROOT / "docs" / "pages" / "weapon.html"
KNUCKLE_HTML = ROOT / "docs" / "pages" / "weapon" / "knuckle.html"


class WeaponPageTests(unittest.TestCase):
    def test_weapon_landing_page_is_catalog_not_embedded_data_copy(self):
        html = WEAPON_HTML.read_text(encoding="utf-8")
        self.assertIn('class="weapon-catalog"', html)
        self.assertEqual(11, html.count('class="weapon-card"'))
        self.assertNotIn("<table", html)
        self.assertNotIn("<details", html)

    def test_static_weapon_child_preserves_data_sentinels(self):
        html = KNUCKLE_HTML.read_text(encoding="utf-8")
        for value in ("ナックル", "エイトオンス", "ノヴァクローグ", "ファイバーロア"):
            with self.subTest(value=value):
                self.assertIn(value, html)


if __name__ == "__main__":
    unittest.main()
