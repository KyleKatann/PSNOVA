import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
PAGE_STYLE = ROOT / "docs" / "css" / "page.css"
SHARED_STYLE = ROOT / "docs" / "css" / "style.css"

PACKAGE = "/PSNOVA/img/home/psnova-vita-package.jpg"
LOGOS = {
    "PSNOVA 公式サイト": "/PSNOVA/img/home/psnova-title.jpg",
    "PSO2 公式サイト": "/PSNOVA/img/home/pso2-logo.jpg",
}


class HomepageProductMediaTests(unittest.TestCase):
    def test_vita_package_is_inside_product_table_cell(self):
        html = INDEX.read_text(encoding="utf-8")
        self.assertIn('class="ta1 product-table"', html)
        cell = re.search(
            r'<td class="product-image-cell" rowspan="8">.*?</td>',
            html,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(cell)
        self.assertIn(f'src="{PACKAGE}"', cell.group(0))
        self.assertNotIn('class="product-overview"', html)
        self.assertNotIn('class="product-media"', html)

    def test_each_official_logo_is_inside_its_matching_table_row(self):
        html = INDEX.read_text(encoding="utf-8")
        self.assertIn('class="ta1 official-links-table"', html)
        self.assertNotIn('class="official-links-overview"', html)
        self.assertNotIn('class="official-link-media"', html)

        for label, source in LOGOS.items():
            with self.subTest(label=label):
                row = re.search(
                    rf'<tr>\s*<th>{re.escape(label)}</th>.*?</tr>',
                    html,
                    flags=re.DOTALL,
                )
                self.assertIsNotNone(row)
                self.assertIn('class="official-image-cell"', row.group(0))
                self.assertIn(f'src="{source}"', row.group(0))
                self.assertNotRegex(row.group(0), r'<a[^>]+>\s*<img')

    def test_sega_credit_stays_inside_official_image_cell(self):
        html = INDEX.read_text(encoding="utf-8")
        row = re.search(
            r'<tr>\s*<th>PSO2 公式サイト</th>.*?</tr>',
            html,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(row)
        self.assertIn('class="official-image-cell"', row.group(0))
        self.assertIn("©SEGA", row.group(0))

    def test_all_home_visual_assets_are_repository_local(self):
        html = INDEX.read_text(encoding="utf-8")
        for source in [PACKAGE, *LOGOS.values()]:
            self.assertIn(source, html)
            self.assertTrue((ROOT / "docs" / source.removeprefix("/PSNOVA/")).exists())

    def test_css_styles_table_cells_instead_of_external_cards(self):
        css = PAGE_STYLE.read_text(encoding="utf-8")
        self.assertIn("/* === HOMEPAGE === */", css)
        self.assertIn(".product-table .product-image-cell", css)
        self.assertIn(".official-links-table .official-image-cell", css)
        self.assertNotIn(".product-overview", css)
        self.assertNotIn(".official-links-overview", css)

    def test_homepage_label_columns_use_one_shared_blue_surface(self):
        css = PAGE_STYLE.read_text(encoding="utf-8")
        self.assertIn(".product-table th:first-child", css)
        self.assertIn(".official-links-table th:first-child", css)
        self.assertIn("background: var(--accent-soft);", css)

    def test_table_grid_is_owned_by_shared_css(self):
        page_css = PAGE_STYLE.read_text(encoding="utf-8")
        shared_css = SHARED_STYLE.read_text(encoding="utf-8")

        self.assertNotIn("border-right: 1px solid var(--border);", page_css)
        self.assertNotIn("border-bottom: 1px solid var(--border);", page_css)
        self.assertNotIn(".official-links-table tr > :last-child", page_css)
        self.assertIn("#main table th,", shared_css)
        self.assertIn("#main table td {", shared_css)
        self.assertIn("border-right: 1px solid var(--border);", shared_css)
        self.assertIn("border-bottom: 1px solid var(--border);", shared_css)
        self.assertIn("#main table tr > :last-child", shared_css)
        self.assertIn("#main table tbody > tr:last-child > td", shared_css)


if __name__ == "__main__":
    unittest.main()
