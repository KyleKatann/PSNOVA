from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PAGE = DOCS / "pages" / "novafactor.html"
SIDEBAR = DOCS / "js" / "sidebar.js"
SITEMAP = DOCS / "sitemap.xml"


def assert_in_order(text, values):
    cursor = -1
    for value in values:
        cursor = text.index(value, cursor + 1)


def test_nova_factor_guide_is_linked_below_faq():
    sidebar = SIDEBAR.read_text(encoding="utf-8")
    faq = '<a href="/PSNOVA/pages/faq.html">初心者Q&amp;A</a>'
    guide = '<a href="/PSNOVA/pages/novafactor.html">ノヴァファクター集め</a>'

    assert faq in sidebar
    assert guide in sidebar
    assert sidebar.index(faq) < sidebar.index(guide)
    assert "https://kylekatann.github.io/PSNOVA/pages/novafactor.html" in SITEMAP.read_text(encoding="utf-8")


def test_nova_factor_guide_keeps_reader_facing_copy():
    html = PAGE.read_text(encoding="utf-8")

    assert "ノヴァファクターはLv201以上の大型エネミーからドロップする。" in html
    assert "必要装備" in html
    assert "おすすめクエスト" in html
    assert "対象属性" not in html
    assert "弱点属性" not in html
    assert "5ch" not in html
    assert "内部テーブル" not in html
    assert "なぜ" not in html
    assert "→" not in html
    assert "周回先の選び方" not in html
    assert "難：ギュゲンテ撃破任務 XH" not in html


def test_death_date_spawn_order_matches_last_date_pattern():
    html = PAGE.read_text(encoding="utf-8")

    death_date = html.split("<h4>1. 超：デス・デート XH</h4>", 1)[1].split(
        "<h4>2. 超：城壁のヴィヴリュード XH</h4>", 1
    )[0]
    assert_in_order(
        death_date,
        [
            "デェフキュオネ",
            "グラヴディオン",
            "ノイヴァトアス",
            "ヴァリゴルドス",
            "ヴィヴリュード",
            "アルテイオス",
        ],
    )

    last_date = html.split("<h4>3. 難：★ラスト・デート XH</h4>", 1)[1].split(
        "<h4>4. 難：リベルゲンテ決戦 XH</h4>", 1
    )[0]
    assert_in_order(
        last_date,
        [
            "デェフキュオネ",
            "グラヴディオン",
            "マグネトアス",
            "ディゴルドス",
            "ヴィヴリュード",
            "アルテイオス",
        ],
    )
