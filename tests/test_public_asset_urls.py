import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

REMOTE_ASSET_RE = re.compile(r"^https?://", re.IGNORECASE)
CSS_REMOTE_URL_RE = re.compile(
    r"url\(\s*[\"']?(https?://[^)\"']+)",
    re.IGNORECASE,
)
JS_REMOTE_IMAGE_RE = re.compile(
    r"<img\b[^>]*\bsrc=\\?[\"'](https?://[^\"'\\]+)",
    re.IGNORECASE,
)
ALLOWED_REMOTE_IMAGE_PREFIXES = (
    "https://hbb.afl.rakuten.co.jp/hsb/",
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


def is_approved_remote_image(url):
    return any(
        url.startswith(prefix)
        for prefix in ALLOWED_REMOTE_IMAGE_PREFIXES
    )


class PublicAssetUrlTests(unittest.TestCase):
    def test_public_html_loaded_assets_are_local(self):
        violations = []

        for path in public_html_files():
            parser = LoadedAssetParser()
            parser.feed(path.read_text(encoding="utf-8"))
            parser.close()

            for url in parser.urls:
                if REMOTE_ASSET_RE.match(url) and not is_approved_remote_image(url):
                    violations.append(
                        f"{path.relative_to(ROOT)} -> {url}"
                    )

        self.assertEqual(
            [],
            violations,
            "公開HTMLが読み込むCSS・JS・画像等のassetはローカルの "
            "/PSNOVA/... パスを使用しなければならない。og:image などの"
            "メタデータ用絶対URLはこの規則の対象外である。",
        )

    def test_public_css_does_not_hotlink_remote_assets(self):
        violations = []

        for path in (DOCS / "css").glob("*.css"):
            css = path.read_text(encoding="utf-8")
            for url in CSS_REMOTE_URL_RE.findall(css):
                violations.append(
                    f"{path.relative_to(ROOT)} -> {url}"
                )

        self.assertEqual([], violations)

    def test_dynamic_remote_images_are_limited_to_rakuten_affiliate_banners(self):
        violations = []
        approved = []

        for path in (DOCS / "js").glob("*.js"):
            js = path.read_text(encoding="utf-8")
            for url in JS_REMOTE_IMAGE_RE.findall(js):
                if is_approved_remote_image(url):
                    approved.append(url)
                else:
                    violations.append(
                        f"{path.relative_to(ROOT)} -> {url}"
                    )

        self.assertEqual([], violations)
        self.assertEqual(6, len(approved))


if __name__ == "__main__":
    unittest.main()
