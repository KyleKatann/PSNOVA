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
            "初心者Q&amp;A",
            "ゲストクルー",
            "コア精錬所",
            "エクストラハードでは、どう育成すればいい？",
            "PSO2プレイヤー向けQ&amp;A",
            "PSO2クルー",
        ]
        for sentinel in sentinels:
            with self.subTest(sentinel=sentinel):
                self.assertIn(sentinel, html)

    def test_faq_removes_archive_provenance_notice(self):
        html = FAQ_PATH.read_text(encoding="utf-8")
        self.assertNotIn(
            "旧PSNOVA攻略Wikiの保存内容から、攻略本文を整理して再掲載しています。時点依存の記述を含みます。",
            html,
        )

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

    def test_faq_uses_beginner_qa_name_on_shared_discovery_surfaces(self):
        expected_label = "初心者Q&A"
        paths = [
            DOCS / "js" / "sidebar.js",
            DOCS / "js" / "page-meta.js",
            DOCS / "js" / "site-search.js",
        ]
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT)):
                text = path.read_text(encoding="utf-8")
                self.assertIn(FAQ_URL, text)
                self.assertIn(expected_label, text)

    def test_faq_url_remains_registered_in_sitemap(self):
        self.assertIn(FAQ_URL, (DOCS / "sitemap.xml").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
