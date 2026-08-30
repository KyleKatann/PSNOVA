import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
STYLE = ROOT / "docs" / "css" / "home-product.css"

ASSETS = {
    "/PSNOVA/img/home/psnova-vita-package.jpg": (145, 184),
    "/PSNOVA/img/home/psnova-title.jpg": (170, 96),
    "/PSNOVA/img/home/pso2-logo.jpg": (170, 96),
}


class HomepageProductMediaTests(unittest.TestCase):
    def test_product_media_uses_only_repository_local_images(self):
        html = INDEX.read_text(encoding="utf-8")
        match = re.search(
            r'<aside class="product-media".*?</aside>',
            html,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match)
        block = match.group(0)

        sources = re.findall(r'<img[^>]+src="([^"]+)"', block)
        self.assertEqual(set(sources), set(ASSETS))
        self.assertNotRegex(block, r'<a\b')
        self.assertNotRegex(block, r'src="https?://')

        for source in sources:
            with self.subTest(source=source):
                local_path = ROOT / "docs" / source.removeprefix("/PSNOVA/")
                self.assertTrue(local_path.exists())

    def test_product_media_keeps_static_dimensions_and_sega_credit(self):
        html = INDEX.read_text(encoding="utf-8")
        self.assertIn("©SEGA", html)
        for source, (width, height) in ASSETS.items():
            with self.subTest(source=source):
                pattern = (
                    rf'src="{re.escape(source)}"'
                    rf'[^>]*width="{width}" height="{height}"'
                )
                self.assertRegex(html, pattern)

    def test_product_layout_is_right_column_on_desktop_and_stacks_on_small_screens(self):
        html = INDEX.read_text(encoding="utf-8")
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn('/PSNOVA/css/home-product.css', html)
        self.assertIn(".product-overview", css)
        self.assertIn("grid-template-columns: minmax(0, 1fr) 300px;", css)
        self.assertIn("@media screen and (max-width: 900px)", css)
        self.assertIn("grid-template-columns: 1fr;", css)


if __name__ == "__main__":
    unittest.main()
