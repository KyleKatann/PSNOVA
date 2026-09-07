import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
IMAGE_LAYOUT = DOCS / "js" / "menubar.js"


class LazyImageTests(unittest.TestCase):
    def test_image_layout_does_not_enable_lazy_loading_at_runtime(self):
        js = IMAGE_LAYOUT.read_text(encoding="utf-8")

        self.assertNotRegex(
            js,
            r'setAttribute\(\s*["\']loading["\']\s*,\s*["\']lazy["\']\s*\)',
        )
        self.assertNotRegex(
            js,
            r'\.loading\s*=\s*["\']lazy["\']',
        )

    def test_image_layout_does_not_delete_legacy_jpegs_at_runtime(self):
        js = IMAGE_LAYOUT.read_text(encoding="utf-8")

        self.assertNotIn(
            "function removeInternalScreenshots()",
            js,
        )
        self.assertNotIn(
            "function isInternalScreenshot",
            js,
        )
        self.assertNotIn(
            "image.remove();",
            js,
        )


if __name__ == "__main__":
    unittest.main()
