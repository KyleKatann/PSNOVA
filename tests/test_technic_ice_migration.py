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


def test_ice_technic_page_preserves_source_facts_without_copying_source_prose():
    source = visible_text(source_page())
    public = visible_text(PUBLIC)

    source_sentences = [
        "照準の位置へ向けて敵を貫通する氷柱を放つ",
        "自身またはタリスの前方に無数の氷の矢を出現させ、前方扇状の範囲内にいる対象に断続的にダメージを与える",
        "自身またはタリスを中心とした円筒状に吹雪を発生させる",
        "目標地点に対し、氷柱を落とす",
        "自身と周囲のプレイヤーキャラクターの打撃防御力・射撃防御力・法撃防御力を上昇させる",
    ]
    for sentence in source_sentences:
        assert sentence in source
        assert sentence not in public

    for fact in (
        "空中の敵には他のテクニック",
        "雑魚戦からギガンテスの部位攻撃",
        "3ヒット攻撃",
        "エアリアルアドバンス",
        "上空から氷柱を落とす",
        "Lv20では元ステータスに129%",
        "半径ステップ2回分程度",
    ):
        assert fact in public


def test_ice_technic_page_has_description_for_every_technic():
    public = PUBLIC.read_text(encoding="utf-8")

    assert public.count('class="technic-entry"') == 5
    assert public.count('class="technic-note"') == 5
    assert public.count('<th scope="row">説明文</th>') == 5
    assert '<link rel="stylesheet" href="/PSNOVA/css/page.css">' in public
    assert '<main id="main" class="technic-detail-page technic-ice-page">' in public
    assert "<p>解説</p>" not in public


def test_ice_technic_page_splits_levels_into_two_15_column_tables():
    public = PUBLIC.read_text(encoding="utf-8")

    assert public.count('class="technic-level-table"') == 10
    assert public.count('class="table-scroll technic-level-scroll"') == 10

    for level in range(1, 31):
        assert public.count(f'<th scope="col">{level}</th>') == 5

    assert public.count('<tr><th scope="row">威力</th>') == 10
    assert public.count('<tr><th scope="row">消費GP</th>') == 10
    assert public.count('<tr><th scope="row">メモリーフラグメント</th>') == 10
    assert public.count('<tr><th scope="row">グランピース(氷属性)</th>') == 10

    assert public.count('<tr><th scope="row">追加素材</th>') == 5
    assert public.count("<td>ホ※</td>") == 5
    assert public.count("<td>ブ※</td>") == 5
    assert public.count("<td>マ※</td>") == 5
    assert "※ホ" not in public
    assert "※ブ" not in public
    assert "※マ" not in public
    assert "その他必要素材" not in public

    assert "min-width: 2200px" not in public
    assert "min-width:2200px" not in public


def test_ice_technic_page_keeps_material_legends_and_final_values():
    public = PUBLIC.read_text(encoding="utf-8")
    legend = "追加素材: ホ※=ホワイトチケット×1 / ブ※=ブラックチケット×2 / マ※=マキアファクター×1"

    assert public.count(legend) == 5

    assert "<td>562</td><td>2571</td>" in public
    assert "<td>5718</td><td>6323</td>" in public
    assert "<td>4737</td><td>5223</td>" in public
    assert "<td>5286</td><td>5838</td>" in public
    assert "<td>2126</td><td>2244</td>" in public
    assert "<td>129</td><td>130</td>" in public
    assert "<td>138</td><td>139</td>" in public

    assert "J×6<br>K×10" in public
    assert "L×8<br>M×8" in public
    assert "L×6<br>M×10" in public


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
