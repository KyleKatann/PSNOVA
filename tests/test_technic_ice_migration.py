from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "docs" / "pages" / "technic" / "ice.html"
TECHNIC = ROOT / "docs" / "pages" / "technic.html"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"
SITEMAP = ROOT / "docs" / "sitemap.xml"
SOURCE_DIR = (
    ROOT
    / "reference"
    / "psnovanet"
    / "psnova"
    / "!technic工事中excelが土方"
)


class VisibleTextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        text = data.strip()
        if text:
            self.parts.append(text)

    @property
    def text(self):
        return "".join(self.parts)


def visible_text(path):
    parser = VisibleTextParser()
    parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
    return parser.text


def source_page():
    matches = list(SOURCE_DIR.glob("テクニック_氷属性*.html"))
    assert len(matches) == 1
    return matches[0]


def test_ice_technic_page_preserves_reader_useful_source_sentinels():
    source = visible_text(source_page())
    public = visible_text(PUBLIC)

    sentinels = [
        "地面に沿って進むため、空中にいるエネミーには他のテクニックを使用したほうが良い",
        "照準の位置へ向けて敵を貫通する氷柱を放つ",
        "氷テクニックの中では非常に使いやすい",
        "3HITすべてが打ち上げ属性",
        "目標地点に対し、氷柱を落とす",
        "最終ステータス",
        "打撃防御力",
        "ホワイトチケット",
        "ブラックチケット",
        "マキアファクター",
    ]

    for sentinel in sentinels:
        assert sentinel in source
        assert sentinel in public


def test_ice_technic_page_keeps_level_transition_and_final_values():
    public = PUBLIC.read_text(encoding="utf-8")

    assert "<tr><td>20</td><td>562</td><td>20</td></tr>" in public
    assert "<tr><td>21</td><td>2571</td><td>20</td></tr>" in public
    assert "<tr><td>30</td><td>6323</td><td>20</td></tr>" in public
    assert "<tr><td>30</td><td>5223</td><td>22</td></tr>" in public
    assert "<tr><td>30</td><td>5838</td><td>22</td></tr>" in public
    assert "<tr><td>30</td><td>2244</td><td>20</td></tr>" in public
    assert "<tr><td>20</td><td>129</td><td>20</td></tr>" in public
    assert "<tr><td>30</td><td>139</td><td>20</td></tr>" in public
    assert "<tr><td>25</td><td>J×6<br>K×10</td><td>×40</td><td>ホワイトチケット×1</td></tr>" in public
    assert "<tr><td>29</td><td>L×8<br>M×8</td><td>×50</td><td>ブラックチケット×2</td></tr>" in public
    assert "<tr><td>30</td><td>L×6<br>M×10</td><td>×50</td><td>マキアファクター×1</td></tr>" in public


def test_ice_technic_page_does_not_invent_shifta_duration_for_deband():
    source = visible_text(source_page())
    public = visible_text(PUBLIC)

    assert "1分30秒" not in source
    assert "1分30秒" not in public


def test_ice_technic_page_excludes_archive_and_wiki_editing_chrome():
    public = PUBLIC.read_text(encoding="utf-8")

    for forbidden in (
        "web.archive.org",
        "table_edit2",
        "paraedit.png",
        "mini_add.png",
        "cmd=secedit",
        "comment",
    ):
        assert forbidden not in public


def test_ice_technic_page_is_registered_in_public_navigation_and_sitemap():
    route = "/PSNOVA/pages/technic/ice.html"

    assert route in TECHNIC.read_text(encoding="utf-8")
    assert route in SIDEBAR.read_text(encoding="utf-8")
    assert (
        "https://kylekatann.github.io" + route
        in SITEMAP.read_text(encoding="utf-8")
    )
