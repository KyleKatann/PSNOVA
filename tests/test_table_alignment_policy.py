from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "docs" / "css" / "wiki-table.css"


def test_table_alignment_defaults_to_center_for_data_cells():
    css = CSS.read_text(encoding="utf-8")

    assert "#main table tbody td,\n#main table tbody th:not([bgcolor]) {\n    text-align: center;" in css
    assert "#main table tbody td:first-child,\n#main table tbody th:first-child:not([bgcolor])" in css
    first_cell_rule = css.split(
        "#main table tbody td:first-child,\n#main table tbody th:first-child:not([bgcolor])",
        1,
    )[1].split("}", 1)[0]
    assert "text-align: center;" in first_cell_rule
    assert "text-align: left;" not in first_cell_rule


def test_table_alignment_keeps_text_and_quest_columns_left_aligned():
    css = CSS.read_text(encoding="utf-8")

    expected_selectors = (
        "details table:has(tbody > tr > :nth-child(2):last-child)",
        "details table:has(tbody > tr > :nth-child(4):last-child)",
        "details table:has(> thead):has(tbody > tr > :nth-child(5):last-child)",
        "details table:not(:has(> thead)):has(tbody > tr > :nth-child(5):last-child)",
        "details table:has(tbody > tr > :nth-child(7):last-child)",
        "details table:has(tbody > tr > :nth-child(8):last-child)",
        "table:has(tbody > tr > :nth-child(14):last-child)",
        "table:has(tbody > tr > :nth-child(6):last-child)",
        "table:has(tbody > tr > :nth-child(5):last-child) tbody > tr > :nth-child(2)",
        "table:has(> thead):has(tbody > tr > :nth-child(4):last-child)",
        "table:not(:has(> thead)):has(tbody > tr > :nth-child(4):last-child)",
        "table:has([rowspan]):has(tbody > tr > :nth-child(7):last-child)",
        "table:not(:has([rowspan])):has(tbody > tr > :nth-child(7):last-child)",
    )

    for selector in expected_selectors:
        assert selector in css

    assert "text-align: left;" in css


def test_same_width_five_column_tables_are_disambiguated_by_source_semantics():
    css = CSS.read_text(encoding="utf-8")

    assert (
        "details table:has(> thead):has(tbody > tr > :nth-child(5):last-child) "
        "tbody > tr > :nth-child(3)"
    ) in css
    assert (
        "details table:not(:has(> thead)):has(tbody > tr > :nth-child(5):last-child) "
        "tbody > tr > :last-child"
    ) in css


def test_alignment_policy_is_css_only_not_runtime_repair():
    css = CSS.read_text(encoding="utf-8")

    assert "JavaScript must not infer" in css
    assert "table-semantics" not in css
