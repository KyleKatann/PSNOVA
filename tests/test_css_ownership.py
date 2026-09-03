from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "docs" / "css" / "style.css"
PAGE = ROOT / "docs" / "css" / "page.css"


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


def test_page_specific_css_has_one_owner_file():
    style = STYLE.read_text(encoding="utf-8")
    page = PAGE.read_text(encoding="utf-8")

    assert ".weapon-catalog {" in page
    assert ".data-toolbar {" in page
    assert ".product-table .product-image-cell" in page
    assert ".weapon-catalog {" not in style
    assert ".product-table .product-image-cell" not in style


def test_weapon_filter_grid_does_not_duplicate_single_type_selectors():
    page = PAGE.read_text(encoding="utf-8")

    assert ".data-filter-grid.is-single-type" not in page
    assert page.count(".data-filter-grid { grid-template-columns: 1fr; }") == 1


def test_shop_numeric_format_has_one_shared_owner():
    style = STYLE.read_text(encoding="utf-8")
    page = PAGE.read_text(encoding="utf-8")

    shared_shop = block(style, "#main table .shop-level-cell")
    page_shop = block(page, ".shop-level-cell")

    assert "font-variant-numeric: tabular-nums;" in shared_shop
    assert "font-variant-numeric" not in page_shop
    assert "white-space: nowrap;" in page_shop


def test_home_cells_inherit_shared_table_presentation():
    style = STYLE.read_text(encoding="utf-8")
    page = PAGE.read_text(encoding="utf-8")

    shared_cells = block(style, "#main table th,\n#main table td")

    assert "background: var(--surface-subtle);" in shared_cells
    assert "vertical-align: middle;" in shared_cells
    assert "background: var(--surface-subtle);" not in page
    assert "vertical-align: middle;" not in page
