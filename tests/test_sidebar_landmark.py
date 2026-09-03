import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"
QUALITY = ROOT / "tools" / "psnova_quality.py"


class SidebarLandmarkTests(unittest.TestCase):
    def test_shared_sidebar_uses_native_aside(self):
        source = SIDEBAR.read_text(encoding="utf-8")

        self.assertEqual(
            source.count('<aside id="sub">'),
            1,
        )
        self.assertEqual(
            source.count("</aside>"),
            1,
        )
        self.assertNotIn(
            '<div id="sub">',
            source,
        )

    def test_sidebar_navigation_remains_named(self):
        source = SIDEBAR.read_text(encoding="utf-8")

        self.assertIn(
            '<nav aria-label="攻略メニュー">',
            source,
        )

    def test_inventory_understands_generated_sidebar_landmark(self):
        source = QUALITY.read_text(encoding="utf-8")

        self.assertIn(
            "shared_sidebar_is_aside",
            source,
        )
        self.assertIn(
            "has_shared_sidebar",
            source,
        )
        self.assertIn(
            '"side();" in text',
            source,
        )


if __name__ == "__main__":
    unittest.main()
