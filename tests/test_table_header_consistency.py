import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
CSS = DOCS / "css" / "wiki-table.css"
MODERN = DOCS / "css" / "modern.css"
MOBILE = DOCS / "css" / "mobile-table.css"
AGENT = ROOT / "Agent.md"


def test_shared_final_header_rule_is_strong_and_uniform():
    css = CSS.read_text(encoding="utf-8")

    selector = (
        "#main table > thead th,\n"
        "#main table > thead td,\n"
        "#main table > tbody:first-of-type > tr:first-child > th,\n"
        "#main table > tbody:first-of-type > tr:first-child > td[bgcolor] {"
    )

    assert selector in css

    start = css.index(selector)
    end = css.index("}", start)
    body = css[start:end]

    assert "color: #1f3146;" in body
    assert "background: var(--accent-soft);" in body
    assert "font-weight: 800;" in body
    assert "text-align: center !important;" in body


def test_final_header_rule_wins_after_legacy_body_th_neutralization():
    css = CSS.read_text(encoding="utf-8")

    neutral = css.index(
        "#main table tbody th:not([bgcolor]) {"
    )
    final_header = css.index(
        "#main table > thead th,"
    )

    assert final_header > neutral


def test_other_shared_css_does_not_reduce_header_weight():
    modern = MODERN.read_text(encoding="utf-8")
    mobile = MOBILE.read_text(encoding="utf-8")

    # modern.css already defines table headers as strong.
    assert "table th," in modern
    assert "font-weight: 800;" in modern

    # mobile layer changes scrolling/wrapping only.
    assert "font-weight: 400" not in mobile
    assert "font-weight: normal" not in mobile


def test_all_public_table_header_shapes_are_supported_by_shared_rule():
    table_re = re.compile(
        r"<table\b[^>]*>(.*?)</table>",
        re.I | re.S,
    )
    first_row_re = re.compile(
        r"<tr\b[^>]*>(.*?)</tr>",
        re.I | re.S,
    )

    found_thead = 0
    found_first_row_th = 0
    found_legacy_bgcolor = 0

    for path in DOCS.rglob("*.html"):
        html = path.read_text(
            encoding="utf-8",
            errors="strict",
        )

        for table in table_re.finditer(html):
            table_html = table.group(1)

            if re.search(r"<thead\b", table_html, re.I):
                found_thead += 1
                continue

            first_row = first_row_re.search(table_html)
            if not first_row:
                continue

            row = first_row.group(1)

            if re.search(r"<th\b", row, re.I):
                found_first_row_th += 1

            if re.search(
                r"<(?:th|td)\b[^>]*\bbgcolor\s*=",
                row,
                re.I,
            ):
                found_legacy_bgcolor += 1

    # Repository currently contains multiple generations of table markup.
    # The shared CSS must support all of them.
    assert found_thead > 0
    assert found_first_row_th > 0
    assert found_legacy_bgcolor > 0


def test_gigantes_and_legacy_enemy_headers_use_same_shared_visual_contract():
    gigantes = (
        DOCS / "pages" / "gigantes.html"
    ).read_text(encoding="utf-8")

    enemy = (
        DOCS / "pages" / "enemy.html"
    ).read_text(encoding="utf-8")

    assert '<th scope="col">種別</th>' in gigantes
    assert '<th bgcolor="#87cefa">名前</th>' in enemy

    css = CSS.read_text(encoding="utf-8")

    # Both source forms terminate in the same 800-weight visual contract.
    assert (
        "#main table > tbody:first-of-type > "
        "tr:first-child > th,"
        in css
    )
    assert (
        "#main table tr:first-child > th[bgcolor],"
        in css
    )


def test_header_weight_rule_is_recorded_in_agent():
    agent = AGENT.read_text(encoding="utf-8")

    assert (
        "All data-table column headers use the same strong header treatment"
        in agent
    )
    assert "`font-weight: 800`" in agent
    assert "Legacy `th[bgcolor]`" in agent
    assert "semantic `<thead>`" in agent
    assert "direct first-row `<th>`" in agent
