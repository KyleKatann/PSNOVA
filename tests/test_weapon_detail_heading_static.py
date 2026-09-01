from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MENUBAR = ROOT / "docs" / "js" / "menubar.js"
STYLE = ROOT / "docs" / "css" / "style.css"
WEAPON_CSS = ROOT / "docs" / "css" / "weapon-tools.css"
LOCK_JS = ROOT / "docs" / "js" / "weapon-static-heading.js"
LOCK_CSS = ROOT / "docs" / "css" / "weapon-static-heading.css"
AGENT = ROOT / "Agent.md"
WEAPON_DIR = ROOT / "docs" / "pages" / "weapon"

WEAPONS = {
    "sword": ("ソード", "sword.png"),
    "partizan": ("パルチザン", "partizan.png"),
    "doublesaber": ("ダブルセイバー", "dsaber.png"),
    "knuckle": ("ナックル", "knuckle.png"),
    "rifle": ("アサルトライフル", "rifle.png"),
    "tmachinegun": ("ツインマシンガン", "tmachineg.png"),
    "rod": ("ロッド", "rod.png"),
    "talis": ("タリス", "thalys.png"),
    "wand": ("ウォンド", "wand.png"),
    "halo": ("ヘイロウ", "halo.png"),
    "pile": ("パイル", "pile.png"),
}


def test_weapon_detail_headings_are_static_source_markup():
    for slug, (label, icon) in WEAPONS.items():
        html = (
            WEAPON_DIR / f"{slug}.html"
        ).read_text(encoding="utf-8")

        assert (
            f'<h2><img class="weapon-type-icon" '
            f'src="/PSNOVA/img/weapon/{icon}" '
            f'alt="" width="30" height="30">'
            f'{label} 武器データ</h2>'
            in html
        )

        assert "<details" not in html
        assert "<summary" not in html


def test_legacy_disclosure_runtime_is_removed():
    menubar = MENUBAR.read_text(
        encoding="utf-8"
    )
    style = STYLE.read_text(
        encoding="utf-8"
    )

    assert not LOCK_JS.exists()
    assert not LOCK_CSS.exists()

    assert "weapon-static-heading" not in menubar
    assert "weapon-child-pending" not in menubar
    assert "weapon-static-heading.css" not in style


def test_static_heading_icon_style_lives_in_weapon_tools_css():
    css = WEAPON_CSS.read_text(
        encoding="utf-8"
    )

    assert (
        "#main.weapon-detail-page "
        "h2 .weapon-type-icon {"
        in css
    )

    assert "width: 30px;" in css
    assert "height: 30px;" in css


def test_static_weapon_heading_and_toolbar_rules_are_recorded():
    agent = AGENT.read_text(
        encoding="utf-8"
    )

    assert (
        "ordinary static `<h2>` weapon-type heading"
        in agent
    )
    assert (
        "must not rely on JavaScript "
        "to force a disclosure widget open"
        in agent
    )
    assert (
        "weapon search/filter toolbars use `position: sticky`"
        in agent
    )
    assert (
        "remain visible near the top of the viewport"
        in agent
    )
    assert "They use no card shadow." in agent
    assert (
        "weapon table header remains sticky below the toolbar"
        in agent
    )
