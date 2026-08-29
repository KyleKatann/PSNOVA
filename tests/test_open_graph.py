import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE_META = ROOT / "docs" / "js" / "page-meta.js"


class OpenGraphTests(unittest.TestCase):
    def test_core_open_graph_properties_are_set(self):
        js = PAGE_META.read_text(encoding="utf-8")
        for prop in ("og:title", "og:description", "og:type", "og:url", "og:site_name"):
            with self.subTest(prop=prop):
                self.assertIn('setPropertyMeta("' + prop + '"', js)

    def test_open_graph_reuses_page_metadata(self):
        js = PAGE_META.read_text(encoding="utf-8")
        self.assertIn('setPropertyMeta("og:title", current.title)', js)
        self.assertIn('setPropertyMeta("og:description", current.description)', js)
        self.assertIn('setOpenGraph(current, window.location.pathname)', js)


if __name__ == "__main__":
    unittest.main()
