import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class WeaponPileTests(unittest.TestCase):
    def test_pile_section_uses_pile_dataset(self):
        html = (ROOT / "docs" / "pages" / "weapon" / "pile.html").read_text(encoding="utf-8")
        match = re.search(
            r"<summary>パイル</summary>(.*?)</details>",
            html,
            re.DOTALL,
        )
        self.assertIsNotNone(match)

        section = match.group(1)
        self.assertIn(
            "<tr><th>パイル</th><th>3</th><th>579</th><th>529</th>",
            section,
        )
        self.assertIn(
            "<tr><th>スペキュレイナー</th><th>15</th><th>5921</th><th>5921</th>",
            section,
        )
        self.assertNotIn("<tr><th>ロッド</th>", section)


if __name__ == "__main__":
    unittest.main()