import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class WeaponSitemapCoverageTests(unittest.TestCase):
    def test_all_weapon_child_pages_are_in_sitemap(self):
        sitemap = (DOCS / "sitemap.xml").read_text(encoding="utf-8")
        weapon_pages = sorted((DOCS / "pages" / "weapon").glob("*.html"))
        self.assertEqual(11, len(weapon_pages))
        for page in weapon_pages:
            url = f"https://kylekatann.github.io/PSNOVA/pages/weapon/{page.name}"
            self.assertIn(url, sitemap)


if __name__ == "__main__":
    unittest.main()
