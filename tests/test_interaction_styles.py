import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / "docs" / "css" / "style.css"


class InteractionStyleTests(unittest.TestCase):
    def test_interaction_styles_are_in_sitewide_bundle(self):
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn("/* === INTERACTION AND RESPONSIVE NAV === */", css)
        self.assertNotIn("@import", css)

    def test_transitions_are_short_and_restrained(self):
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn("transition-duration: 120ms", css)
        self.assertNotIn("1s", css.lower())

    def test_reduced_motion_is_respected(self):
        css = STYLE.read_text(encoding="utf-8")
        self.assertIn("prefers-reduced-motion: reduce", css)
        self.assertIn("transition-duration: 0.01ms !important", css)


if __name__ == "__main__":
    unittest.main()
