from pathlib import Path


PAGE_CSS = Path(__file__).resolve().parents[1] / "docs" / "css" / "page.css"


def test_technic_additional_material_row_is_yellow_with_normal_dark_text():
    css = PAGE_CSS.read_text(encoding="utf-8")

    assert ".technic-level-table tbody tr:nth-child(5)" in css
    assert "background: #fff8e8;" in css
    assert "color: var(--text);" in css
    assert "color: #7a5414;" not in css
    assert "#main.technic-detail-page .technic-material-note" in css
    assert "background: #fff9ec;" in css
