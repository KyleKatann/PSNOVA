import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
FAQ_PATH = DOCS / "pages" / "faq.html"
FAQ_URL = "/PSNOVA/pages/faq.html"


class ReferencePageMigrationTests(unittest.TestCase):
    def test_faq_preserves_reference_content_sentinels(self):
        html = FAQ_PATH.read_text(encoding="utf-8")
        sentinels = [
            "体験版でよくある質問",
            "ゲストクルー",
            "コア精錬所",
            "エクストラハードからはどうすれば？",
            "PSO2プレイヤーに対するQ&amp;A",
            "PSO2クルー",
        ]
        for sentinel in sentinels:
            with self.subTest(sentinel=sentinel):
                self.assertIn(sentinel, html)

    def test_faq_does_not_restore_archived_wiki_chrome(self):
        html = FAQ_PATH.read_text(encoding="utf-8")
        forbidden = [
            "web.archive.org",
            "adsbygoogle",
            "paraedit.png",
            "saved_resource",
            "Wayback",
        ]
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, html)

    def test_faq_is_registered_in_shared_discovery_surfaces(self):
        paths = [
            DOCS / "js" / "sidebar.js",
            DOCS / "js" / "page-meta.js",
            DOCS / "js" / "site-search.js",
            DOCS / "sitemap.xml",
        ]
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertIn(FAQ_URL, path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
