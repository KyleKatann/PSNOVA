import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENUBAR = ROOT / "docs" / "js" / "menubar.js"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"


class InternalUrlTests(unittest.TestCase):
    def test_shared_internal_urls_are_root_relative(self):
        for path in (MENUBAR, SIDEBAR):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertNotIn("https://kylekatann.github.io/PSNOVA/", text)
                self.assertIn("/PSNOVA/", text)

    def test_affiliate_destination_remains_external(self):
        sidebar = SIDEBAR.read_text(encoding="utf-8")
        self.assertIn("https://hb.afl.rakuten.co.jp/", sidebar)

    def test_shared_asset_loaders_use_site_root_paths(self):
        menubar = MENUBAR.read_text(encoding="utf-8")
        for asset in (
            "/PSNOVA/css/modern.css",
            "/PSNOVA/css/site-search.css",
            "/PSNOVA/js/site-search.js",
            "/PSNOVA/js/table-semantics.js",
        ):
            with self.subTest(asset=asset):
                self.assertIn(asset, menubar)


if __name__ == "__main__":
    unittest.main()
