import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_semantic_table_headers_are_explicitly_centered_after_body_alignment_rules():
    css = (ROOT / "docs/css/style.css").read_text(encoding="utf-8")
    marker = "User-corrected invariant: every semantic column-header row is centered."
    assert marker in css
    tail = css.split(marker, 1)[1]
    assert "#main table > thead th" in tail
    assert "text-align: center !important;" in tail


def test_public_table_headers_use_clear_japanese_shop_level_label():
    docs = ROOT / "docs"
    forbidden = ("Shop Lv", "ShopLv", "shopLv", "ショップLv")

    for path in docs.rglob("*.html"):
        if "分類中" in path.parts:
            continue

        text = path.read_text(encoding="utf-8")
        headers = re.findall(r"<th\b[^>]*>(.*?)</th>", text, flags=re.I | re.S)
        for header in headers:
            label = html.unescape(re.sub(r"<[^>]+>", "", header)).strip()
            for forbidden_label in forbidden:
                assert forbidden_label not in label, (
                    f"{path.relative_to(ROOT)} のheaderに {forbidden_label!r} が含まれている"
                )


def test_consumable_material_quantities_use_multiplication_sign():
    html_source = (ROOT / "docs/pages/item.html").read_text(encoding="utf-8")
    assert "グランピース×1" in html_source
    assert "グランピースx" not in html_source


def test_automatic_page_section_navigation_stays_removed():
    loader = (ROOT / "docs/js/menubar.js").read_text(encoding="utf-8")
    entry_css = (ROOT / "docs/css/style.css").read_text(encoding="utf-8")
    assert "section-nav.js" not in loader
    assert "section-nav.css" not in entry_css
    assert not (ROOT / "docs/js/section-nav.js").exists()
    assert not (ROOT / "docs/css/section-nav.css").exists()


