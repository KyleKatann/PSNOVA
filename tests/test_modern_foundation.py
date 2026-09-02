import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "docs" / "css" / "style.css"
MENUBAR_JS = ROOT / "docs" / "js" / "menubar.js"


class ModernFoundationTests(unittest.TestCase):
    def test_sitewide_stylesheet_has_core_tokens(self):
        css = STYLE.read_text(encoding="utf-8")
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
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn("@media screen and (max-width: 480px)", css)
        self.assertIn("font-size: 14px", css)

    def test_sitewide_stylesheet_is_loaded_directly_without_import_chain(self):
        css = STYLE.read_text(encoding="utf-8")
        js = MENUBAR_JS.read_text(encoding="utf-8")

        self.assertNotIn("@import", css)
        self.assertNotIn("/PSNOVA/css/style.css", js)
        self.assertNotIn("addStylesheetOnce", js)


if __name__ == "__main__":
    unittest.main()
