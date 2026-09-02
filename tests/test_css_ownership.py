from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "docs" / "css" / "style.css"
WEAPON = ROOT / "docs" / "css" / "weapon-tools.css"
HOME = ROOT / "docs" / "css" / "home-product.css"


def block(css, selector):
    token = selector + " {"
    assert token in css
    return css.split(token, 1)[1].split("}", 1)[0]


def test_main_paragraph_width_has_one_sitewide_owner():
    css = STYLE.read_text(encoding="utf-8")
    body = block(css, "#main p")

    assert "max-width: none;" in body
    assert "max-width: 82ch;" not in css


def test_navigation_readability_is_owned_by_sitewide_css():
    css = STYLE.read_text(encoding="utf-8")

    assert "font-size: 16px;" in block(css, "nav#menubar ul li a")
    assert "font-size: 16px;" in block(css, "#menubar-s a")
    assert "font-size: 14px;" in block(css, "#sub .submenu a")
    assert "line-height: 1.45;" in block(css, "#sub .submenu a")
    assert "font-size: 13px;" in block(css, "#sub .submenu .weapon-submenu a")
    assert "line-height: 1.4;" in block(css, "#sub .submenu .weapon-submenu a")
    assert "font-size: 12px;" in block(css, "#sub .submenu p")


def test_semantic_table_header_is_owned_by_sitewide_css():
    css = STYLE.read_text(encoding="utf-8")

    assert "#main table thead th {" not in css
    assert css.count("#main table > thead th {") == 1
    body = block(css, "#main table > thead th")

    assert "color: #1f3146;" in body
    assert "background: var(--accent-soft);" in body
    assert "font-weight: 800;" in body
    assert "text-align: center !important;" in body
    assert "white-space: nowrap;" in body


def test_page_specific_css_has_distinct_owners():
    style = STYLE.read_text(encoding="utf-8")
    weapon = WEAPON.read_text(encoding="utf-8")
    home = HOME.read_text(encoding="utf-8")

    assert ".weapon-catalog {" in weapon
    assert ".data-toolbar {" in weapon
    assert ".weapon-catalog {" not in style
    assert ".product-table .product-image-cell" in home
    assert ".product-table .product-image-cell" not in style
