from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OVERVIEW = DOCS / "pages" / "granarts.html"
DETAIL_DIR = DOCS / "pages" / "granarts"
SIDEBAR = DOCS / "js" / "sidebar.js"
SITEMAP = DOCS / "sitemap.xml"
STAGED = DOCS / "pages" / "分類中" / "!granarts工事中excelが土方"

EXPECTED = {
    "sword": ("ソード", ("ライジングエッジ", "ツイスターフォール", "ノヴァストライク", "オーバーエンド", "ソニックアロウ", "ファングラッシュ", "トルネードメテオ")),
    "partizan": ("パルチザン", ("スライドシェイカー", "スピードレイン", "ピークアップスロー", "トリックレイヴ", "スライドエンド", "バンタースナッチ", "オーバースライサー")),
    "doublesaber": ("ダブルセイバー", ("シザーエッジ", "ランブリングムーン", "イリュージョンレイヴ", "サプライズダンク", "デッドリーアーチャー", "アクロエフェクト", "ムーンサルトラッシュ")),
    "knuckle": ("ナックル", ("ダッキングブロウ", "フリッカージャブ", "ペンデュラムロール", "ストレイトチャージ", "クエイクハウリング", "スライドアッパー", "ヘルクラッシュ")),
    "rifle": ("アサルトライフル", ("ピアッシングシェル", "グレネードシェル", "ワンポイント", "インパクトスライダー", "スニークシューター", "グローリーレイン", "リフレクトイージス")),
    "tmachinegun": ("ツインマシンガン", ("エリアルシューティング", "バレットスコール", "インフィニティファイア", "サテライトエイム", "エルダーリベリオン", "リバースタップ", "ダンシングスイープ")),
    "halo": ("ヘイロウ", ("リングフィールド", "プロテクションウォール", "アグレッシブケイジ", "スネアゲート", "アッパービート", "サテライトビット", "レゾナンスキャノン")),
    "pile": ("パイル", ("パイルシューター", "パイルラッシュ", "パイルストーム", "ブーストダンク", "ブーストブリッツ", "ライジングインパクト", "バーンスマッシュ")),
}


class RowParser(HTMLParser):
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
            self.current_row.append("".join(self.current_cell).strip())
            self.current_cell = None
        elif tag == "tr" and self.current_row is not None:
            self.rows.append(self.current_row)
            self.current_row = None


def test_granarts_overview_matches_weapon_style_and_links_all_categories():
    html = OVERVIEW.read_text(encoding="utf-8")
    assert 'class="weapon-catalog"' in html
    assert html.count('class="weapon-card"') == len(EXPECTED)
    for slug, (name, _) in EXPECTED.items():
        assert f'href="/PSNOVA/pages/granarts/{slug}.html"' in html
        assert f"<span>{name}</span>" in html


def test_each_granarts_page_contains_seven_static_rows():
    for slug, (name, expected_names) in EXPECTED.items():
        html = (DETAIL_DIR / f"{slug}.html").read_text(encoding="utf-8")
        assert "分類中" not in html
        assert f"{name} グランアーツ" in html
        assert 'class="table-scroll"' in html
        assert 'class="weapon-data-table"' in html
        assert 'data-granarts-static="true"' in html
        assert "<thead>" in html
        assert 'scope="col"' in html
        assert "Lv30威力" in html
        assert "Lv30消費GP" in html
        parser = RowParser()
        parser.feed(html)
        assert parser.rows[0] == ["名前", "技量補正", "説明", "Lv30威力", "Lv30消費GP"]
        assert [row[0] for row in parser.rows[1:]] == list(expected_names)
        assert len(parser.rows) == 8
        for forbidden in ("web.archive.org", "adsbygoogle", "table_edit2", "paraedit.png"):
            assert forbidden not in html


def test_granarts_sentinels_preserve_staged_final_values():
    sentinels = {
        "sword": ("オーバーエンド", "17776", "25"),
        "rifle": ("リフレクトイージス", "2500", "100"),
        "halo": ("レゾナンスキャノン", "9148", "17"),
        "pile": ("パイルストーム", "16254", "15"),
    }
    for slug, expected in sentinels.items():
        parser = RowParser()
        parser.feed((DETAIL_DIR / f"{slug}.html").read_text(encoding="utf-8"))
        matching = [row for row in parser.rows if row and row[0] == expected[0]]
        assert len(matching) == 1
        assert matching[0][-2:] == list(expected[1:])


def test_granarts_navigation_and_sitemap_register_all_public_pages():
    sidebar = SIDEBAR.read_text(encoding="utf-8")
    assert '<a class="weapon-data-link" href="/PSNOVA/pages/granarts.html">グランアーツ</a>' in sidebar
    expected_routes = {"/PSNOVA/pages/granarts.html"}
    for slug, (name, _) in EXPECTED.items():
        route = f"/PSNOVA/pages/granarts/{slug}.html"
        expected_routes.add(route)
        assert f'href="{route}">{name}</a>' in sidebar
    sitemap = ElementTree.parse(SITEMAP).getroot()
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    routes = {(loc.text or "").strip().removeprefix("https://kylekatann.github.io") for loc in sitemap.findall("sm:url/sm:loc", ns)}
    assert expected_routes <= routes


def test_granarts_staging_source_remains_nonpublic_reference():
    assert STAGED.is_dir()
