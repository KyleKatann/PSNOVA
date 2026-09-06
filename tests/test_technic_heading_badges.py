from pathlib import Path


PAGE_CSS = Path(__file__).resolve().parents[1] / "docs" / "css" / "page.css"


def test_technic_entry_titles_do_not_render_attribute_name_badges():
    css = PAGE_CSS.read_text(encoding="utf-8")

    assert ".technic-entry-title::before" in css
    assert ".technic-entry-title::after" not in css
    assert 'content: "炎属性"' not in css
    assert 'content: "氷属性"' not in css
