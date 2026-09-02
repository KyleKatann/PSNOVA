import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SIDEBAR_JS = ROOT / "docs" / "js" / "sidebar.js"
STYLE = ROOT / "docs" / "css" / "style.css"


class MobileLayoutTests(unittest.TestCase):
    def test_mobile_layout_uses_css_order_without_runtime_dom_reordering(self):
        js = SIDEBAR_JS.read_text(encoding="utf-8")
        css = STYLE.read_text(encoding="utf-8")

        self.assertNotIn("prioritizeMainOnMobile", js)
        self.assertNotIn("contents.insertBefore(main, sub);", js)
        self.assertIn("#main {\n        width: 100%;\n        order: 1;", css)
        self.assertIn("#sub {\n        width: 100%;\n        flex-basis: auto;\n        order: 2;", css)


if __name__ == "__main__":
    unittest.main()
