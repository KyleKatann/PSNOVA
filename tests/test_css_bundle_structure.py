from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "docs" / "css"
STYLE = CSS / "style.css"
WEAPON = CSS / "weapon-tools.css"
HOME = CSS / "home-product.css"
MENUBAR = ROOT / "docs" / "js" / "menubar.js"


def test_public_css_inventory_is_exactly_three_files():
    assert {path.name for path in CSS.glob("*.css")} == {
        "style.css",
        "weapon-tools.css",
        "home-product.css",
    }


def test_public_css_has_no_import_chain():
    for path in (STYLE, WEAPON, HOME):
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


def test_weapon_bundle_is_loaded_only_for_weapon_routes():
    css = WEAPON.read_text(encoding="utf-8")
    js = MENUBAR.read_text(encoding="utf-8")

    assert ".weapon-catalog {" in css
    assert ".data-toolbar {" in css
    assert "/PSNOVA/css/weapon-tools.css" in js
    assert "data-psnova-weapon-tools-style" in js
    assert r"weapon(?:\.html|\/[^/]+\.html)$" in js


def test_home_bundle_remains_homepage_specific():
    css = HOME.read_text(encoding="utf-8")
    html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert ".product-table .product-image-cell" in css
    assert "/PSNOVA/css/home-product.css" in html
