from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
STYLE = ROOT / "docs" / "css" / "style.css"
MODERN = ROOT / "docs" / "css" / "modern.css"
AFFILIATE_CSS = ROOT / "docs" / "css" / "affiliate.css"
AFFILIATE_JS = ROOT / "docs" / "js" / "affiliate-banner.js"
AGENT = ROOT / "Agent.md"


def test_all_public_pages_use_full_main_column_without_internal_page_image_suppression():
    html = INDEX.read_text(encoding="utf-8")
    style = STYLE.read_text(encoding="utf-8")
    modern = MODERN.read_text(encoding="utf-8")

    assert '<body class="homepage">' in html
    assert 'alt="PSNOVAのギガンテス"' in html

    assert "#main p {" in modern

    global_rule = modern.rsplit(
        "#main p {",
        1,
    )[1].split("}", 1)[0]

    assert "max-width: none;" in global_rule
    assert "max-width: 82ch;" not in modern
    assert "#main p {" not in style
    assert "body.homepage #main p" not in style
    assert 'body:not(.homepage) #main img[src$=".jpg"]' not in style


def test_affiliate_banner_is_two_equal_columns_on_desktop():
    css = AFFILIATE_CSS.read_text(encoding="utf-8")
    js = AFFILIATE_JS.read_text(encoding="utf-8")

    assert "grid-template-columns: repeat(2, minmax(0, 1fr));" in css
    assert ".affiliate-banner-item" in css
    assert "height: 76px;" in css
    assert "width: 100%;" in css
    assert "height: 100%;" in css
    assert "object-fit: contain;" in css
    assert "pickBanners(2)" in js
    assert 'affiliate-banner-item' in js


def test_affiliate_banner_collapses_to_one_visible_item_on_mobile():
    css = AFFILIATE_CSS.read_text(encoding="utf-8")

    assert "@media (max-width: 800px)" in css
    assert "grid-template-columns: 1fr;" in css
    assert ".affiliate-banner-item:nth-child(n + 2)" in css
    mobile_second_item = css.split(".affiliate-banner-item:nth-child(n + 2)", 1)[1].split("}", 1)[0]
    assert "display: none;" in mobile_second_item


def test_user_corrected_specs_are_recorded_as_invariants():
    agent = AGENT.read_text(encoding="utf-8")

    assert "Every user-reported regression that establishes a corrected specification" in agent
    assert "Correction-derived invariants" in agent
    assert "Weapon section headings show exactly one weapon icon" in agent
    assert "トアス種, ゴルドス種, and アフォル種" in agent
    assert "Affiliate/PR presentation on desktop uses two equal-width banner slots" in agent
    assert "All public pages should use the available main-content width naturally" in agent
