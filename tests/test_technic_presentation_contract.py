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
        "Technic material-legend text uses the same `#26384d` text color as ordinary data tables",
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


def test_technic_tables_fit_coarse_pointer_desktop_layout_without_horizontal_growth():
    css = PAGE_CSS.read_text(encoding="utf-8")
    coarse = css.split(
        "/* Smartphone desktop-site mode keeps Technic Lv tables inside the main column.", 1
    )[1].split("@media screen and (max-width: 800px)", 1)[0]

    assert "@media screen and (min-width: 801px) and (pointer: coarse)" in coarse
    assert "#main.technic-detail-page .technic-level-scroll > .technic-level-table" in coarse
    assert "width: 100%;" in coarse
    assert "min-width: 100%;" in coarse
    assert "max-width: 100%;" in coarse
    assert "white-space: normal;" in coarse
    assert "width: 120px;" in coarse
    assert "min-width: 120px;" in coarse
    assert "overflow-wrap: anywhere;" in coarse
    assert "max-content" not in coarse


def test_technic_descriptions_match_gray_blue_accent_pattern_and_material_legends_are_yellow():
    css = PAGE_CSS.read_text(encoding="utf-8")

    note_rule = css.split("#main.technic-detail-page .technic-note {", 1)[1].split("}", 1)[0]
    material_rule = css.split("#main.technic-detail-page .technic-material-note {", 1)[1].split("}", 1)[0]

    assert "background: var(--surface-subtle);" in note_rule
    assert "border: 1px solid #e5e8ef;" in note_rule
    assert "border-left: 4px solid var(--accent);" in note_rule
    assert "#98a2b3" not in note_rule
    assert "#fff9ec" not in note_rule
    assert "#c99a34" not in note_rule

    assert "color: #26384d;" in material_rule
    assert "color: #614714;" not in material_rule
    assert "background: #fff9ec;" in material_rule
    assert "border: 1px solid #ead8aa;" in material_rule
    assert "border-left: 4px solid #c99a34;" in material_rule
