from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT = ROOT / "Agent.md"
PAGE_CSS = ROOT / "docs" / "css" / "page.css"


def test_agent_records_technic_presentation_contract():
    guide = AGENT.read_text(encoding="utf-8")

    for rule in (
        "All public data tables use the same square-corner treatment",
        "Every technic entry must include a reader-facing description in static HTML",
        "use the PSO2 Wiki only as a secondary source",
        "Never copy source wording verbatim",
        "Existing technic descriptions imported from the archived Wiki must also be rewritten",
        "Technic Lv tables use the same column geometry across every technique and every attribute",
        "Technic supplementary notes and material legends use one consistent yellow highlight treatment",
    ):
        assert rule in guide


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


def test_technic_notes_share_one_yellow_highlight_style():
    css = PAGE_CSS.read_text(encoding="utf-8")

    assert (
        "#main.technic-detail-page .technic-note,\n"
        "#main.technic-detail-page .technic-material-note"
    ) in css
    assert "background: #fff9ec;" in css
    assert "border: 1px solid #ead8aa;" in css
    assert "border-left: 4px solid #c99a34;" in css
