import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHARED_JS = [
    ROOT / "docs" / "js" / "menubar.js",
    ROOT / "docs" / "js" / "sidebar.js",
]


class SharedRenderingTests(unittest.TestCase):
    def test_document_write_is_not_used(self):
        for path in SHARED_JS:
            with self.subTest(path=path.name):
                js = path.read_text(encoding="utf-8")
                self.assertNotIn("document.write", js)

    def test_shared_html_is_inserted_next_to_call_site(self):
        for path in SHARED_JS:
            with self.subTest(path=path.name):
                js = path.read_text(encoding="utf-8")
                self.assertIn('insertAdjacentHTML("beforebegin", html);', js)
                self.assertIn("document.currentScript", js)


if __name__ == "__main__":
    unittest.main()
