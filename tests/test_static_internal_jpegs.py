from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITEMAP = DOCS / "sitemap.xml"


class MainJpegScanner(HTMLParser):
    def __init__(self):
        super().__init__()
        self.main_depth = 0
        self.jpeg_sources = []

    def process_start(self, tag, attrs):
        tag = tag.lower()
        attrs = dict(attrs)

        if tag == "div":
            if self.main_depth:
                self.main_depth += 1
            elif attrs.get("id") == "main":
                self.main_depth = 1

        if tag == "img" and self.main_depth:
            src = attrs.get("src") or ""
            path = urlparse(src).path.lower()

            if path.endswith((".jpg", ".jpeg")):
                self.jpeg_sources.append(src)

    def handle_starttag(self, tag, attrs):
        self.process_start(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        self.process_start(tag, attrs)

        if tag.lower() == "div" and self.main_depth:
            self.main_depth -= 1

    def handle_endtag(self, tag):
        if tag.lower() == "div" and self.main_depth:
            self.main_depth -= 1


def public_internal_pages():
    root = ElementTree.parse(SITEMAP).getroot()

    ns = {
        "sm": "http://www.sitemaps.org/schemas/sitemap/0.9"
    }

    result = set()

    for loc in root.findall("sm:url/sm:loc", ns):
        route = unquote(
            urlparse(
                (loc.text or "").strip()
            ).path
        )

        if not route.startswith("/PSNOVA/"):
            continue

        relative = (
            route[len("/PSNOVA/"):]
            or "index.html"
        )

        if (
            relative.endswith(".html")
            and relative != "index.html"
        ):
            result.add(DOCS / relative)

    return sorted(result)


def test_public_internal_main_has_no_legacy_jpeg_images():
    failures = []

    pages = public_internal_pages()

    assert len(pages) >= 20

    for path in pages:
        parser = MainJpegScanner()
        parser.feed(
            path.read_text(encoding="utf-8")
        )

        for src in parser.jpeg_sources:
            failures.append(
                f"{path.relative_to(ROOT)}: {src}"
            )

    assert not failures, "\n".join(failures)
