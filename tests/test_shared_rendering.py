import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENUBAR = ROOT / "docs" / "js" / "menubar.js"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"


class SharedRenderingTests(unittest.TestCase):
    def test_document_write_is_not_used(self):
        for path in (MENUBAR, SIDEBAR):
            with self.subTest(path=path.name):
                js = path.read_text(encoding="utf-8")
                self.assertNotIn(
                    "document.write",
                    js,
                )

    def test_sidebar_html_is_inserted_before_main_without_call_site_dependency(self):
        js = SIDEBAR.read_text(encoding="utf-8")

        self.assertIn(
            'var main = contents.querySelector("#main");',
            js,
        )
        self.assertIn(
            'main.insertAdjacentHTML("beforebegin", html);',
            js,
        )
        self.assertNotIn(
            "document.currentScript",
            js,
        )
        self.assertIn(
            "function initSidebar()",
            js,
        )

    def test_obsolete_menu_compatibility_api_is_removed(self):
        js = MENUBAR.read_text(encoding="utf-8")

        self.assertNotIn(
            "function menu()",
            js,
        )
        self.assertNotIn(
            "compatibility no-op",
            js,
        )


if __name__ == "__main__":
    unittest.main()
