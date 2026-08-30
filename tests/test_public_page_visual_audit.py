import re
import unittest
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITEMAP = DOCS / "sitemap.xml"
WEAPON_DIR = DOCS / "pages" / "weapon"
SITE_PREFIX = "https://kylekatann.github.io/PSNOVA/"


class PublicPageVisualAuditTests(unittest.TestCase):
    def sitemap_pages(self):
        root = ElementTree.parse(SITEMAP).getroot()
        namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        pages = []
        for loc in root.findall("sm:url/sm:loc", namespace):
            url = (loc.text or "").strip()
            if not url.startswith(SITE_PREFIX):
                continue
            relative = url[len(SITE_PREFIX):]
            relative = relative or "index.html"
            pages.append(DOCS / relative)
        return pages

    def primary_public_pages(self):
        pages = set(self.sitemap_pages())
        pages.update(WEAPON_DIR.glob("*.html"))
        return sorted(pages)

    def test_all_primary_public_pages_exist(self):
        for path in self.primary_public_pages():
            with self.subTest(path=path):
                self.assertTrue(path.exists())

    def test_every_primary_public_page_uses_the_shared_visual_shell(self):
        for path in self.primary_public_pages():
            html = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(DOCS)):
                self.assertEqual(html.count("<header>"), 1)
                self.assertIn('id="logo"', html)
                self.assertIn('/PSNOVA/css/style.css', html)
                self.assertIn('/PSNOVA/js/menubar.js', html)
                self.assertIn('/PSNOVA/js/sidebar.js', html)
                self.assertIn('<div id="main">', html)
                self.assertRegex(html, r"<h2>[^<]+</h2>")

    def test_primary_public_pages_do_not_define_page_specific_inline_stylesheets(self):
        style_block = re.compile(r"<style\b", re.IGNORECASE)
        for path in self.primary_public_pages():
            html = path.read_text(encoding="utf-8")
            with self.subTest(path=path.relative_to(DOCS)):
                self.assertIsNone(style_block.search(html))

    def test_primary_public_data_table_headers_use_header_cells(self):
        table_pattern = re.compile(r"<table\b[^>]*>(.*?)</table>", re.IGNORECASE | re.DOTALL)
        first_row_pattern = re.compile(r"<tr\b[^>]*>(.*?)</tr>", re.IGNORECASE | re.DOTALL)
        legacy_td_header = re.compile(r"<td\b[^>]*\bbgcolor\s*=", re.IGNORECASE)

        for path in self.primary_public_pages():
            html = path.read_text(encoding="utf-8")
            for table_index, table_match in enumerate(table_pattern.finditer(html), start=1):
                first_row = first_row_pattern.search(table_match.group(1))
                if not first_row:
                    continue
                with self.subTest(path=path.relative_to(DOCS), table=table_index):
                    self.assertIsNone(
                        legacy_td_header.search(first_row.group(1)),
                        "Table headers must use th cells so every page receives the shared header design.",
                    )

    def test_primary_public_table_cells_stay_inside_explicit_rows(self):
        table_pattern = re.compile(r"<table\b[^>]*>(.*?)</table>", re.IGNORECASE | re.DOTALL)
        row_pattern = re.compile(r"<tr\b[^>]*>.*?</tr>", re.IGNORECASE | re.DOTALL)
        row_start_pattern = re.compile(r"<tr\b", re.IGNORECASE)
        row_end_pattern = re.compile(r"</tr\s*>", re.IGNORECASE)
        cell_pattern = re.compile(r"<(?:td|th)\b", re.IGNORECASE)

        for path in self.primary_public_pages():
            html = path.read_text(encoding="utf-8")
            for table_index, table_match in enumerate(table_pattern.finditer(html), start=1):
                table_html = table_match.group(1)
                with self.subTest(path=path.relative_to(DOCS), table=table_index):
                    self.assertEqual(
                        len(row_start_pattern.findall(table_html)),
                        len(row_end_pattern.findall(table_html)),
                        "Every table row must have an explicit closing </tr>; do not rely on browser repair.",
                    )

                    outside_rows = row_pattern.sub("", table_html)
                    self.assertIsNone(
                        cell_pattern.search(outside_rows),
                        "Table cells must be contained by an explicit <tr>...</tr> row.",
                    )


if __name__ == "__main__":
    unittest.main()
