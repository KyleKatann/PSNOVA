import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
STYLE = ROOT / "docs" / "css" / "home-product.css"

PACKAGE = "/PSNOVA/img/home/psnova-vita-package.jpg"
LOGOS = {
    "/PSNOVA/img/home/psnova-title.jpg": (170, 96),
    "/PSNOVA/img/home/pso2-logo.jpg": (170, 96),
}


class HomepageProductMediaTests(unittest.TestCase):
    def test_product_overview_contains_only_vita_package(self):
        html = INDEX.read_text(encoding="utf-8")
        match = re.search(
            r'<div class="product-overview">.*?</div>\s*<h3>公式サイトへのリンク</h3>',
            html,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match)
        block = match.group(0)
        self.assertIn(PACKAGE, block)
        self.assertNotIn("psnova-title.jpg", block)
        self.assertNotIn("pso2-logo.jpg", block)

    def test_official_link_section_contains_nova_and_pso2_logos_on_the_right(self):
        html = INDEX.read_text(encoding="utf-8")
        match = re.search(
            r'<div class="official-links-overview">.*?</div>\s*</section>',
            html,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match)
        block = match.group(0)
        self.assertIn('class="official-link-media"', block)
        self.assertIn("PSNOVA 公式サイト", block)
        self.assertIn("PSO2 公式サイト", block)
        self.assertIn("©SEGA", block)
        self.assertNotRegex(block, r'<a[^>]+>\s*<img')

        for source, (width, height) in LOGOS.items():
            with self.subTest(source=source):
                self.assertIn(source, block)
                self.assertRegex(
                    block,
                    rf'src="{re.escape(source)}"[^>]*width="{width}" height="{height}"',
                )
                local_path = ROOT / "docs" / source.removeprefix("/PSNOVA/")
                self.assertTrue(local_path.exists())

    def test_all_home_visual_assets_are_repository_local(self):
        html = INDEX.read_text(encoding="utf-8")
        for source in [PACKAGE, *LOGOS.keys()]:
            self.assertIn(source, html)
            self.assertTrue((ROOT / "docs" / source.removeprefix("/PSNOVA/")).exists())

    def test_layout_keeps_package_and_official_logos_in_separate_right_columns(self):
        html = INDEX.read_text(encoding="utf-8")
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn('/PSNOVA/css/home-product.css', html)
        self.assertIn(".product-overview", css)
        self.assertIn("grid-template-columns: minmax(0, 1fr) 160px;", css)
        self.assertIn(".official-links-overview", css)
        self.assertIn("grid-template-columns: minmax(0, 1fr) 210px;", css)
        self.assertIn("@media screen and (max-width: 640px)", css)


if __name__ == "__main__":
    unittest.main()
