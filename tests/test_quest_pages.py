from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEST_PAGES = {
    "steel-wilderness.html": ("鋼の荒野", "仲間の探索", "極:伏す猛銃と天舞う砲凰"),
    "gran-water-source.html": ("グラン水源", "ヨミの要求", "超:氷塊のギガティオン"),
    "flame-highlands.html": ("炎の高地", "リーティアのお願い", "極:棘と大火球の輪舞曲"),
    "ancient-city.html": ("古代都市", "静かなる都市", "極:漆黒の鉄馬と光線獣"),
    "nova-interior.html": ("ノヴァ内部", "果たすべき使命", "極:魂の解放"),
    "additional.html": ("追加クエスト", "タイムアタック・鋼の荒野", "経験値フィーバー"),
}


def page_text(filename: str) -> str:
    return (ROOT / "docs" / "pages" / "quest" / filename).read_text(encoding="utf-8")


def test_quest_pages_use_public_site_shell():
    scripts = (
        "/PSNOVA/js/openclose.js",
        "/PSNOVA/js/fixmenu_pagetop.js",
        "/PSNOVA/js/menubar.js",
        "/PSNOVA/js/sidebar.js",
    )

    for filename, (title, _, _) in QUEST_PAGES.items():
        html = page_text(filename)
        assert html.count('<main id="main">') == 1
        assert '<a class="skip-link" href="#main">本文へスキップ</a>' in html
        assert f"<title>PSNOVA攻略サイト - {title}</title>" in html
        assert f"<h2>{title}</h2>" in html
        assert '<p class="page-lead">' in html
        assert '/PSNOVA/img/logo.png' in html
        for script in scripts:
            assert f'<script defer src="{script}"></script>' in html


def test_quest_pages_strip_historical_site_chrome():
    forbidden = (
        "web.archive.org",
        "?cmd=",
        "adsbygoogle",
        "anchor_super",
        "paraedit.png",
        "mini_add.png",
        "Wayback",
    )

    for filename in QUEST_PAGES:
        html = page_text(filename)
        for token in forbidden:
            assert token not in html


def test_quest_pages_keep_quest_group_sentinels():
    for filename, (title, first_quest, last_quest) in QUEST_PAGES.items():
        html = page_text(filename)
        assert title in html
        assert first_quest in html
        assert last_quest in html
        assert "クエスト名" in html


def test_quest_pages_are_registered_in_sidebar_and_sitemap():
    sidebar = (ROOT / "docs" / "js" / "sidebar.js").read_text(encoding="utf-8")
    sitemap = (ROOT / "docs" / "sitemap.xml").read_text(encoding="utf-8")

    for filename, (title, _, _) in QUEST_PAGES.items():
        path = f"/PSNOVA/pages/quest/{filename}"
        assert f'href="{path}"' in sidebar
        assert f">{title}</a>" in sidebar
        assert f"https://kylekatann.github.io{path}" in sitemap
