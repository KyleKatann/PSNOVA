import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RepositoryConcernTests(unittest.TestCase):
    def test_core_repository_concerns_are_separated(self):
        self.assertTrue((ROOT / "docs").is_dir())
        self.assertTrue((ROOT / "tools").is_dir())
        self.assertTrue((ROOT / "data").is_dir())

    def test_public_docs_do_not_contain_generation_tools(self):
        self.assertFalse((ROOT / "docs" / "pages" / "tools").exists())

    def test_data_contract_is_documented(self):
        text = (ROOT / "data" / "README.md").read_text(encoding="utf-8")
        self.assertIn("source-of-truth", text)
        self.assertIn("docs/", text)
        self.assertIn("tools/", text)


if __name__ == "__main__":
    unittest.main()
