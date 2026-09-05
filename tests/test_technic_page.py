from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PAGE = DOCS / "pages" / "technic.html"
SIDEBAR = DOCS / "js" / "sidebar.js"
SITEMAP = DOCS / "sitemap.xml"


class TechniqueTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.current_row = None
        self.current_cell = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.current_row = []
        elif tag in {"th", "td"} and self.current_row is not None:
            self.current_cell = []

    def handle_data(self, data):
        if self.current_cell is not None:
            self.current_cell.append(data)

    def handle_endtag(self, tag):
        if tag in {"th", "td"} and self.current_cell is not None:
            self.current_row.append(
                "".join(self.current_cell).strip()
            )
            self.current_cell = None
        elif tag == "tr" and self.current_row is not None:
            self.rows.append(self.current_row)
            self.current_row = None


def test_technic_overview_preserves_staged_usage_contract():
    html = PAGE.read_text(encoding="utf-8")

    for text in (
        "フォース",
        "バスター",
        "テクニック使用可",
        "サブパレット",
        "チャージが必須",
    ):
        assert text in html


def test_technic_overview_lists_all_six_attributes():
    parser = TechniqueTableParser()
    parser.feed(PAGE.read_text(encoding="utf-8"))

    assert parser.rows == [
        ["属性", "系統", "特徴"],
        ["炎属性", "フォイエ系", "発火現象を起こす。"],
        ["氷属性", "バータ系", "吹雪などを発生させる。"],
        ["雷属性", "ゾンデ系", "落雷などを起こす。"],
        ["風属性", "ザン系", "かまいたちや気圧変化を発生させる。"],
        ["光属性", "グランツ系", "浄化の光による攻撃や体力回復などを行う。"],
        ["闇属性", "メギド系", "凝縮したグランを操る。"],
    ]


def test_technic_overview_is_registered_in_navigation_and_sitemap():
    sidebar = SIDEBAR.read_text(encoding="utf-8")
    assert (
        '<a href="/PSNOVA/pages/technic.html">テクニック</a>'
        in sidebar
    )

    sitemap = ElementTree.parse(SITEMAP).getroot()
    ns = {
        "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
    }
    urls = {
        (loc.text or "").strip()
        for loc in sitemap.findall("sm:url/sm:loc", ns)
    }

    assert (
        "https://kylekatann.github.io/PSNOVA/pages/technic.html"
        in urls
    )
