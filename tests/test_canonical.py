import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE_META = ROOT / "docs" / "js" / "page-meta.js"


class CanonicalTests(unittest.TestCase):
    def test_canonical_link_is_created_or_updated(self):
        js = PAGE_META.read_text(encoding="utf-8")
        self.assertIn('querySelector(\'link[rel="canonical"]\')', js)
        self.assertIn('canonical.setAttribute("rel", "canonical")', js)
        self.assertIn('canonical.setAttribute("href", "https://kylekatann.github.io" + pathname)', js)

    def test_canonical_uses_current_path_without_redirecting(self):
        js = PAGE_META.read_text(encoding="utf-8")
        self.assertIn("setCanonical(window.location.pathname)", js)
        self.assertNotIn("window.location.replace", js)
        self.assertNotIn("window.location.href =", js)


if __name__ == "__main__":
    unittest.main()
