from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TECHNIC_DIR = ROOT / "docs" / "pages" / "technic"
LANDING = ROOT / "docs" / "pages" / "technic.html"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"
SITEMAP = ROOT / "docs" / "sitemap.xml"


ATTRIBUTES = {
    "fire": ("炎", ("フォイエ", "ギ・フォイエ", "ラ・フォイエ", "サ・フォイエ", "シフタ")),
    "ice": ("氷", ("バータ", "ギ・バータ", "ラ・バータ", "サ・バータ", "デバンド")),
    "thunder": ("雷", ("ゾンデ", "ギ・ゾンデ", "ラ・ゾンデ", "サ・ゾンデ", "ゾンディール")),
    "wind": ("風", ("ザン", "ギ・ザン", "ラ・ザン", "サ・ザン", "ナ・ザン")),
    "light": ("光", ("グランツ", "ギ・グランツ", "ラ・グランツ", "レスタ", "アンティ")),
    "dark": ("闇", ("メギド", "ギ・メギド", "ラ・メギド", "メギバース", "サ・メギド")),
}


def test_all_six_technic_attribute_pages_share_the_published_format():
    for slug, (label, names) in ATTRIBUTES.items():
        page = TECHNIC_DIR / f"{slug}.html"
        assert page.is_file()
        html = page.read_text(encoding="utf-8")

        assert f"<title>PSNOVA攻略サイト - {label}属性テクニック</title>" in html
        assert f'<main id="main" class="technic-detail-page technic-{slug}-page">' in html
        assert f"<h2>{label}属性テクニック</h2>" in html
        assert html.count('class="technic-entry"') == 5
        assert html.count('class="technic-entry-title"') == 5
        assert html.count('class="technic-note"') == 5
        assert html.count('class="technic-summary-table"') == 5
        assert html.count('class="technic-level-table"') == 10
        assert html.count('class="table-scroll technic-level-scroll"') == 10
        assert html.count('class="technic-material-note"') == 5
        assert html.count('<th scope="row">説明文</th>') == 5
        assert "<h2>強化素材について</h2>" not in html

        for name in names:
            assert f'<h2 class="technic-entry-title">{name}</h2>' in html
            assert f'aria-label="{name} Lv1〜15性能・強化素材"' in html
            assert f'aria-label="{name} Lv16〜30性能・強化素材"' in html


def test_all_six_technic_attribute_pages_are_publicly_registered():
    landing = LANDING.read_text(encoding="utf-8")
    sidebar = SIDEBAR.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")

    for slug in ATTRIBUTES:
        route = f"/PSNOVA/pages/technic/{slug}.html"
        assert route in landing
        assert route in sidebar
        assert f"https://kylekatann.github.io{route}" in sitemap
