import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE_ENTRY = ROOT / "docs" / "css" / "style.css"
INTERACTION = ROOT / "docs" / "css" / "interaction.css"


class InteractionStyleTests(unittest.TestCase):
    def test_interaction_styles_are_loaded_globally(self):
        css = STYLE_ENTRY.read_text(encoding="utf-8")
        self.assertIn('@import url("/PSNOVA/css/interaction.css");', css)

    def test_transitions_are_short_and_restrained(self):
        css = INTERACTION.read_text(encoding="utf-8")
        self.assertIn("transition-duration: 120ms", css)
        self.assertNotIn("1s", css.lower())

    def test_reduced_motion_is_respected(self):
        css = INTERACTION.read_text(encoding="utf-8")
        self.assertIn("prefers-reduced-motion: reduce", css)
        self.assertIn("transition-duration: 0.01ms !important", css)


if __name__ == "__main__":
    unittest.main()
