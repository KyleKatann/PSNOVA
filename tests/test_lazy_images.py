import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
IMAGE_LAYOUT = DOCS / "js" / "menubar.js"

IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
LAZY_RE = re.compile(
    r"""\bloading\s*=\s*(["'])lazy\1""",
    re.IGNORECASE,
)


def public_html_files():
    yield DOCS / "index.html"

    for path in (DOCS / "pages").rglob("*.html"):
        if "分類中" not in path.parts:
            yield path


class LazyImageTests(unittest.TestCase):
    def test_public_images_do_not_use_lazy_loading(self):
        violations = []

        for path in public_html_files():
            html = path.read_text(encoding="utf-8")

            for tag in IMG_RE.findall(html):
                if LAZY_RE.search(tag):
                    violations.append(
                        f"{path.relative_to(ROOT)} -> {tag}"
                    )

        self.assertEqual(
            [],
            violations,
            "公開画像では loading=lazy を使用してはならない:\n"
            + "\n".join(violations),
        )

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
