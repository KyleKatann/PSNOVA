from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "docs" / "css" / "wiki-table.css"


def test_table_alignment_defaults_to_center_for_semantic_body_cells():
    css = CSS.read_text(encoding="utf-8")

    assert (
        "#main table tbody td,\n"
        "#main table tbody th {\n"
        "    text-align: center;"
        in css
    )

    assert (
        "#main table tbody td:first-child,\n"
        "#main table tbody th:first-child"
        in css
    )


def test_legacy_source_shape_is_not_used_as_css_semantics():
    css = CSS.read_text(encoding="utf-8")

    for forbidden in (
        "[bgcolor]",
        "tbody th:not([bgcolor])",
        "not(:has(> thead))",
        "tbody:first-of-type > tr:first-child",
    ):
        assert forbidden not in css


def test_explicit_table_semantics_preserve_special_text_alignment():
    css = CSS.read_text(encoding="utf-8")

    assert (
        "details table:not(.appearance-data-table):has(> thead)"
        in css
    )

    assert (
        ".appearance-data-table tbody > tr > :last-child"
        in css
    )

    assert (
        ".trophy-data-table tbody > tr > :nth-child(2)"
        in css
    )

    assert (
        ".trophy-data-table tbody > tr > :nth-child(3)"
        in css
    )

    assert "text-align: left;" in css


def test_alignment_is_css_presentation_not_runtime_html_repair():
    css = CSS.read_text(encoding="utf-8")

    assert "JavaScript must not infer" in css
    assert "table-semantics" not in css
