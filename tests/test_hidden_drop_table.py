from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "pages" / "drop-table-4f6e9a2c.html"


class HiddenDropTableTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")

    def test_page_is_unlisted_and_noindex(self):
        self.assertIn(
            '<meta name="robots" content="noindex,nofollow,noarchive">',
            self.html,
        )
        self.assertNotIn(
            "drop-table-4f6e9a2c",
            (ROOT / "docs" / "index.html").read_text(encoding="utf-8"),
        )
        self.assertNotIn(
            "drop-table-4f6e9a2c",
            (ROOT / "docs" / "sitemap.xml").read_text(encoding="utf-8"),
        )

    def test_table_has_gigantes_only_without_part_column(self):
        for heading in (
            "ギガンテス",
            "敵Lv",
            "レア枠",
            "通常枠1",
            "通常枠2",
            "通常枠3",
            "通常枠4",
        ):
            self.assertIn(f'<th scope="col">{heading}</th>', self.html)
        self.assertNotIn('<th scope="col">部位</th>', self.html)
        for internal_name in (
            "armor_",
            "antenna_",
            "weak_",
            "phalanx_",
            "mana_device",
            "damage_",
        ):
            self.assertNotIn(internal_name, self.html)

    def test_gran_burst_rows_and_runtime_javascript_are_absent(self):
        for marker in ("グランバースト", "gran_burst", "BurstProbability"):
            self.assertNotIn(marker, self.html)
        self.assertNotIn("<script", self.html.lower())


if __name__ == "__main__":
    unittest.main()
