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

    assert "ノヴァファクターはLv201～260の大型エネミーから狙える希少素材。" in html
    assert "必要装備" in html
    assert "おすすめクエスト" in html
    assert "約154か所" in html
    assert "約155か所" in html
    assert "約105～130か所" in html
    assert "ノヴァファクター狙いでは、テンプテーション付き武器へ持ち替える必要はありません" in html
    assert "テンプテーションが上げるのは通常アイテム側のドロップ率" in html
    assert "レア枠の当選率は上がらない" in html
    assert "レア枠から始まるドロップ抽選を1回追加" in html
    assert 'href="/PSNOVA/pages/rare-drop.html">レアドロップの仕組み</a>' in html
    assert "テンプテーションを付けられるなら付けておく" not in html

    for internal_term in (
        "DropID",
        "CharacterID",
        "PartsParam",
        "Repop",
        "runtime",
        "selector",
        "enemy_group_id",
        "incident",
        "内部テーブル",
    ):
        assert internal_term not in html


def test_recommended_quest_order_and_spawn_order():
    html = PAGE.read_text(encoding="utf-8")

    comparison = html.split("<h2>おすすめクエスト</h2>", 1)[1].split(
        "<h3>1. 難：★ラスト・デート XH</h3>", 1
    )[0]
    assert_in_order(
        comparison,
        [
            "難：★ラスト・デート XH",
            "超：デス・デート XH",
            "極：ヘル・デート XH",
            "極：棘と大火球の輪舞曲 XH",
            "超：尖塔に潜む光線獣 XH",
        ],
    )

    last_date = html.split("<h3>1. 難：★ラスト・デート XH</h3>", 1)[1].split(
        "<h3>2. 超：デス・デート XH</h3>", 1
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

    death_date = html.split("<h3>2. 超：デス・デート XH</h3>", 1)[1].split(
        "<h3>3. 極：ヘル・デート XH</h3>", 1
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
