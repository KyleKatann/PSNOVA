import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITE_ROOT = "/PSNOVA/"
SIDEBAR = DOCS / "js" / "sidebar.js"


class _LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self.hrefs.append(href)


def _html_hrefs(text):
    parser = _LinkParser()
    parser.feed(text)
    return parser.hrefs


def _route_for(path):
    relative = path.relative_to(DOCS).as_posix()
    if relative == "index.html":
        return SITE_ROOT
    return f"{SITE_ROOT}{relative}"


def _internal_target(base_route, href):
    split = urlsplit(href)
    if split.scheme or split.netloc:
        return None

    target = urljoin(base_route, split.path or base_route)
    if target == f"{SITE_ROOT}index.html":
        target = SITE_ROOT
    if not target.startswith(SITE_ROOT):
        return None
    return target


class PublicNavigationCoverageTests(unittest.TestCase):
    def test_every_public_html_page_is_reachable_from_site_root(self):
        pages = {
            _route_for(path): path
            for path in sorted(DOCS.rglob("*.html"))
        }
        self.assertIn(SITE_ROOT, pages)

        sidebar = SIDEBAR.read_text(encoding="utf-8")
        shared_hrefs = re.findall(r'href=["\']([^"\']+)["\']', sidebar)

        links = {}
        for route, path in pages.items():
            html = path.read_text(encoding="utf-8")
            targets = set()
            for href in (*_html_hrefs(html), *shared_hrefs):
                target = _internal_target(route, href)
                if target in pages:
                    targets.add(target)
            links[route] = targets

        reachable = {SITE_ROOT}
        pending = [SITE_ROOT]
        while pending:
            route = pending.pop()
            for target in links[route] - reachable:
                reachable.add(target)
                pending.append(target)

        unreachable = sorted(set(pages) - reachable)
        self.assertEqual(
            [],
            unreachable,
            "トップページから到達できない公開HTMLがある",
        )


if __name__ == "__main__":
    unittest.main()
