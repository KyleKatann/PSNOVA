import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_TOOLS = ROOT / "docs" / "pages" / "tools"
TOOLS = ROOT / "tools"


class ToolLocationTests(unittest.TestCase):
    def test_generation_tools_are_outside_public_docs(self):
        self.assertFalse(PUBLIC_TOOLS.exists())
        self.assertTrue(TOOLS.exists())

    def test_core_generators_are_preserved(self):
        for directory in ("weapon_table_maker", "material_table_maker", "enemy_table_maker"):
            with self.subTest(directory=directory):
                self.assertTrue((TOOLS / directory).exists())


if __name__ == "__main__":
    unittest.main()
