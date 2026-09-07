from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MENUBAR = DOCS / "js" / "menubar.js"
PAGE_META = DOCS / "js" / "page-meta.js"
SITEMAP = DOCS / "sitemap.xml"
SITE_ORIGIN = "https://kylekatann.github.io"
SITE_ROOT = "/PSNOVA/"


class HeadMetadataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title_parts = []
        self.named_meta = {}
        self.property_meta = {}
        self.canonicals = []

    @property
    def title(self):
        return "".join(self.title_parts).strip()

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attrs = dict(attrs)

        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            name = attrs.get("name")
            prop = attrs.get("property")
            if name:
                self.named_meta.setdefault(name, []).append(attrs.get("content", ""))
            if prop:
                self.property_meta.setdefault(prop, []).append(attrs.get("content", ""))
        elif tag == "link" and attrs.get("rel") == "canonical":
            self.canonicals.append(attrs.get("href", ""))

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)


def sitemap_routes():
    root = ElementTree.parse(SITEMAP).getroot()
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    routes = set()

    for loc in root.findall("sm:url/sm:loc", ns):
        value = (loc.text or "").strip()
        route = unquote(urlparse(value).path)
        routes.add(route)

    return routes


def public_html_routes():
    routes = {SITE_ROOT}

    for path in DOCS.rglob("*.html"):
        if path == DOCS / "index.html":
            continue
        if "分類中" in path.parts:
            continue

        relative = path.relative_to(DOCS).as_posix()
        routes.add(SITE_ROOT + relative)

    return routes


def route_to_file(route):
    if route in {SITE_ROOT, "/PSNOVA/index.html"}:
        return DOCS / "index.html"

    assert route.startswith(SITE_ROOT)
    return DOCS / route.removeprefix(SITE_ROOT)


def parse(route):
    parser = HeadMetadataParser()
    parser.feed(route_to_file(route).read_text(encoding="utf-8"))
    return parser


def test_sitemap_and_public_html_cover_same_routes():
    assert sitemap_routes() == public_html_routes()


def test_public_metadata_is_static_and_self_consistent():
    for route in sorted(public_html_routes()):
        parser = parse(route)
        canonical_url = SITE_ORIGIN + route
        page_type = "website" if route == SITE_ROOT else "article"

        if route == SITE_ROOT:
            assert parser.title == "PSNOVA攻略サイト"
        else:
            assert parser.title.startswith("PSNOVA攻略サイト - "), route
            assert parser.title.removeprefix("PSNOVA攻略サイト - ").strip(), route

        descriptions = parser.named_meta.get("description")
        assert descriptions is not None and len(descriptions) == 1, route
        description = descriptions[0].strip()
        assert description, route

        assert "keywords" not in parser.named_meta, route
        assert parser.canonicals == [canonical_url], route
        assert parser.property_meta.get("og:title") == [parser.title], route
        assert parser.property_meta.get("og:description") == [description], route
        assert parser.property_meta.get("og:type") == [page_type], route
        assert parser.property_meta.get("og:url") == [canonical_url], route
        assert parser.property_meta.get("og:site_name") == ["PSNOVA攻略サイト"], route


def test_runtime_metadata_repair_is_removed():
    assert not PAGE_META.exists()

    menubar = MENUBAR.read_text(encoding="utf-8")
    assert "page-meta.js" not in menubar
    assert "data-psnova-page-meta" not in menubar


