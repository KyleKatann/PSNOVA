import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class WeaponPileTests(unittest.TestCase):
    def test_pile_section_uses_pile_dataset(self):
        html = (ROOT / "docs" / "pages" / "weapon" / "pile.html").read_text(encoding="utf-8")
        match = re.search(
            r'<table class="weapon-data-table"[^>]*data-weapon-type="パイル"[^>]*>(.*?)</table>',
            html,
            re.DOTALL,
        )
        self.assertIsNotNone(match)

        section = match.group(1)
        self.assertIn(
            "<tr><td>パイル</td><td>3</td><td>579</td><td>529</td>",
            section,
        )
        self.assertIn(
            "<tr><td>スペキュレイナー</td><td>15</td><td>5921</td><td>5921</td>",
            section,
        )
        self.assertNotIn("<tr><td>ロッド</td>", section)


if __name__ == "__main__":
    unittest.main()