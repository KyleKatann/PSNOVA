import re
import unittest
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITEMAP = DOCS / "sitemap.xml"
SITE_PREFIX = "https://kylekatann.github.io/PSNOVA/"


class PublicPageVisualAuditTests(unittest.TestCase):
    def public_data_pages(self):
        root = ElementTree.parse(SITEMAP).getroot()
        namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        pages = []
        for loc in root.findall("sm:url/sm:loc", namespace):
            url = (loc.text or "").strip()
            if not url.startswith(SITE_PREFIX):
                continue
            relative = url[len(SITE_PREFIX):]
            if relative.startswith("pages/") and relative.endswith(".html"):
                pages.append(DOCS / relative)
        return pages

    def test_all_sitemap_data_pages_exist(self):
        for path in self.public_data_pages():
            with self.subTest(path=path):
                self.assertTrue(path.exists())

    def test_all_public_data_pages_use_the_shared_visual_shell(self):
        for path in self.public_data_pages():
            html = path.read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertEqual(html.count("<header>"), 1)
                self.assertIn('id="logo"', html)
                self.assertIn('/PSNOVA/css/style.css', html)
                self.assertIn('/PSNOVA/js/menubar.js', html)
                self.assertIn('/PSNOVA/js/sidebar.js', html)
                self.assertIn('<div id="main">', html)
                self.assertRegex(html, r"<h2>[^<]+</h2>")

    def test_public_data_pages_do_not_define_page_specific_inline_stylesheets(self):
        style_block = re.compile(r"<style\b", re.IGNORECASE)
        for path in self.public_data_pages():
            html = path.read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertIsNone(style_block.search(html))


if __name__ == "__main__":
    unittest.main()
