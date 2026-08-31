import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATERIAL = ROOT / "docs" / "pages" / "material.html"


class MaterialCoreRarityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        html = MATERIAL.read_text(encoding="utf-8")
        start = html.index("<summary>コア</summary>")
        cls.core = html[start:html.index("</details>", start)]

    def test_core_rarities_keep_reference_star_notation(self):
        sentinels = {
            "スモール・コア": "★1",
            "ダーカー・コア": "★2",
            "ギガンテス・コア": "★7",
            "アルテイオスの純コア": "★10",
            "Gプレディカーダの超コア": "★11",
            "Gプレディカーダの極コア": "★13",
            "ディートアスの超コア": "★14",
            "ディートアスの極コア": "★15",
        }
        for name, rarity in sentinels.items():
            with self.subTest(name=name):
                self.assertIn(f"<tr><td>{name}</td><td>{rarity}</td>", self.core)

    def test_all_core_rarities_are_visible_star_values(self):
        rarities = re.findall(r"<tr><td>.*?</td><td>(.*?)</td>", self.core)
        self.assertTrue(rarities)
        for rarity in rarities:
            with self.subTest(rarity=rarity):
                self.assertRegex(rarity, r"^★(?:[1-9]|1[0-5])$")

    def test_hidden_wiki_sort_padding_is_not_imported_as_rarity_data(self):
        broken_values = (
            "100", "200", "300", "500", "600", "700", "800", "900",
            "1000", "1100", "1300", "1400", "1500",
        )
        for value in broken_values:
            with self.subTest(value=value):
                self.assertNotIn(f"<td>{value}</td>", self.core)


if __name__ == "__main__":
    unittest.main()
