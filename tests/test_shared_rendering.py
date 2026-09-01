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

    def test_sidebar_html_is_inserted_next_to_call_site(self):
        js = SIDEBAR.read_text(encoding="utf-8")

        self.assertIn(
            'insertAdjacentHTML("beforebegin", html);',
            js,
        )
        self.assertIn(
            "document.currentScript",
            js,
        )

    def test_menubar_is_compatibility_noop(self):
        js = MENUBAR.read_text(encoding="utf-8")

        self.assertIn(
            "function menu() {}",
            js,
        )
        self.assertNotIn(
            'insertAdjacentHTML("beforebegin", html);',
            js,
        )


if __name__ == "__main__":
    unittest.main()
