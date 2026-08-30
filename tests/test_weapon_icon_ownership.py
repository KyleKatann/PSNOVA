import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class WeaponIconOwnershipTests(unittest.TestCase):
    def test_weapon_summary_icon_has_one_owner(self):
        image_layout = (DOCS / "js" / "image-layout.js").read_text(encoding="utf-8")
        weapon_icons = (DOCS / "js" / "weapon-icons.js").read_text(encoding="utf-8")

        self.assertNotIn('summary.classList.add("native-icon-heading")', image_layout)
        self.assertNotIn('summary.style.setProperty("--native-icon"', image_layout)
        self.assertIn('details.classList.add("native-icon-table")', image_layout)
        self.assertIn('summary.insertBefore(icon, summary.firstChild)', weapon_icons)


if __name__ == "__main__":
    unittest.main()
