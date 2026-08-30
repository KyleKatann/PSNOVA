import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class PublicNavigationCoverageTests(unittest.TestCase):
    def test_class_and_skill_pages_are_linked_from_sidebar(self):
        sidebar = (DOCS / "js" / "sidebar.js").read_text(encoding="utf-8")
        self.assertIn('/PSNOVA/pages/class.html', sidebar)
        self.assertIn('/PSNOVA/pages/skill.html', sidebar)


if __name__ == "__main__":
    unittest.main()
