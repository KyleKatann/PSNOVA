import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODERN_CSS = ROOT / "docs" / "css" / "modern.css"
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

    def test_modern_stylesheet_is_loaded_globally(self):
        js = MENUBAR_JS.read_text(encoding="utf-8")
        self.assertIn("/PSNOVA/css/modern.css", js)
        self.assertIn('data-psnova-modern', js)
        self.assertIn("document.head.appendChild(link);", js)


if __name__ == "__main__":
    unittest.main()
