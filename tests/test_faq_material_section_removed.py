from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FAQ = ROOT / "docs" / "pages" / "faq.html"


def test_beginner_qa_does_not_include_material_lookup_subsection():
    html = FAQ.read_text(encoding="utf-8")
    assert "必要な素材が見つからない" not in html
    assert "ダーカーの皮片：" not in html
    assert "ダーカーの殻片：" not in html
    assert "青い鉱石：" not in html
