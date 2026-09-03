import re
import unittest
from collections import deque
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SIDEBAR = DOCS / "js" / "sidebar.js"
SITE_ORIGIN = "https://kylekatann.github.io"


class AnchorParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return

        attributes = dict(attrs)
        href = (attributes.get("href") or "").strip()

        if href:
            self.hrefs.append(href)


def public_html_files():
    return sorted(
        path
        for path in DOCS.rglob("*.html")
        if "分類中" not in path.parts
    )


def route_for_file(path):
    relative = path.relative_to(DOCS).as_posix()

    if relative == "index.html":
        return "/PSNOVA/"

    return "/PSNOVA/" + relative


def normalize_internal_route(href, current_route):
    if href.startswith("#"):
        return None

    absolute = urljoin(
        SITE_ORIGIN + current_route,
        href,
    )
    parts = urlsplit(absolute)

    if parts.netloc != "kylekatann.github.io":
        return None

    path = parts.path

    if not path.startswith("/PSNOVA/"):
        return None

    if path == "/PSNOVA/index.html":
        path = "/PSNOVA/"

    return path


class PublicNavigationReachabilityTests(unittest.TestCase):
    def test_every_public_page_is_reachable_from_home(self):
        files = public_html_files()

        routes = {
            route_for_file(path): path
            for path in files
        }

        sidebar_source = SIDEBAR.read_text(encoding="utf-8")
        sidebar_hrefs = re.findall(
            r'href=["\']([^"\']+)["\']',
            sidebar_source,
        )

        graph = {}

        for route, path in routes.items():
            html = path.read_text(encoding="utf-8")

            parser = AnchorParser()
            parser.feed(html)
            parser.close()

            hrefs = list(parser.hrefs)

            if '/PSNOVA/js/sidebar.js' in html:
                hrefs.extend(sidebar_hrefs)

            targets = set()

            for href in hrefs:
                target = normalize_internal_route(
                    href,
                    route,
                )

                if target in routes:
                    targets.add(target)

            graph[route] = targets

        start = "/PSNOVA/"
        self.assertIn(start, routes)

        visited = {start}
        queue = deque([start])

        while queue:
            route = queue.popleft()

            for target in graph.get(route, set()):
                if target not in visited:
                    visited.add(target)
                    queue.append(target)

        unreachable = sorted(
            set(routes) - visited
        )

        self.assertEqual(
            [],
            unreachable,
            "Public orphan pages found:\n"
            + "\n".join(unreachable),
        )


if __name__ == "__main__":
    unittest.main()
