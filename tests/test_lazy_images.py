import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
IMAGE_LAYOUT = DOCS / "js" / "menubar.js"

IMG_RE = re.compile(r'<img\b[^>]*>', re.IGNORECASE)
SRC_RE = re.compile(r'\bsrc=["\']([^"\']+)["\']', re.IGNORECASE)


def public_html_files():
    for path in DOCS.rglob("*.html"):
        if "分類中" not in path.parts:
            yield path


class LazyImageTests(unittest.TestCase):
    def test_non_logo_images_have_static_lazy_loading(self):
        violations = []

        for path in public_html_files():
            html = path.read_text(encoding="utf-8")
            for tag in IMG_RE.findall(html):
                match = SRC_RE.search(tag)
                src = match.group(1) if match else ""
                if src == "/PSNOVA/img/logo.png":
                    continue
                if 'loading="lazy"' not in tag:
                    violations.append(
                        f"{path.relative_to(ROOT)} -> {src}"
                    )

        self.assertEqual(
            [],
            violations,
            "Non-logo images must declare loading=lazy statically:\n"
            + "\n".join(violations),
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
