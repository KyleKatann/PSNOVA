from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "docs" / "pages" / "technic" / "fire.html"
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
    matches = list(SOURCE_DIR.glob("テクニック_炎属性*.html"))
    assert len(matches) == 1
    return matches[0]


def test_fire_technic_page_preserves_reader_useful_source_sentinels():
    source = visible_text(source_page())
    public = visible_text(PUBLIC)

    sentinels = [
        "初期状態で習得しているテクニック",
        "照準のある位置へ向けて直線的に飛行する火の玉を打ち出す",
        "自身またはタリスのある地点を中心に螺旋状の火の玉を発生させる",
        "威力はやや低いが即座に爆発するため、移動する目標への攻撃に向く",
        "当たった敵を吹き飛ばす",
        "最終ステータス",
        "ホワイトチケット",
        "ブラックチケット",
        "マキアファクター",
    ]

    for sentinel in sentinels:
        assert sentinel in source
        assert sentinel in public


def test_fire_technic_page_keeps_level_transition_and_final_values():
    public = PUBLIC.read_text(encoding="utf-8")

    assert "<tr><td>20</td><td>486</td><td>20</td></tr>" in public
    assert "<tr><td>21</td><td>1555</td><td>20</td></tr>" in public
    assert "<tr><td>30</td><td>2673</td><td>20</td></tr>" in public
    assert "<tr><td>30</td><td>5859</td><td>22</td></tr>" in public
    assert "<tr><td>30</td><td>2173</td><td>20</td></tr>" in public
    assert "<tr><td>30</td><td>5216</td><td>22</td></tr>" in public
    assert "<tr><td>20</td><td>129</td><td>20</td></tr>" in public
    assert "<tr><td>30</td><td>139</td><td>20</td></tr>" in public
    assert "フォイエLv1のみ、メモリーフラグメント: - / グランピース(炎属性): -。" in public


def test_fire_technic_page_excludes_archive_and_wiki_editing_chrome():
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


def test_fire_technic_page_is_registered_in_public_navigation_and_sitemap():
    route = "/PSNOVA/pages/technic/fire.html"

    assert route in TECHNIC.read_text(encoding="utf-8")
    assert route in SIDEBAR.read_text(encoding="utf-8")
    assert (
        "https://kylekatann.github.io" + route
        in SITEMAP.read_text(encoding="utf-8")
    )
