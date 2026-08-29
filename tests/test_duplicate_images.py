import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"
DUPLICATE = ROOT / "docs" / "img" / "title.jpg"
SHARED_HERO = ROOT / "docs" / "img" / "gigantes" / "gigantes.jpg"


class DuplicateImageTests(unittest.TestCase):
    def test_duplicate_title_image_is_removed(self):
        self.assertFalse(DUPLICATE.exists())
        self.assertTrue(SHARED_HERO.exists())

    def test_home_page_reuses_shared_hero(self):
        html = INDEX.read_text(encoding="utf-8")
        self.assertIn("/PSNOVA/img/gigantes/gigantes.jpg", html)
        self.assertNotIn("/PSNOVA/img/title.jpg", html)


if __name__ == "__main__":
    unittest.main()
