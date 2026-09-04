from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OPEN_CLOSE = ROOT / "docs" / "js" / "openclose.js"
KEYBOARD_SPEC = ROOT / "tests" / "ui" / "keyboard.spec.js"


def test_mobile_menu_reorders_trigger_before_binding():
    source = OPEN_CLOSE.read_text(encoding="utf-8")

    assert 'document.querySelector("#container > header")' in source
    assert "header.appendChild(button)" in source
    assert "placeContentsDrawerTrigger(button, isContentsDrawer);" in source


def test_mobile_menu_moves_focus_into_drawer_and_back_on_escape():
    source = OPEN_CLOSE.read_text(encoding="utf-8")

    assert 'menu.querySelector("a[href]")' in source
    assert "firstLink.focus();" in source
    assert 'event.key === "Escape"' in source
    assert "button.focus();" in source


def test_browser_keyboard_regression_exists():
    source = KEYBOARD_SPEC.read_text(encoding="utf-8")

    assert "mobile-chromium" in source
    assert "await expect(trigger).toBeFocused();" in source
    assert "await expect(firstMenuLink).toBeFocused();" in source
    assert "await page.keyboard.press('Escape');" in source
