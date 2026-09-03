import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PUBLISHED_ASSET_RE = re.compile(
    r"https://kylekatann\.github\.io/PSNOVA/(?:css|js|img)/"
)


class LoadedAssetParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.urls = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attributes = dict(attrs)

        if tag in {"img", "script", "source", "video", "audio"}:
            src = (attributes.get("src") or "").strip()
            if src:
                self.urls.append(src)

        if tag == "link":
            rel = set(
                (attributes.get("rel") or "").lower().split()
            )
            if rel.intersection(
                {"stylesheet", "icon", "apple-touch-icon"}
            ):
                href = (attributes.get("href") or "").strip()
                if href:
                    self.urls.append(href)


def public_html_files():
    for path in DOCS.rglob("*.html"):
        if "分類中" not in path.parts:
            yield path


class PublicAssetUrlTests(unittest.TestCase):
    def test_public_html_does_not_self_hotlink_loaded_site_assets(self):
        violations = []

        for path in public_html_files():
            parser = LoadedAssetParser()
            parser.feed(path.read_text(encoding="utf-8"))
            parser.close()

            for url in parser.urls:
                if PUBLISHED_ASSET_RE.search(url):
                    violations.append(
                        f"{path.relative_to(ROOT)} -> {url}"
                    )

        self.assertEqual(
            [],
            violations,
            "Loaded repository-owned CSS/JS/image assets must use "
            "local /PSNOVA/... paths. Absolute metadata URLs such as "
            "og:image are intentionally outside this rule.",
        )


if __name__ == "__main__":
    unittest.main()
