from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEAPON_DIR = ROOT / "docs" / "pages" / "weapon"
MENUBAR = ROOT / "docs" / "js" / "menubar.js"
WEAPON_TOOLS = ROOT / "docs" / "js" / "weapon-tools.js"

WEAPON_PAGES = (
    "sword.html",
    "partizan.html",
    "doublesaber.html",
    "knuckle.html",
    "rifle.html",
    "tmachinegun.html",
    "rod.html",
    "talis.html",
    "wand.html",
    "halo.html",
    "pile.html",
)


def test_weapon_tools_script_stays_retired():
    assert not WEAPON_TOOLS.exists()
    loader = MENUBAR.read_text(encoding="utf-8")
    assert "weapon-tools.js" not in loader
    assert "data-psnova-weapon-tools" not in loader


def test_weapon_detail_pages_keep_only_catalog_navigation():
    for filename in WEAPON_PAGES:
        html = (WEAPON_DIR / filename).read_text(encoding="utf-8")
        assert (
            '<a class="weapon-page-nav-index" '
            'href="/PSNOVA/pages/weapon.html">武器一覧</a>'
        ) in html
        assert 'rel="prev"' not in html
        assert 'rel="next"' not in html


def test_weapon_detail_pages_have_no_search_filter_sort_controls():
    forbidden = (
        'id="weapon-search"',
        'id="weapon-rarity-filter"',
        'id="weapon-shop-filter"',
        'id="weapon-sort"',
        'class="data-toolbar"',
    )

    for filename in WEAPON_PAGES:
        html = (WEAPON_DIR / filename).read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in html, f"{filename} に廃止済みcontrol {token} が含まれている"
