from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "docs" / "pages" / "gigantes.html"
CSS = ROOT / "docs" / "css" / "wiki-table.css"
AGENT = ROOT / "Agent.md"


def test_gigantes_desktop_table_does_not_scroll_horizontally():
    css = CSS.read_text(encoding="utf-8")

    assert "#main .gigantes-table-scroll {" in css
    assert "overflow: visible;" in css

    assert "#main .gigantes-table {" in css
    assert "max-width: 100%;" in css
    assert "min-width: 0;" in css


def test_gigantes_mobile_table_remains_horizontally_scrollable():
    css = CSS.read_text(encoding="utf-8")

    assert "@media screen and (max-width: 800px)" in css
    assert "overflow-x: auto;" in css
    assert "min-width: 1100px;" in css


def test_gigantes_notes_wrap_and_quest_entries_do_not():
    css = CSS.read_text(encoding="utf-8")

    assert "#main .gigantes-table td:nth-last-child(2)" in css
    assert "white-space: normal;" in css
    assert "overflow-wrap: anywhere;" in css

    assert "#main .gigantes-table td:last-child" in css
    assert "white-space: nowrap;" in css


def test_gigantes_stage_labels_use_explicit_cell_breaks():
    html = HTML.read_text(encoding="utf-8")

    expected = (
        "レイブヒュフテ<br>(第一段階)",
        "レイヴガイスト<br>(第二段階)",
        "ネメスフース<br>(第一段階)",
        "ネメスヒュフテ<br>(第二段階)",
        "ネメスガイスト<br>(第三段階)",
    )

    for value in expected:
        assert value in html

    for value in (
        "レイブヒュフテ(第一段階)",
        "レイヴガイスト(第二段階)",
        "ネメスフース(第一段階)",
        "ネメスヒュフテ(第二段階)",
        "ネメスガイスト(第三段階)",
    ):
        assert value not in html


def test_gigantes_layout_rules_are_recorded_in_agent():
    agent = AGENT.read_text(encoding="utf-8")

    assert "Gigantes data tables must fit within the main content width" in agent
    assert "must not use horizontal scrolling" in agent
    assert "`難易度SH以降での出現クエスト` column must stay on one line" in agent
    assert "`備考` column is the flexible wrapping column" in agent
    assert "explicit cell-internal `<br>`" in agent
