import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

SITE_ORIGIN = "https://kylekatann.github.io"
SITE_PREFIX = "/PSNOVA/"


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.anchors = set()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)

        element_id = attributes.get("id")
        if element_id:
            self.anchors.add(element_id)

        if tag == "a":
            name = attributes.get("name")
            if name:
                self.anchors.add(name)

            href = attributes.get("href")
            if href is not None:
                self.links.append(href)


def public_html_files():
    for path in DOCS.rglob("*.html"):
        if "分類中" not in path.parts:
            yield path


def parse_html(path):
    parser = LinkParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser


def published_url(path):
    relative = path.relative_to(DOCS).as_posix()
    return SITE_ORIGIN + SITE_PREFIX + relative


def local_target_from_url(url):
    parts = urlsplit(url)

    if parts.scheme not in ("", "http", "https"):
        return None

    if parts.netloc and parts.netloc != "kylekatann.github.io":
        return None

    path = unquote(parts.path)

    if not path.startswith(SITE_PREFIX):
        return None

    relative = path[len(SITE_PREFIX):]

    if not relative or relative.endswith("/"):
        relative += "index.html"

    target = (DOCS / relative).resolve()

    try:
        target.relative_to(DOCS.resolve())
    except ValueError:
        return None

    return target, unquote(parts.fragment)


class PublicInternalLinkTests(unittest.TestCase):
    def test_public_html_internal_links_resolve(self):
        missing = []
        fragment_cache = {}

        for source_path in public_html_files():
            parser = parse_html(source_path)
            base = published_url(source_path)

            for href in parser.links:
                href = href.strip()

                if not href:
                    continue

                if href.startswith(("mailto:", "tel:", "javascript:", "data:")):
                    continue

                absolute = urljoin(base, href)
                target_info = local_target_from_url(absolute)

                if target_info is None:
                    continue

                target, fragment = target_info

                if not target.is_file():
                    missing.append(
                        f"{source_path.relative_to(ROOT)} -> {href} "
                        f"(missing {target.relative_to(ROOT)})"
                    )
                    continue

                if fragment and target.suffix.lower() == ".html":
                    if target not in fragment_cache:
                        fragment_cache[target] = parse_html(target).anchors

                    if fragment not in fragment_cache[target]:
                        missing.append(
                            f"{source_path.relative_to(ROOT)} -> {href} "
                            f"(missing fragment #{fragment})"
                        )

        self.assertEqual(
            [],
            missing,
            "Broken internal links found:\n" + "\n".join(missing),
        )


if __name__ == "__main__":
    unittest.main()
