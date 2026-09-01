import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARED_JS = [
    ROOT / "docs" / "js" / "menubar.js",
    ROOT / "docs" / "js" / "sidebar.js",
]


class SharedJavascriptSafetyTests(unittest.TestCase):
    def test_invalid_append_child_string_calls_are_removed(self):
        for path in SHARED_JS:
            with self.subTest(path=path.name):
                js = path.read_text(encoding="utf-8")

                self.assertNotIn(
                    'appendChild("span")',
                    js,
                )
                self.assertNotIn(
                    "hoge!!",
                    js,
                )

    def test_ready_state_branch_is_removed(self):
        for path in SHARED_JS:
            with self.subTest(path=path.name):
                js = path.read_text(encoding="utf-8")

                self.assertNotIn(
                    'document.readyState!="complete"',
                    js,
                )

    def test_sidebar_fallback_insertion_target_exists(self):
        sidebar_js = (
            ROOT / "docs" / "js" / "sidebar.js"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'document.getElementById("contents")',
            sidebar_js,
        )

    def test_legacy_menubar_entrypoint_is_noop(self):
        menu_js = (
            ROOT / "docs" / "js" / "menubar.js"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "function menu() {}",
            menu_js,
        )


if __name__ == "__main__":
    unittest.main()
