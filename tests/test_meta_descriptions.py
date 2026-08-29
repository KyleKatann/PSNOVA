import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE_META = ROOT / "docs" / "js" / "page-meta.js"


class MetaDescriptionTests(unittest.TestCase):
    def test_important_pages_define_descriptions(self):
        js = PAGE_META.read_text(encoding="utf-8")
        self.assertGreaterEqual(js.count("description:"), 18)
        for token in ("武器", "防具", "素材", "エネミー", "特殊能力", "トロフィー"):
            with self.subTest(token=token):
                self.assertIn(token, js)

    def test_description_meta_is_created_or_updated(self):
        js = PAGE_META.read_text(encoding="utf-8")
        self.assertIn('setNamedMeta("description", current.description)', js)
        self.assertIn('meta.setAttribute("content", content)', js)
        self.assertIn('document.head.appendChild(meta)', js)


if __name__ == "__main__":
    unittest.main()
