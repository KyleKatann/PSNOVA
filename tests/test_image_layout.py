import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENUBAR = ROOT / "docs" / "js" / "menubar.js"
IMAGE_LAYOUT = ROOT / "docs" / "js" / "image-layout.js"
INTERACTION = ROOT / "docs" / "css" / "interaction.css"


class ImageLayoutTests(unittest.TestCase):
    def test_image_layout_script_is_loaded_globally(self):
        js = MENUBAR.read_text(encoding="utf-8")
        self.assertIn("/PSNOVA/js/image-layout.js", js)
        self.assertIn("data-psnova-image-layout", js)

    def test_known_large_images_have_explicit_dimensions(self):
        js = IMAGE_LAYOUT.read_text(encoding="utf-8")
        self.assertIn('"/PSNOVA/img/logo.png": { width: 660, height: 121 }', js)
        self.assertIn('"/PSNOVA/img/gigantes/gigantes.jpg": { width: 1000, height: 540 }', js)
        self.assertIn('image.setAttribute("width", String(dimensions.width))', js)
        self.assertIn('image.setAttribute("height", String(dimensions.height))', js)

    def test_unknown_images_are_not_guessed(self):
        js = IMAGE_LAYOUT.read_text(encoding="utf-8")
        self.assertIn("if (!pathname)", js)

    def test_internal_pages_remove_jpeg_screenshots_but_keep_small_png_icons(self):
        js = IMAGE_LAYOUT.read_text(encoding="utf-8")
        css = INTERACTION.read_text(encoding="utf-8")
        self.assertIn("function removeInternalScreenshots()", js)
        self.assertIn('/\\.jpe?g$/i.test(pathname)', js)
        self.assertIn("image.remove();", js)
        self.assertIn("html.internal-page #main img[src$=\".jpg\"]", css)

    def test_weapon_native_icons_are_mapped_and_present(self):
        js = IMAGE_LAYOUT.read_text(encoding="utf-8")
        icons = {
            "ソード": "sword.png",
            "パルチザン": "partizan.png",
            "ダブルセイバー": "dsaber.png",
            "ナックル": "knuckle.png",
            "アサルトライフル": "rifle.png",
            "ツインマシンガン": "tmachineg.png",
            "ロッド": "rod.png",
            "タリス": "thalys.png",
            "ウォンド": "wand.png",
            "ヘイロウ": "halo.png",
            "パイル": "pile.png",
        }
        for label, filename in icons.items():
            with self.subTest(label=label):
                self.assertIn(label, js)
                self.assertTrue((ROOT / "docs" / "img" / "weapon" / filename).exists())

    def test_class_native_icons_are_mapped_and_present(self):
        js = IMAGE_LAYOUT.read_text(encoding="utf-8")
        for label, filename in {
            "ハンター": "hunter.png",
            "レンジャー": "ranger.png",
            "フォース": "force.png",
            "バスター": "buster.png",
        }.items():
            with self.subTest(label=label):
                self.assertIn(label, js)
                self.assertTrue((ROOT / "docs" / "img" / "job" / filename).exists())


if __name__ == "__main__":
    unittest.main()
