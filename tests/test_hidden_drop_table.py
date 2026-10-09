from pathlib import Path
import re
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

    def test_table_is_item_centric(self):
        for heading in ("アイテム", "入手元", "クエスト", "敵Lv / 基礎率"):
            self.assertIn(f'<th scope="col">{heading}</th>', self.html)

        for retired_heading in (
            "ギガンテス",
            "敵Lv",
            "レア枠",
            "通常枠1",
            "通常枠2",
            "通常枠3",
            "通常枠4",
            "部位",
        ):
            self.assertNotIn(f'<th scope="col">{retired_heading}</th>', self.html)

    def test_monster_drop_rows_have_quest_names(self):
        tbody = re.search(r"<tbody>(.*?)</tbody>", self.html, re.S)
        self.assertIsNotNone(tbody)
        rows = re.findall(r"<tr>(.*?)</tr>", tbody.group(1), re.S)
        self.assertGreater(len(rows), 300)

        checked = 0
        for row in rows:
            cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
            self.assertEqual(len(cells), 4)
            source = re.sub(r"<[^>]+>", "", cells[1]).strip()
            quest = re.sub(r"<br\s*/?>", "\n", cells[2])
            quest = re.sub(r"<[^>]+>", "", quest).strip()
            if "モンスタードロップ" in source:
                checked += 1
                self.assertTrue(quest)
                self.assertNotEqual(quest, "—")
        self.assertEqual(checked, len(rows))

    def test_gran_burst_and_internal_parts_are_absent(self):
        for marker in (
            "gran_burst",
            "BurstProbability",
            "armor_",
            "antenna_",
            "weak_",
            "phalanx_",
            "mana_device",
            "damage_",
        ):
            self.assertNotIn(marker, self.html)
        self.assertNotIn("<script", self.html.lower())


if __name__ == "__main__":
    unittest.main()
