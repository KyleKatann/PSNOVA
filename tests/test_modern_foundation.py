import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODERN_CSS = ROOT / "docs" / "css" / "modern.css"
STYLE_ENTRY = ROOT / "docs" / "css" / "style.css"
MENUBAR_JS = ROOT / "docs" / "js" / "menubar.js"


class ModernFoundationTests(unittest.TestCase):
    def test_modern_stylesheet_has_core_tokens(self):
        css = MODERN_CSS.read_text(encoding="utf-8")
        for token in (
            "--page-bg:",
            "--surface:",
            "--text:",
            "--border:",
            "--accent:",
            "box-sizing: border-box",
            "a:focus-visible",
        ):
            with self.subTest(token=token):
                self.assertIn(token, css)

    def test_mobile_typography_does_not_drop_to_legacy_12px(self):
        css = MODERN_CSS.read_text(encoding="utf-8")
        self.assertIn("@media screen and (max-width: 480px)", css)
        self.assertIn("font-size: 14px", css)

    def test_modern_stylesheet_is_loaded_from_initial_css_entrypoint(self):
        css = STYLE_ENTRY.read_text(encoding="utf-8")
        js = MENUBAR_JS.read_text(encoding="utf-8")
        self.assertIn('@import url("/PSNOVA/css/modern.css");', css)
        self.assertNotIn("addStylesheetOnce", js)
        self.assertNotIn("document.head.appendChild(link);", js)


if __name__ == "__main__":
    unittest.main()
