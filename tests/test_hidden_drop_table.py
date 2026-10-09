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

    def test_table_is_all_item_centric_three_column_structure(self):
        for heading in ("アイテム", "入手元", "クエスト"):
            self.assertIn(f'<th scope="col">{heading}</th>', self.html)

        for retired_heading in (
            "ギガンテス",
            "敵Lv",
            "敵Lv / 基礎率",
            "レア枠",
            "通常枠1",
            "通常枠2",
            "通常枠3",
            "通常枠4",
            "部位",
        ):
            self.assertNotIn(f'<th scope="col">{retired_heading}</th>', self.html)

        item_cells = re.findall(r'<td rowspan="\d+">([^<]+)</td>', self.html)
        self.assertEqual(len(item_cells), 820)
        self.assertEqual(len(set(item_cells)), 820)
        self.assertIn("収録アイテム：820種類", self.html)

    def test_enemy_source_rows_have_quests_and_plain_enemy_names(self):
        self.assertNotIn("モンスタードロップ", self.html)

        rows = re.findall(
            r'<tr class="enemy-source">(.*?)</tr>',
            self.html,
            re.S,
        )
        self.assertGreater(len(rows), 0)

        for row in rows:
            cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
            # First source row for an item has the rowspan item cell; subsequent rows do not.
            self.assertIn(len(cells), (2, 3))
            source = re.sub(r"<[^>]+>", "", cells[-2]).strip()
            quest = re.sub(r"<br\s*/?>", "\n", cells[-1])
            quest = re.sub(r"<[^>]+>", "", quest).strip()
            self.assertTrue(source)
            self.assertTrue(quest)
            self.assertNotEqual(quest, "—")

    def test_quest_column_is_three_column_left_aligned_and_compact(self):
        self.assertIn('<table id="drop-table">', self.html)
        self.assertIn(
            '#drop-table tbody tr.enemy-source td:last-child {',
            self.html,
        )
        for css in (
            'column-count: 3;',
            'text-align: left;',
            'line-height: 1.25;',
            'padding-top: 0.3rem;',
            'padding-bottom: 0.3rem;',
        ):
            self.assertIn(css, self.html)
        self.assertIn(
            '<colgroup><col style="width:24%"><col style="width:22%"><col style="width:54%"></colgroup>',
            self.html,
        )

    def test_burst_part_internal_and_javascript_markers_are_absent(self):
        for marker in (
            "gran_burst",
            "BurstProbability",
            "armor_",
            "antenna_",
            "weak_",
            "phalanx_",
            "mana_device",
            "damage_",
            "敵Lv / 基礎率",
        ):
            self.assertNotIn(marker, self.html)
        self.assertNotIn("<script", self.html.lower())
        self.assertNotIn('rel="canonical"', self.html)


if __name__ == "__main__":
    unittest.main()
