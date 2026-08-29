import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGE_LAYOUT = ROOT / "docs" / "js" / "image-layout.js"


class LazyImageTests(unittest.TestCase):
    def test_non_critical_images_are_lazy_loaded(self):
        js = IMAGE_LAYOUT.read_text(encoding="utf-8")
        self.assertIn('image.setAttribute("loading", "lazy")', js)
        self.assertIn("!eagerPaths[pathname]", js)

    def test_logo_and_shared_hero_remain_eager(self):
        js = IMAGE_LAYOUT.read_text(encoding="utf-8")
        self.assertIn('"/PSNOVA/img/logo.png": true', js)
        self.assertIn('"/PSNOVA/img/gigantes/gigantes.jpg": true', js)


if __name__ == "__main__":
    unittest.main()
