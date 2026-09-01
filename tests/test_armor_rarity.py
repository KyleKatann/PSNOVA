import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARMOR = ROOT / "docs" / "pages" / "armor.html"


class ArmorRarityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        html = ARMOR.read_text(encoding="utf-8")
        start = html.index("<h3>シールドユニット</h3>")
        end = html.index("</table>", start)
        cls.table = html[start:end]

    def test_rarities_keep_reference_star_notation(self):
        sentinels = {
            "ポストアタック": "★1",
            "フラットブロウ": "★2",
            "マキシブロウト": "★7",
            "ヘプタブロウブ": "★9",
            "オクタブロウブ": "★10",
            "クラッシュテクオル": "★13",
            "ゴウルフィオル": "★14",
            "ノヴァクオル": "★15",
        }
        for name, rarity in sentinels.items():
            with self.subTest(name=name):
                self.assertIn(f"<tr><td>{name}</td><td>{rarity}</td>", self.table)

    def test_all_armor_rarities_are_visible_star_values(self):
        rows = re.findall(r"<tr><td>(.*?)</td><td>(.*?)</td>", self.table)
        self.assertTrue(rows)
        for name, rarity in rows:
            if name == "名前":
                continue
            with self.subTest(name=name, rarity=rarity):
                self.assertRegex(rarity, r"^★(?:[1-9]|1[0-5])$")

    def test_hidden_zero_sort_padding_is_not_imported(self):
        for value in ("01", "02", "03", "04", "05", "06", "07", "08", "09"):
            with self.subTest(value=value):
                self.assertNotRegex(self.table, rf"<tr><td>[^<]+</td><td>{value}</td>")


if __name__ == "__main__":
    unittest.main()
