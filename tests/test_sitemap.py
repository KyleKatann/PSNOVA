import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITEMAP = ROOT / "docs" / "sitemap.xml"


class SitemapTests(unittest.TestCase):
    def test_sitemap_is_valid_xml(self):
        root = ET.parse(SITEMAP).getroot()
        self.assertTrue(root.tag.endswith("urlset"))

    def test_sitemap_contains_core_pages(self):
        xml = SITEMAP.read_text(encoding="utf-8")
        for url in (
            "https://kylekatann.github.io/PSNOVA/",
            "https://kylekatann.github.io/PSNOVA/pages/weapon.html",
            "https://kylekatann.github.io/PSNOVA/pages/material.html",
            "https://kylekatann.github.io/PSNOVA/pages/enemy.html",
            "https://kylekatann.github.io/PSNOVA/pages/trophy.html",
        ):
            with self.subTest(url=url):
                self.assertIn(url, xml)


if __name__ == "__main__":
    unittest.main()
