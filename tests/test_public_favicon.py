import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ICON_PATH = DOCS / "img" / "logo.png"


def public_html_files():
    yield from DOCS.rglob("*.html")


class PublicFaviconTests(unittest.TestCase):
    def test_favicon_asset_exists(self):
        self.assertTrue(ICON_PATH.is_file())

    def test_every_public_page_declares_local_favicon(self):
        violations = []

        expected = (
            '<link rel="icon" '
            'href="/PSNOVA/img/logo.png" '
            'type="image/png">'
        )

        for path in public_html_files():
            text = path.read_text(encoding="utf-8")

            if text.count(expected) != 1:
                violations.append(
                    f"{path.relative_to(ROOT)}: "
                    f"favicon宣言は1個でなければならない"
                )

        self.assertEqual(
            [],
            violations,
            "不正なfavicon宣言:\n"
            + "\n".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
