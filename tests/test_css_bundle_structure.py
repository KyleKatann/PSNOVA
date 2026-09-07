from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CSS = DOCS / "css"
STYLE = CSS / "style.css"
PAGE = CSS / "page.css"
MENUBAR = DOCS / "js" / "menubar.js"
INDEX = DOCS / "index.html"
WEAPON_INDEX = DOCS / "pages" / "weapon.html"


def test_public_css_inventory_is_exactly_two_files():
    assert {path.name for path in CSS.glob("*.css")} == {
        "style.css",
        "page.css",
    }


def test_public_css_file_count_never_increases():
    assert len(list(CSS.glob("*.css"))) <= 2


def test_public_css_has_no_import_chain():
    for path in (STYLE, PAGE):
        assert "@import" not in path.read_text(encoding="utf-8")


def test_sitewide_bundle_owns_shared_components():
    css = STYLE.read_text(encoding="utf-8")

    for token in (
        ":root {",
        "#main .table-scroll {",
        "prefers-reduced-motion: reduce",
        ".affiliate-banner {",
        ".site-search {",
        ".page-lead {",
    ):
        assert token in css


def test_page_bundle_owns_home_and_weapon_specific_styles():
    css = PAGE.read_text(encoding="utf-8")

    assert "/* === HOMEPAGE === */" in css
    assert ".product-table .product-image-cell" in css
    assert "/* === WEAPON PAGES === */" in css
    assert ".weapon-catalog {" in css
    assert ".data-toolbar {" not in css
    assert ".data-filter-grid" not in css


def test_page_bundle_is_loaded_statically_for_homepage_and_weapon_routes():
    homepage = INDEX.read_text(encoding="utf-8")
    weapon = WEAPON_INDEX.read_text(encoding="utf-8")

    assert '<link rel="stylesheet" href="/PSNOVA/css/page.css">' in homepage
    assert '<link rel="stylesheet" href="/PSNOVA/css/page.css" data-psnova-page-style="true">' in weapon


def test_old_page_specific_css_names_stay_removed():
    sources = [
        INDEX.read_text(encoding="utf-8"),
        MENUBAR.read_text(encoding="utf-8"),
    ]
    for old in ("weapon-tools.css", "home-product.css"):
        assert not (CSS / old).exists()
        assert all(old not in source for source in sources)


