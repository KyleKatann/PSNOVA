from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

MODERN = ROOT / "docs" / "css" / "modern.css"
STYLE = ROOT / "docs" / "css" / "style.css"
WIKI = ROOT / "docs" / "css" / "wiki-table.css"


def block(css, selector):
    token = selector + " {"

    assert css.count(token) == 1

    return css.split(token, 1)[1].split("}", 1)[0]


def test_main_paragraph_width_has_one_owner():
    modern = MODERN.read_text(encoding="utf-8")
    style = STYLE.read_text(encoding="utf-8")

    body = block(modern, "#main p")

    assert "max-width: none;" in body
    assert "max-width: 82ch;" not in modern
    assert "#main p {" not in style


def test_navigation_readability_is_owned_by_modern_css():
    modern = MODERN.read_text(encoding="utf-8")
    style = STYLE.read_text(encoding="utf-8")

    assert "font-size: 16px;" in block(
        modern,
        "nav#menubar ul li a",
    )

    assert "font-size: 16px;" in block(
        modern,
        "#menubar-s a",
    )

    assert "font-size: 14px;" in block(
        modern,
        "#sub .submenu a",
    )

    assert "line-height: 1.45;" in block(
        modern,
        "#sub .submenu a",
    )

    assert "font-size: 13px;" in block(
        modern,
        "#sub .submenu .weapon-submenu a",
    )

    assert "line-height: 1.4;" in block(
        modern,
        "#sub .submenu .weapon-submenu a",
    )

    assert "font-size: 12px;" in block(
        modern,
        "#sub .submenu p",
    )

    assert (
        "User-corrected navigation readability baseline"
        not in style
    )


def test_semantic_table_header_has_one_owner():
    css = WIKI.read_text(encoding="utf-8")

    assert "#main table thead th {" not in css

    body = block(
        css,
        "#main table > thead th",
    )

    assert "color: #1f3146;" in body
    assert "background: var(--accent-soft);" in body
    assert "font-weight: 800;" in body
    assert "text-align: center !important;" in body
    assert "white-space: nowrap;" in body
