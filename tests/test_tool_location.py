import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_TOOLS = ROOT / "docs" / "pages" / "tools"
TOOLS = ROOT / "tools"


class ToolLocationTests(unittest.TestCase):
    def test_repository_tools_are_outside_public_docs(self):
        self.assertFalse(PUBLIC_TOOLS.exists())
        self.assertTrue(TOOLS.exists())


if __name__ == "__main__":
    unittest.main()
