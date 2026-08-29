import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
GITIGNORE = ROOT / ".gitignore"


class NotebookCheckpointTests(unittest.TestCase):
    def test_no_notebook_checkpoint_directories_are_tracked(self):
        checkpoints = list(TOOLS.rglob(".ipynb_checkpoints")) if TOOLS.exists() else []
        self.assertEqual([], checkpoints)

    def test_notebook_checkpoints_are_ignored(self):
        text = GITIGNORE.read_text(encoding="utf-8")
        self.assertIn(".ipynb_checkpoints/", text)
        self.assertIn("**/.ipynb_checkpoints/", text)


if __name__ == "__main__":
    unittest.main()
