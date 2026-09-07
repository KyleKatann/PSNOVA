import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENUBAR = ROOT / "docs" / "js" / "menubar.js"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"
STYLE = ROOT / "docs" / "css" / "style.css"


class InternalUrlTests(unittest.TestCase):
    def test_shared_internal_urls_are_root_relative(self):
        for path in (MENUBAR, SIDEBAR):
            text = path.read_text(encoding="utf-8")

            with self.subTest(path=path.name):
                self.assertNotIn(
                    "https://kylekatann.github.io/PSNOVA/",
                    text,
                )
                self.assertIn("/PSNOVA/", text)

    def test_affiliate_destination_remains_external(self):
        menubar = MENUBAR.read_text(encoding="utf-8")

        self.assertIn(
            "https://hb.afl.rakuten.co.jp/",
            menubar,
        )
        self.assertIn(
            'rel="nofollow sponsored noopener"',
            menubar,
        )

    def test_retired_shared_script_loaders_stay_removed(self):
        menubar = MENUBAR.read_text(encoding="utf-8")
        style = STYLE.read_text(encoding="utf-8")

        for retired in (
            "/PSNOVA/js/site-search.js",
            "/PSNOVA/js/table-enhancements.js",
        ):
            with self.subTest(retired=retired):
                self.assertNotIn(retired, menubar)

        self.assertIn(
            "/PSNOVA/css/page.css",
            menubar,
        )

        for legacy in (
            "modern.css",
            "site-search.css",
            "interaction.css",
        ):
            with self.subTest(legacy=legacy):
                self.assertNotIn(legacy, menubar)
                self.assertNotIn(legacy, style)

        self.assertNotIn(
            "table-semantics.js",
            menubar,
        )
        self.assertNotIn(
            "data-psnova-table-semantics",
            menubar,
        )


if __name__ == "__main__":
    unittest.main()
