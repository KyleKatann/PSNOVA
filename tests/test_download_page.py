import html
import string
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOWNLOAD_PATH = DOCS / "pages" / "download.html"
DOWNLOAD_URL = "/PSNOVA/pages/download.html"


class DownloadPageTests(unittest.TestCase):
    def test_download_preserves_reference_content_sentinels(self):
        source = DOWNLOAD_PATH.read_text(encoding="utf-8")
        decoded = html.unescape(source)

        sentinels = [
            "アップデート一覧",
            "2015/03/26",
            "166MB",
            "プレイヤーレベルを200まで開放",
            "難易度エクストラハード追加",
            "経験値ブースト3倍 20個",
            "「EoE：ゼファー」セット",
            "「EoE：リーンベル」セット",
            "「EoE：ヴァシュロン」セット",
            "「SO4：エッジ」セット",
            "「SO4：レイミ」セット",
            "「VP：レナス」セット",
            "「戦場のヴァルキュリア3：リエラ」セット",
            "メモリーフラグメント集結",
            "経験値フェスティバル",
            "メモリーフラグメント回収",
            "スーパーラッピータイム",
            "経験値フィーバー",
            "グランエナジー・ラッシュ",
            "タイムアタック・古代都市",
            "ＰＴアタック・鋼の荒野",
            "タイムアタック・炎の高地",
            "ＰＴアタック・大尖塔",
            "難：炎の支配者",
            "波状防衛戦",
            "ガーネット編 第3話 暴走の果て",
            "サンシャウト編 第3話 盲目な追走",
            "ガーネット編 第2話 お料理大作戦",
            "サンシャウト編 第2話 見えぬ妨害",
            "ガーネット編 第1話 無敵艦隊、発進",
            "サンシャウト編 第1話 疑惑の捜査官",
            "ファンタシースター ノヴァ テーマ",
        ]

        for sentinel in sentinels:
            with self.subTest(sentinel=sentinel):
                self.assertIn(sentinel, decoded)

    def test_all_experience_boost_variants_are_preserved(self):
        source = DOWNLOAD_PATH.read_text(encoding="utf-8")

        for suffix in string.ascii_uppercase:
            with self.subTest(suffix=suffix):
                self.assertIn(
                    f"経験値ブースト3倍 A{suffix}",
                    source,
                )

    def test_download_does_not_restore_archived_wiki_chrome(self):
        source = DOWNLOAD_PATH.read_text(encoding="utf-8")

        forbidden = [
            "web.archive.org",
            "adsbygoogle",
            "paraedit.png",
            "saved_resource",
            "Wayback",
            "cmd=secedit",
        ]

        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, source)

    def test_download_uses_public_page_shell_and_discovery_surfaces(self):
        source = DOWNLOAD_PATH.read_text(encoding="utf-8")
        decoded = html.unescape(source)

        self.assertIn(
            "<title>PSNOVA攻略サイト - ダウンロードコンテンツ</title>",
            decoded,
        )
        self.assertIn(
            'rel="canonical" href="https://kylekatann.github.io/PSNOVA/pages/download.html"',
            source,
        )
        self.assertIn('<main id="main">', source)
        self.assertIn('<a class="skip-link" href="#main">本文へスキップ</a>', source)

        for script in (
            "openclose.js",
            "fixmenu_pagetop.js",
            "menubar.js",
            "sidebar.js",
        ):
            with self.subTest(script=script):
                self.assertIn(
                    f'<script defer src="/PSNOVA/js/{script}"></script>',
                    source,
                )

        sidebar = (DOCS / "js" / "sidebar.js").read_text(encoding="utf-8")
        self.assertIn(DOWNLOAD_URL, sidebar)
        self.assertIn("ダウンロードコンテンツ", html.unescape(sidebar))

        sitemap = (DOCS / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn(DOWNLOAD_URL, sitemap)

    def test_download_tables_use_static_semantic_headers(self):
        source = DOWNLOAD_PATH.read_text(encoding="utf-8")

        self.assertGreaterEqual(source.count("<table>"), 5)
        self.assertEqual(source.count("<thead>"), source.count("<table>"))
        self.assertNotIn("<thead><tr><td", source)
        self.assertIn('scope="colgroup" colspan="5">推奨レベル</th>', source)
        self.assertIn('scope="rowgroup" colspan="10">有料</th>', source)
        self.assertIn('scope="rowgroup" colspan="10">無料</th>', source)
        self.assertIn('scope="rowgroup" colspan="10">ストーリー(有料)</th>', source)


if __name__ == "__main__":
    unittest.main()
