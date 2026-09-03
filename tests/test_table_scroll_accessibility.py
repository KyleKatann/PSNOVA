import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / "docs" / "js" / "table-enhancements.js"
CSS = ROOT / "docs" / "css" / "style.css"


class TableScrollAccessibilityTests(unittest.TestCase):
    def test_generated_scroll_region_is_keyboard_focusable(self):
        js = JS.read_text(encoding="utf-8")

        self.assertIn(
            'wrapper.setAttribute("tabindex", "0");',
            js,
        )
        self.assertIn(
            'wrapper.setAttribute("role", "region");',
            js,
        )
        self.assertIn(
            'wrapper.setAttribute("aria-labelledby", ensureLabelSourceId(labelSource));',
            js,
        )

    def test_scroll_region_has_visible_focus_style(self):
        css = CSS.read_text(encoding="utf-8")

        self.assertIn(
            "#main .table-scroll:focus-visible",
            css,
        )


if __name__ == "__main__":
    unittest.main()
