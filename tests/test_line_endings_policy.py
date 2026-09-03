import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATTRIBUTES = ROOT / ".gitattributes"


class LineEndingPolicyTests(unittest.TestCase):
    def test_repository_uses_lf_for_active_text_files(self):
        text = ATTRIBUTES.read_text(encoding="utf-8")

        self.assertIn("* text=auto eol=lf", text)

    def test_historical_sources_are_excluded_from_normalization(self):
        text = ATTRIBUTES.read_text(encoding="utf-8")

        self.assertIn("reference/** -text", text)
        self.assertIn("docs/pages/分類中/** -text", text)


if __name__ == "__main__":
    unittest.main()
