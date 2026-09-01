import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGE_LAYOUT = ROOT / "docs" / "js" / "image-layout.js"


class LazyImageTests(unittest.TestCase):
    def test_non_critical_images_are_lazy_loaded(self):
        js = IMAGE_LAYOUT.read_text(encoding="utf-8")

        self.assertIn(
            'image.setAttribute("loading", "lazy")',
            js,
        )
        self.assertIn(
            "!eagerPaths[pathname]",
            js,
        )

    def test_only_persistent_logo_is_forced_eager(self):
        js = IMAGE_LAYOUT.read_text(encoding="utf-8")

        self.assertIn(
            '"/PSNOVA/img/logo.png": true',
            js,
        )
        self.assertNotIn(
            '"/PSNOVA/img/gigantes/gigantes.jpg": true',
            js,
        )

    def test_internal_legacy_jpegs_are_removed(self):
        js = IMAGE_LAYOUT.read_text(encoding="utf-8")

        self.assertIn(
            "function removeInternalScreenshots()",
            js,
        )
        self.assertIn(
            r"/\.jpe?g$/i.test(pathname)",
            js,
        )
        self.assertIn(
            "image.remove();",
            js,
        )


if __name__ == "__main__":
    unittest.main()
