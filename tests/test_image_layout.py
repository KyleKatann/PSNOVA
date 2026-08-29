import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENUBAR = ROOT / "docs" / "js" / "menubar.js"
IMAGE_LAYOUT = ROOT / "docs" / "js" / "image-layout.js"


class ImageLayoutTests(unittest.TestCase):
    def test_image_layout_script_is_loaded_globally(self):
        js = MENUBAR.read_text(encoding="utf-8")
        self.assertIn("/PSNOVA/js/image-layout.js", js)
        self.assertIn("data-psnova-image-layout", js)

    def test_known_large_images_have_explicit_dimensions(self):
        js = IMAGE_LAYOUT.read_text(encoding="utf-8")
        self.assertIn('"/PSNOVA/img/logo.png": { width: 660, height: 121 }', js)
        self.assertIn('"/PSNOVA/img/gigantes/gigantes.jpg": { width: 1000, height: 540 }', js)
        self.assertIn('image.setAttribute("width", String(dimensions.width))', js)
        self.assertIn('image.setAttribute("height", String(dimensions.height))', js)

    def test_unknown_images_are_not_guessed(self):
        js = IMAGE_LAYOUT.read_text(encoding="utf-8")
        self.assertIn("if (!pathname)", js)


if __name__ == "__main__":
    unittest.main()
