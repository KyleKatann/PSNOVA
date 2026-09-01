from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_semantic_table_headers_are_explicitly_centered_after_body_alignment_rules():
    css = (ROOT / "docs/css/wiki-table.css").read_text(encoding="utf-8")
    marker = "User-corrected invariant: every semantic column-header row is centered."
    assert marker in css
    tail = css.split(marker, 1)[1]
    assert "#main table > thead th" in tail
    assert "text-align: center !important;" in tail


def test_weapon_ui_uses_clear_japanese_shop_level_label():
    script = (ROOT / "docs/js/weapon-tools.js").read_text(encoding="utf-8")
    assert "ショップレベル" in script
    for forbidden in ("Shop Lv", "ShopLv", "shopLv", "ショップLv"):
        assert forbidden not in script


def test_automatic_page_section_navigation_stays_removed():
    loader = (ROOT / "docs/js/menubar.js").read_text(encoding="utf-8")
    entry_css = (ROOT / "docs/css/style.css").read_text(encoding="utf-8")
    assert "section-nav.js" not in loader
    assert "section-nav.css" not in entry_css
    assert not (ROOT / "docs/js/section-nav.js").exists()
    assert not (ROOT / "docs/css/section-nav.css").exists()


def test_agent_guide_records_user_facing_table_rules():
    guide = (ROOT / "Agent.md").read_text(encoding="utf-8")
    assert "table column headers" in guide.lower()
    assert "ショップレベル" in guide
    assert "developer-facing" in guide.lower()
    assert "automatic in-page" in guide.lower()
