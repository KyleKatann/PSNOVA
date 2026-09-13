from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
FARMING = DOCS / "pages" / "farming.html"
FAQ = DOCS / "pages" / "faq.html"


def test_farming_page_keeps_earning_guidance_and_table():
    html = FARMING.read_text(encoding="utf-8")

    for token in (
        "<h1>稼ぎ</h1>",
        "<h2>経験値稼ぎ</h2>",
        "<h2>グランエナジー稼ぎ</h2>",
        "<h2>メモリーフラグメント稼ぎ</h2>",
        "アルマラッピー・オナー",
        "10000G",
        "ダウジンガー",
        "メモリーフラグメント変換1～5",
        '<th scope="col">種類</th>',
        '<th scope="col">推奨クエスト</th>',
        '<th scope="col">理由・補足</th>',
    ):
        assert token in html

    for kind in "ABCDEFGHI":
        assert f"<tr><td>{kind}</td>" in html


def test_farming_guidance_is_split_out_of_beginner_qa():
    faq = FAQ.read_text(encoding="utf-8")

    assert "序盤体験版で経験値を稼ぐならどこがいい？" not in faq
    assert "グランエナジー稼ぎ" not in faq
    assert "メモリーフラグメント稼ぎ" not in faq


def test_farming_page_is_on_public_discovery_surfaces():
    page = FARMING.read_text(encoding="utf-8")
    sidebar = (DOCS / "js" / "sidebar.js").read_text(encoding="utf-8")
    sitemap = (DOCS / "sitemap.xml").read_text(encoding="utf-8")

    assert '<link rel="stylesheet" href="/PSNOVA/css/style.css">' in page
    assert '<script defer src="/PSNOVA/js/menubar.js"></script>' in page
    assert '<script defer src="/PSNOVA/js/sidebar.js"></script>' in page
    assert '<a href="/PSNOVA/pages/farming.html">稼ぎ</a>' in sidebar
    assert "https://kylekatann.github.io/PSNOVA/pages/farming.html" in sitemap
