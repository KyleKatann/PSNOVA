from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MENUBAR = ROOT / "docs" / "js" / "menubar.js"
LOCK_JS = ROOT / "docs" / "js" / "weapon-static-heading.js"
STYLE = ROOT / "docs" / "css" / "style.css"
LOCK_CSS = ROOT / "docs" / "css" / "weapon-static-heading.css"
AGENT = ROOT / "Agent.md"


def test_weapon_child_pages_load_static_heading_behavior():
    js = MENUBAR.read_text(encoding="utf-8")
    assert "isWeaponChild" in js
    assert "/PSNOVA/js/weapon-static-heading.js" in js
    assert "data-psnova-weapon-static-heading" in js


def test_static_heading_blocks_disclosure_toggle_inputs():
    js = LOCK_JS.read_text(encoding="utf-8")
    assert 'event.preventDefault()' in js
    assert 'event.key !== "Enter"' in js
    assert 'event.key !== " "' in js
    assert 'details.open = true' in js
    assert 'tabindex", "-1"' in js


def test_weapon_detail_heading_has_no_disclosure_affordance():
    entry = STYLE.read_text(encoding="utf-8")
    css = LOCK_CSS.read_text(encoding="utf-8")
    assert '@import url("/PSNOVA/css/weapon-static-heading.css");' in entry
    assert "pointer-events: none" in css
    assert "::-webkit-details-marker" in css
    assert 'content: ""' in css


def test_static_weapon_heading_rule_is_recorded():
    agent = AGENT.read_text(encoding="utf-8")
    assert "weapon-type heading above the table permanently expanded and non-interactive" in agent
