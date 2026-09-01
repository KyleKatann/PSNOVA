import html
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
FAQ_PATH = DOCS / "pages" / "faq.html"
FAQ_URL = "/PSNOVA/pages/faq.html"


class ReferencePageMigrationTests(unittest.TestCase):
    def test_faq_preserves_reference_content_sentinels(self):
        source = FAQ_PATH.read_text(encoding="utf-8")

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
                self.assertIn(
                    sentinel,
                    source,
                )

    def test_faq_removes_archive_provenance_notice(self):
        source = FAQ_PATH.read_text(encoding="utf-8")

        self.assertNotIn(
            "旧PSNOVA攻略Wikiの保存内容から、攻略本文を整理して再掲載しています。時点依存の記述を含みます。",
            source,
        )

    def test_faq_does_not_restore_archived_wiki_chrome(self):
        source = FAQ_PATH.read_text(encoding="utf-8")

        forbidden = [
            "web.archive.org",
            "adsbygoogle",
            "paraedit.png",
            "saved_resource",
            "Wayback",
        ]

        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(
                    token,
                    source,
                )

    def test_faq_uses_beginner_qa_name_on_shared_discovery_surfaces(self):
        expected_label = "初心者Q&A"

        for path in (
            DOCS / "js" / "sidebar.js",
            DOCS / "js" / "site-search.js",
        ):
            with self.subTest(
                path=path.relative_to(ROOT)
            ):
                text = path.read_text(
                    encoding="utf-8"
                )

                self.assertIn(
                    FAQ_URL,
                    text,
                )
                self.assertIn(
                    expected_label,
                    html.unescape(text),
                )

        source = FAQ_PATH.read_text(
            encoding="utf-8"
        )

        decoded = html.unescape(source)

        self.assertIn(
            "PSNOVA攻略サイト - 初心者Q&A",
            decoded,
        )

        self.assertIn(
            'rel="canonical" '
            'href="https://kylekatann.github.io'
            '/PSNOVA/pages/faq.html"',
            source,
        )

    def test_faq_url_remains_registered_in_sitemap(self):
        self.assertIn(
            FAQ_URL,
            (
                DOCS / "sitemap.xml"
            ).read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
