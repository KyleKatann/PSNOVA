import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MENUBAR = ROOT / "docs" / "js" / "menubar.js"
IMAGE_LAYOUT = MENUBAR
STYLE_ENTRY = ROOT / "docs" / "css" / "style.css"


class ImageLayoutTests(unittest.TestCase):
    def test_runtime_legacy_jpeg_cleanup_is_removed(self):
        js = IMAGE_LAYOUT.read_text(
            encoding="utf-8"
        )

        css = STYLE_ENTRY.read_text(
            encoding="utf-8"
        )

        for forbidden in (
            "function removeInternalScreenshots()",
            "function isInternalScreenshot",
            "image.remove();",
        ):
            with self.subTest(
                forbidden=forbidden
            ):
                self.assertNotIn(
                    forbidden,
                    js,
                )

        self.assertNotIn(
            '#main img[src$=".jpg"]',
            css,
        )

        self.assertNotIn(
            '#main img[src$=".jpeg"]',
            css,
        )

    def test_weapon_icons_are_not_runtime_mapped(self):
        js = IMAGE_LAYOUT.read_text(
            encoding="utf-8"
        )

        self.assertNotIn(
            "var weaponIcons",
            js,
        )
        self.assertNotIn(
            "native-icon-table",
            js,
        )
        self.assertNotIn(
            "details > summary",
            js,
        )

        for filename in (
            "sword.png",
            "partizan.png",
            "dsaber.png",
            "knuckle.png",
            "rifle.png",
            "tmachineg.png",
            "rod.png",
            "thalys.png",
            "wand.png",
            "halo.png",
            "pile.png",
        ):
            with self.subTest(filename=filename):
                self.assertTrue(
                    (
                        ROOT
                        / "docs"
                        / "img"
                        / "weapon"
                        / filename
                    ).exists()
                )

    def test_class_native_icons_are_mapped_and_present(self):
        js = IMAGE_LAYOUT.read_text(
            encoding="utf-8"
        )

        for label, filename in {
            "ハンター": "hunter.png",
            "レンジャー": "ranger.png",
            "フォース": "force.png",
            "バスター": "buster.png",
        }.items():
            with self.subTest(label=label):
                self.assertIn(label, js)

                self.assertTrue(
                    (
                        ROOT
                        / "docs"
                        / "img"
                        / "job"
                        / filename
                    ).exists()
                )


if __name__ == "__main__":
    unittest.main()
