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

    def test_table_is_all_item_centric_split_source_structure(self):
        self.assertIn('<th scope="col" rowspan="2">アイテム</th>', self.html)
        self.assertIn('<th scope="colgroup" colspan="2">入手元</th>', self.html)
        self.assertIn('<th scope="col" rowspan="2">クエスト / 入手先</th>', self.html)
        self.assertIn('<th scope="col">種別</th>', self.html)
        self.assertIn('<th scope="col">名称</th>', self.html)

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

    def test_enemy_sources_are_split_into_kind_and_enemy_name(self):
        self.assertNotIn("モンスタードロップ", self.html)

        rows = re.findall(
            r'<tr class="enemy-source">(.*?)</tr>',
            self.html,
            re.S,
        )
        self.assertGreater(len(rows), 0)

        kind_cells = re.findall(
            r'<td rowspan="(\d+)" class="source-kind">([^<]+)</td>',
            self.html,
        )
        self.assertGreater(len(kind_cells), 0)
        for rowspan, label in kind_cells:
            self.assertGreater(int(rowspan), 0)
            self.assertEqual(label, "エネミードロップ")

        for row in rows:
            cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
            self.assertIn(len(cells), (2, 4))
            enemy = re.sub(r"<[^>]+>", "", cells[-2]).strip()
            detail = re.sub(r"<br\s*/?>", "\n", cells[-1])
            detail = re.sub(r"<[^>]+>", "", detail).strip()
            self.assertTrue(enemy)
            self.assertNotEqual(enemy, "エネミードロップ")
            self.assertTrue(detail)
            self.assertNotEqual(detail, "—")

    def test_non_enemy_sources_span_both_source_columns(self):
        rows = re.findall(r'<tr(?: class="([^"]+)")?>(.*?)</tr>', self.html, re.S)
        checked = 0
        for cls, row in rows:
            if cls == "enemy-source":
                continue
            cells = re.findall(r"<td([^>]*)>(.*?)</td>", row, re.S)
            if not cells:
                continue
            source_cell = cells[-2]
            self.assertIn('colspan="2"', source_cell[0])
            source = re.sub(r"<[^>]+>", "", source_cell[1]).strip()
            self.assertTrue(source)
            checked += 1
        self.assertGreater(checked, 0)

    def test_field_drops_are_aggregated_into_detail_column(self):
        rows = re.findall(r'<tr(?: class="([^"]+)")?>(.*?)</tr>', self.html, re.S)
        field_rows = 0
        for cls, row in rows:
            cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
            if not cells:
                continue
            source = re.sub(r"<[^>]+>", "", cells[-2]).strip()
            detail = re.sub(r"<br\s*/?>", "\n", cells[-1])
            detail = re.sub(r"<[^>]+>", "", detail).strip()
            if cls == "field-source":
                field_rows += 1
                self.assertEqual(source, "フィールドドロップ")
                self.assertTrue(detail)
                self.assertNotEqual(detail, "—")
            self.assertFalse(source.endswith(" フィールド"))
        self.assertGreater(field_rows, 0)

    def test_acquisition_types_are_grouped_in_fixed_order_per_item(self):
        rows = re.findall(r'<tr(?: class="([^"]+)")?>(.*?)</tr>', self.html, re.S)

        def rank(cls, source):
            if cls == "enemy-source":
                return 0
            if cls == "field-source":
                return 1
            if source.endswith(" エリアドロップ"):
                return 2
            if source == "共通ドロップ":
                return 3
            if cls == "quest-reward-source" or source == "クエスト報酬":
                return 4
            if source == "エマージェンシー報酬":
                return 5
            if source == "プロミスオーダー報酬":
                return 6
            if source == "探索隊報酬":
                return 7
            if source == "イベント入手":
                return 8
            return 9

        current = []
        groups = 0
        for cls, row in rows:
            cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
            if not cells:
                continue
            if re.search(r'<td rowspan="\d+">', row):
                if current:
                    self.assertEqual(current, sorted(current))
                current = []
                groups += 1
            source = (
                "エネミードロップ"
                if cls == "enemy-source"
                else re.sub(r"<[^>]+>", "", cells[-2]).strip()
            )
            current.append(rank(cls, source))
        if current:
            self.assertEqual(current, sorted(current))
        self.assertEqual(groups, 820)

    def test_quest_rewards_are_aggregated_into_detail_column(self):
        rows = re.findall(r'<tr(?: class="([^"]+)")?>(.*?)</tr>', self.html, re.S)
        reward_rows = 0
        for cls, row in rows:
            cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
            if not cells:
                continue
            source = re.sub(r"<[^>]+>", "", cells[-2]).strip()
            detail = re.sub(r"<br\s*/?>", "\n", cells[-1])
            detail = re.sub(r"<[^>]+>", "", detail).strip()
            if cls == "quest-reward-source":
                reward_rows += 1
                self.assertEqual(source, "クエスト報酬")
                self.assertTrue(detail)
                self.assertNotEqual(detail, "—")
            if (
                source.endswith(" 報酬")
                and source not in (
                    "エマージェンシー報酬",
                    "プロミスオーダー報酬",
                    "探索隊報酬",
                    "クエスト報酬",
                )
            ):
                self.fail(f"unaggregated quest reward source: {source}")
        self.assertGreater(reward_rows, 0)

    def test_detail_column_is_three_column_left_aligned_and_compact(self):
        self.assertIn('<table id="drop-table">', self.html)
        self.assertIn(
            '#drop-table tbody td:last-child {',
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
            '<colgroup><col style="width:22%"><col style="width:13%"><col style="width:18%"><col style="width:47%"></colgroup>',
            self.html,
        )
        self.assertIn(
            '#drop-table tbody td.source-kind {',
            self.html,
        )

    def test_all_displayed_acquisition_rows_have_detail(self):
        rows = re.findall(r'<tr(?: class="([^"]+)")?>(.*?)</tr>', self.html, re.S)
        checked = 0
        for _cls, row in rows:
            cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
            if not cells:
                continue
            detail = re.sub(r"<br\s*/?>", "\n", cells[-1])
            detail = re.sub(r"<[^>]+>", "", detail).strip()
            self.assertTrue(detail)
            self.assertNotEqual(detail, "—")
            checked += 1
        self.assertGreater(checked, 0)
        self.assertNotIn("<td>—</td>", self.html)

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
