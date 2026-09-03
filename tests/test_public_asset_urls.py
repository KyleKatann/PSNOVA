import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PUBLISHED_ASSET_RE = re.compile(
    r"https://kylekatann\.github\.io/PSNOVA/(?:css|js|img)/"
)


def public_html_files():
    for path in DOCS.rglob("*.html"):
        if "分類中" not in path.parts:
            yield path


class PublicAssetUrlTests(unittest.TestCase):
    def test_public_html_does_not_self_hotlink_site_assets(self):
        violations = []

        for path in public_html_files():
            text = path.read_text(encoding="utf-8")
            if PUBLISHED_ASSET_RE.search(text):
                violations.append(str(path.relative_to(ROOT)))

        self.assertEqual(
            [],
            violations,
            "Public HTML must reference repository-owned CSS/JS/image assets "
            "with local /PSNOVA/... paths, not the published GitHub Pages URL.",
        )


if __name__ == "__main__":
    unittest.main()
