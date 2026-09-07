from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS_DIR = ROOT / "docs" / "js"

EXPECTED_JS = {
    "openclose.js",
    "menubar.js",
    "sidebar.js",
}

RETIRED_JS = {
    "fixmenu_pagetop.js",
    "image-layout.js",
    "table-enhancements.js",
    "affiliate-banner.js",
    "site-search.js",
    "weapon-tools.js",
}


def test_public_javascript_is_exactly_three_files():
    actual = {path.name for path in JS_DIR.glob("*.js")}
    assert actual == EXPECTED_JS


def test_retired_javascript_files_stay_absent():
    for filename in RETIRED_JS:
        assert not (JS_DIR / filename).exists(), filename


def test_three_bundles_own_the_merged_behaviors():
    openclose = (JS_DIR / "openclose.js").read_text(encoding="utf-8")
    menubar = (JS_DIR / "menubar.js").read_text(encoding="utf-8")
    sidebar = (JS_DIR / "sidebar.js").read_text(encoding="utf-8")

    assert "function updatePageTopState()" in openclose

    assert "function applyImageHints(image)" in menubar
    assert "function decorateSemanticDataTable(table)" in menubar
    assert "function insertBanner()" in menubar

    assert "function side()" in sidebar
    assert "function initSiteSearch()" in sidebar
    assert 'var SITEMAP_URL = "/PSNOVA/sitemap.xml"' in sidebar


def test_menubar_does_not_reload_retired_scripts():
    menubar = (JS_DIR / "menubar.js").read_text(encoding="utf-8")
    for filename in RETIRED_JS:
        assert f"/PSNOVA/js/{filename}" not in menubar
