from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TECHNIC_DIR = ROOT / "docs" / "pages" / "technic"
TECHNIC_INDEX = ROOT / "docs" / "pages" / "technic.html"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"
SITEMAP = ROOT / "docs" / "sitemap.xml"


PAGES = {
    "thunder": "雷",
    "wind": "風",
    "light": "光",
    "dark": "闇",
}


def test_remaining_technic_pages_follow_fire_ice_structure():
    for slug, attribute in PAGES.items():
        public = (TECHNIC_DIR / f"{slug}.html").read_text(encoding="utf-8")

        assert f'<main id="main" class="technic-detail-page technic-{slug}-page">' in public
        assert public.count('class="technic-entry"') == 5
        assert public.count('class="technic-note"') == 5
        assert public.count('<th scope="row">説明文</th>') == 5
        assert public.count('class="technic-level-table"') == 10
        assert public.count('class="table-scroll technic-level-scroll"') == 10
        assert public.count(f'<tr><th scope="row">グランピース({attribute}属性)</th>') == 10
        assert public.count('<tr><th scope="row">追加素材</th>') == 5
        assert public.count('class="technic-material-note"') == 5
        assert '<h2>強化素材について</h2>' not in public

        for level in range(1, 31):
            assert public.count(f'<th scope="col">{level}</th>') == 5

        for forbidden in (
            "web.archive.org",
            "table_edit2",
            "paraedit.png",
            "mini_add.png",
            "cmd=secedit",
        ):
            assert forbidden not in public


def test_remaining_technic_pages_keep_key_source_facts_and_unknowns():
    thunder = (TECHNIC_DIR / "thunder.html").read_text(encoding="utf-8")
    wind = (TECHNIC_DIR / "wind.html").read_text(encoding="utf-8")
    light = (TECHNIC_DIR / "light.html").read_text(encoding="utf-8")
    dark = (TECHNIC_DIR / "dark.html").read_text(encoding="utf-8")

    assert "表示威力は総ダメージの4分の1" in thunder
    assert "雷属性攻撃を当てても放電せず" in thunder
    assert thunder.count("<td>不明</td>") == 6
    assert "<td>6984</td><td>7721</td>" in thunder
    assert '<th scope="row">メモリーフラグメント</th><td>-</td><td>A×2</td>' in thunder

    assert "ジャンプでかわして残存時間を延ばせる" in wind
    assert "<td>4743</td><td>5233</td>" in wind
    assert "<td>不明</td>" not in wind

    assert "初期状態から習得している回復テクニック" in light
    assert "<td>832</td><td>856</td>" in light
    assert '<th scope="row">メモリーフラグメント</th><td>-</td><td>A×2</td>' in light
    assert "<td>不明</td>" not in light

    assert "ダウン効果" in dark
    assert "<td>9494</td><td>10485</td>" in dark
    assert dark.count("<td>不明</td>") == 4

    assert thunder.count("ブ※=ブラックチケット×1") == 1
    assert light.count("ブ※=ブラックチケット×1") == 1
    assert dark.count("ブ※=ブラックチケット×1") == 1


def test_remaining_technic_pages_are_registered_in_navigation_and_sitemap():
    technic_index = TECHNIC_INDEX.read_text(encoding="utf-8")
    sidebar = SIDEBAR.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")

    for slug in PAGES:
        route = f"/PSNOVA/pages/technic/{slug}.html"
        assert route in technic_index
        assert route in sidebar
        assert "https://kylekatann.github.io" + route in sitemap
