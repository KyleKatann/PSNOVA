from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT = ROOT / "Agent.md"
STYLE_CSS = ROOT / "docs" / "css" / "style.css"
PAGE_CSS = ROOT / "docs" / "css" / "page.css"


def test_agent_records_technic_presentation_contract():
    guide = AGENT.read_text(encoding="utf-8")

    for rule in (
        "All public data tables use the same square-corner treatment",
        "Do not add rounded corners or card-like shadows to a table, its caption, or its table-scroll wrapper",
        "Every technic entry must include a reader-facing description in static HTML",
        "use the PSO2 Wiki only as a secondary source",
        "Never copy source wording verbatim",
        "Existing technic descriptions imported from the archived Wiki must also be rewritten",
        "Technic Lv tables use the same column geometry across every technique and every attribute",
        "Technic descriptive/behavior notes use one consistent gray highlight treatment",
        "reserve it for material legends such as `ホ※` / `ブ※` / `マ※`",
    ):
        assert rule in guide

    assert "Technic supplementary notes and material legends use one consistent yellow highlight treatment" not in guide


def test_shared_data_tables_are_shadowless():
    css = STYLE_CSS.read_text(encoding="utf-8")
    table_rule = css.split("#main table {", 1)[1].split("}", 1)[0]

    assert "box-shadow: none;" in table_rule
    assert "var(--shadow-sm)" not in table_rule
    assert "var(--shadow-md)" not in table_rule


def test_technic_tables_use_square_fixed_shared_column_geometry():
    css = PAGE_CSS.read_text(encoding="utf-8")

    assert "#main.technic-detail-page .technic-level-table {" in css
    assert "table-layout: fixed;" in css
    assert "width: 184px;" in css
    assert "min-width: 184px;" in css
    assert "#main.technic-detail-page .technic-summary-table" in css
    assert "#main.technic-detail-page .technic-level-scroll" in css
    assert "border-radius: 0;" in css
    assert "box-shadow: none;" in css


def test_technic_descriptions_are_gray_and_material_legends_are_yellow():
    css = PAGE_CSS.read_text(encoding="utf-8")

    note_rule = css.split("#main.technic-detail-page .technic-note {", 1)[1].split("}", 1)[0]
    material_rule = css.split("#main.technic-detail-page .technic-material-note {", 1)[1].split("}", 1)[0]

    assert "background: var(--surface-subtle);" in note_rule
    assert "border: 1px solid #e5e8ef;" in note_rule
    assert "border-left: 4px solid #98a2b3;" in note_rule
    assert "#fff9ec" not in note_rule
    assert "#c99a34" not in note_rule

    assert "background: #fff9ec;" in material_rule
    assert "border: 1px solid #ead8aa;" in material_rule
    assert "border-left: 4px solid #c99a34;" in material_rule
