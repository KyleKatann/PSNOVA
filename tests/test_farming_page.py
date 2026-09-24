from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
FARMING = DOCS / "pages" / "farming.html"
FAQ = DOCS / "pages" / "faq.html"
TRIAL = DOCS / "pages" / "trial-version.html"
TIPS = DOCS / "pages" / "tips-bugs.html"
STYLE = DOCS / "css" / "style.css"


def test_farming_page_keeps_earning_guidance_and_table():
    html = FARMING.read_text(encoding="utf-8")

    for token in (
        "<h1>稼ぎ</h1>",
        "<h2>経験値稼ぎ</h2>",
        "<h2>グランエナジー稼ぎ</h2>",
        "<h2>メモリーフラグメント稼ぎ</h2>",
        "難:グラン水源殲滅任務",
        "リーティアのお願い",
        "アルマラッピー・オナー",
        "10000G",
        "ダウジンガー",
        "メモリーフラグメント変換1～9",
        "メモリーフラグメント回収",
        "メモリーフラグメント集結",
        "探索隊",
        '<th scope="col">種類</th>',
        '<th scope="col">推奨クエスト</th>',
        '<th scope="col">プロミスオーダー</th>',
        '<th scope="col">エマージェンシーコール</th>',
        '<th scope="col">その他</th>',
    ):
        assert token in html

    for kind in "ABCDEFGHIJKLM":
        assert f"<tr><td>{kind}</td>" in html

    for internal_token in (
        "questgimmick",
        "promise_registry",
        "emergency_registry",
        "title_string_id",
        "csv総合",
        "item_4",
    ):
        assert internal_token not in html

    fragment_table = html.split('<table class="memory-fragment-table">', 1)[1].split("</table>", 1)[0]
    assert '<colgroup><col style="width:6%"><col style="width:24%"><col style="width:25%"><col style="width:23%"><col style="width:22%"></colgroup>' in fragment_table
    assert "鋼の荒野殲滅任務 N<br>メモリーフラグメント回収<br>メモリーフラグメント集結" in fragment_table
    assert "レゾルカーネベア討伐<br>マグネトアス討伐" in fragment_table
    assert "グランエナジー・ラッシュ H / VH<br>メモリーフラグメント回収" in fragment_table
    assert "メモリーフラグメント回収 VH / SH<br>メモリーフラグメント集結 SH" in fragment_table

    style = STYLE.read_text(encoding="utf-8")
    assert '#main .memory-fragment-table {' in style
    assert '#main .memory-fragment-table tbody > tr > :first-child {' in style
    assert "min-width: 0;" in style

    assert "雪辱の新兵器" not in html


def test_trial_version_owns_trial_qa_and_experience_guidance():
    trial = TRIAL.read_text(encoding="utf-8")

    for token in (
        "<h2>序盤体験版Q&amp;A</h2>",
        "序盤体験版の容量はどれくらい？",
        "序盤体験版のデータは製品版に引き継げる？",
        "体験版ではクラスレベルをいくつまで上げられる？",
        "体験版でもマルチプレイはできる？",
        "ジャストガードやステップアタックは使えないの？",
        "ジャストリバーサルは使えないの？",
        "肩越し視点（TPS）への切り替え方は？",
        "序盤体験版で経験値を稼ぐならどこがいい？",
        "雪辱の新兵器",
        "体験版ではどこまで遊べる？",
    ):
        assert token in trial


def test_trial_guidance_is_split_out_of_beginner_qa():
    faq = FAQ.read_text(encoding="utf-8")

    for token in (
        "<h2>序盤体験版について</h2>",
        "序盤体験版の容量はどれくらい？",
        "序盤体験版のデータは製品版に引き継げる？",
        "体験版ではクラスレベルをいくつまで上げられる？",
        "体験版でもマルチプレイはできる？",
        "序盤体験版で経験値を稼ぐならどこがいい？",
        "体験版ではどこまで遊べる？",
    ):
        assert token not in faq


def test_tips_page_does_not_duplicate_farming_guidance():
    tips = TIPS.read_text(encoding="utf-8")

    for token in (
        "<h3>経験値稼ぎ</h3>",
        "<h3>グランエナジー稼ぎ</h3>",
        "<h3>メモリーフラグメント稼ぎ</h3>",
        "アルマラッピー・オナー討伐プロミスオーダー",
        "ダウジンガー持ち",
        "メモリーフラグメント変換1~5",
        "雪辱の新兵器",
    ):
        assert token not in tips

    assert "小技、小ネタ、稼ぎ、状態異常" not in tips
    assert "小技や稼ぎ方、状態異常" not in tips


def test_farming_page_is_on_public_discovery_surfaces():
    page = FARMING.read_text(encoding="utf-8")
    sidebar = (DOCS / "js" / "sidebar.js").read_text(encoding="utf-8")
    sitemap = (DOCS / "sitemap.xml").read_text(encoding="utf-8")

    assert '<link rel="stylesheet" href="/PSNOVA/css/style.css">' in page
    assert '<script defer src="/PSNOVA/js/menubar.js"></script>' in page
    assert '<script defer src="/PSNOVA/js/sidebar.js"></script>' in page
    assert '<a href="/PSNOVA/pages/farming.html">稼ぎ</a>' in sidebar
    assert "https://kylekatann.github.io/PSNOVA/pages/farming.html" in sitemap
