import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENUBAR = ROOT / "docs" / "js" / "menubar.js"
PAGE_META = ROOT / "docs" / "js" / "page-meta.js"

IMPORTANT_PATHS = (
    "/PSNOVA/",
    "/PSNOVA/index.html",
    "/PSNOVA/pages/weapon.html",
    "/PSNOVA/pages/armor.html",
    "/PSNOVA/pages/attachment.html",
    "/PSNOVA/pages/specialability.html",
    "/PSNOVA/pages/material.html",
    "/PSNOVA/pages/enemy.html",
    "/PSNOVA/pages/gigantes.html",
    "/PSNOVA/pages/appearance.html",
    "/PSNOVA/pages/trophy.html",
)


class PageTitleTests(unittest.TestCase):
    def test_page_metadata_loader_is_global(self):
        js = MENUBAR.read_text(encoding="utf-8")
        self.assertIn("/PSNOVA/js/page-meta.js", js)
        self.assertIn("data-psnova-page-meta", js)

    def test_important_pages_have_unique_title_definitions(self):
        js = PAGE_META.read_text(encoding="utf-8")
        for path in IMPORTANT_PATHS:
            with self.subTest(path=path):
                self.assertIn('"' + path + '"', js)
        titles = []
        for line in js.splitlines():
            if "title:" in line:
                title = line.split('title: "', 1)[1].rsplit('"', 1)[0]
                titles.append(title)
        self.assertEqual(len(titles), len(set(titles)) + 1)  # root and index intentionally share a title

    def test_title_is_applied_to_document(self):
        js = PAGE_META.read_text(encoding="utf-8")
        self.assertIn("document.title = current.title", js)


if __name__ == "__main__":
    unittest.main()
