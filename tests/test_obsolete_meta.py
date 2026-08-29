import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE_META = ROOT / "docs" / "js" / "page-meta.js"


class ObsoleteMetaTests(unittest.TestCase):
    def test_meta_keywords_are_removed_at_runtime(self):
        js = PAGE_META.read_text(encoding="utf-8")
        self.assertIn('querySelectorAll(\'meta[name="keywords"]\')', js)
        self.assertIn("meta.parentNode.removeChild(meta)", js)
        self.assertIn("removeObsoleteMeta();", js)


if __name__ == "__main__":
    unittest.main()
