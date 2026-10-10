from collections import Counter
from html import unescape
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "pages" / "drop-table-4f6e9a2c.html"


def clean_text(value):
    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.I)
    value = re.sub(r"<[^>]+>", "", value)
    return unescape(value).strip()


class HiddenDropTableTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        body_match = re.search(r"<tbody>([\s\S]*?)</tbody>", cls.html)
        if not body_match:
            raise AssertionError("drop table tbody not found")
        cls.body = body_match.group(1)
        cls.rows = []
        current_item = None
        for match in re.finditer(
            r'<tr(?: class="([^"]+)")?>([\s\S]*?)</tr>',
            cls.body,
        ):
            row_class = match.group(1) or ""
            cells = [
                {
                    "attrs": cell.group(1),
                    "html": cell.group(2),
                    "text": clean_text(cell.group(2)),
                }
                for cell in re.finditer(
                    r"<td([^>]*)>([\s\S]*?)</td>",
                    match.group(2),
                )
            ]
            if not cells:
                continue

            starts_item = 'class="item-name"' in cells[0]["attrs"]
            if starts_item:
                current_item = cells[0]["text"]

            if row_class == "enemy-source":
                source = "エネミードロップ"
                enemy = cells[-2]["text"]
            else:
                source = cells[-2]["text"]
                enemy = None

            detail_html = cells[-1]["html"]
            detail_entries = [
                clean_text(entry)
                for entry in re.split(r"<br\s*/?>", detail_html, flags=re.I)
                if clean_text(entry)
            ]
            cls.rows.append(
                {
                    "item": current_item,
                    "starts_item": starts_item,
                    "class": row_class,
                    "cells": cells,
                    "source": source,
                    "enemy": enemy,
                    "detail_entries": detail_entries,
                }
            )

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

    def test_table_has_single_level_enemy_specific_source_columns(self):
        expected_header = (
            '<thead><tr><th scope="col">アイテム</th>'
            '<th scope="col">入手元</th>'
            '<th scope="col">エネミー</th>'
            '<th scope="col">出現候補クエスト / 入手先</th></tr></thead>'
        )
        self.assertIn(expected_header, self.html)
        self.assertNotIn('<th scope="colgroup" colspan="2">入手元</th>', self.html)
        self.assertNotIn('<th scope="col">種別</th>', self.html)
        self.assertNotIn('<th scope="col">名称</th>', self.html)

        item_cells = re.findall(
            r'<td rowspan="\d+" class="item-name">([^<]+)</td>',
            self.html,
        )
        self.assertEqual(len(item_cells), 820)
        self.assertEqual(len(set(item_cells)), 820)
        self.assertIn("収録アイテム：820種類", self.html)

    def test_enemy_rows_are_split_and_quest_wording_is_candidate_level(self):
        enemy_rows = [row for row in self.rows if row["class"] == "enemy-source"]
        self.assertGreater(len(enemy_rows), 0)
        self.assertIn("出現候補クエスト", self.html)
        self.assertNotIn("対応クエスト", self.html)

        kind_cells = re.findall(
            r'<td rowspan="(\d+)" class="source-kind">([^<]+)</td>',
            self.body,
        )
        self.assertGreater(len(kind_cells), 0)
        for rowspan, label in kind_cells:
            self.assertGreater(int(rowspan), 0)
            self.assertEqual(label, "エネミードロップ")

        for row in enemy_rows:
            enemy_cells = [
                cell for cell in row["cells"]
                if 'class="enemy-name"' in cell["attrs"]
            ]
            self.assertEqual(len(enemy_cells), 1)
            self.assertTrue(row["enemy"])
            self.assertNotEqual(row["enemy"], "エネミードロップ")
            self.assertTrue(row["detail_entries"])

    def test_non_enemy_sources_span_source_and_enemy_columns(self):
        checked = 0
        for row in self.rows:
            if row["class"] == "enemy-source":
                continue
            source_cells = [
                cell for cell in row["cells"]
                if 'class="source-wide"' in cell["attrs"]
            ]
            self.assertEqual(len(source_cells), 1)
            self.assertIn('colspan="2"', source_cells[0]["attrs"])
            self.assertTrue(source_cells[0]["text"])
            checked += 1
        self.assertGreater(checked, 0)

    def test_unresolved_routes_are_counted_after_source_name_recovery(self):
        counts = Counter()
        total = 0
        for row in self.rows:
            for entry in row["detail_entries"]:
                if entry.endswith("入手先詳細未特定"):
                    counts[row["source"]] += 1
                    total += 1

        self.assertEqual(total, 30)
        self.assertEqual(
            counts,
            Counter(
                {
                    "地域フォールバック": 15,
                    "エマージェンシー報酬": 10,
                    "プロミスオーダー報酬": 2,
                    "探索隊報酬": 3,
                }
            ),
        )
        self.assertNotIn("<td>—</td>", self.body)
        for row in self.rows:
            self.assertNotIn("—", row["detail_entries"])

    def test_identified_source_rows_display_concrete_game_names(self):
        # 報酬DB・公開プロミスオーダーに照合済みの18件を具体名で固定する。
        expected = [
            ("モノメイト", "プロミスオーダー報酬", "アイテムショップ建設"),
            ("ディメイト", "プロミスオーダー報酬", "アイテムショップ改築"),
            ("トリメイト", "プロミスオーダー報酬", "ブーストエネミー撃破訓練"),
            ("スケープドール", "プロミスオーダー報酬", "瀕死の克服"),
            ("メモリーフラグメントA", "プロミスオーダー報酬", "クラスカウンター建設"),
            ("メモリーフラグメントB", "プロミスオーダー報酬", "クラスカウンター改築"),
            ("メモリーフラグメントD", "プロミスオーダー報酬", "メモリーフラグメント変換4"),
            ("メモリーフラグメントE", "プロミスオーダー報酬", "メモリーフラグメント変換5"),
            ("メモリーフラグメントF", "プロミスオーダー報酬", "メモリーフラグメント変換6"),
            ("メモリーフラグメントG", "プロミスオーダー報酬", "メモリーフラグメント変換7"),
            ("メモリーフラグメントA", "探索隊報酬", "［採集］フラグメント採集（報酬1）"),
            ("メモリーフラグメントB", "探索隊報酬", "［採集］フラグメント採集（報酬2・報酬3）"),
            ("メモリーフラグメントD", "探索隊報酬", "［採集］地上フラグメント採集（報酬2）"),
            ("メモリーフラグメントE", "探索隊報酬", "［採集］地上フラグメント採集（報酬3）"),
            ("メモリーフラグメントF", "探索隊報酬", "［採集］惑星本体フラグメント採集（報酬1）"),
            ("メモリーフラグメントG", "探索隊報酬", "［採集］惑星本体フラグメント採集（報酬2）"),
            ("メモリーフラグメントB", "エマージェンシー報酬", "迫るアグリオスを止めろ"),
            ("メモリーフラグメントG", "エマージェンシー報酬", "ゴルドス討伐"),
        ]
        for item, source, source_name in expected:
            with self.subTest(item=item, source=source):
                matches = [
                    row for row in self.rows
                    if row["item"] == item and row["source"] == source
                ]
                self.assertEqual(len(matches), 1)
                self.assertTrue(
                    any(source_name in e for e in matches[0]["detail_entries"])
                )
                self.assertNotIn(
                    "入手先詳細未特定", matches[0]["cells"][-1]["text"]
                )

    def test_region_and_common_drop_labels_use_runtime_fallback_semantics(self):
        self.assertNotIn("エリアドロップ", self.body)
        self.assertNotIn("共通ドロップ", self.body)

        sources = {row["source"] for row in self.rows}
        self.assertIn("地域フォールバック", sources)
        self.assertIn("共通フォールバック", sources)

        allowed_areas = {
            "鋼の荒野",
            "グラン水源",
            "炎の高地",
            "古代都市",
            "大尖塔",
            "ノヴァ内部",
            "地域未特定",
        }
        region_entries = []
        for row in self.rows:
            if row["source"] != "地域フォールバック":
                continue
            region_entries.extend(row["detail_entries"])
            for entry in row["detail_entries"]:
                area, separator, detail = entry.partition("：")
                self.assertEqual(separator, "：")
                self.assertIn(area, allowed_areas)
                self.assertTrue(detail)

        self.assertGreater(len(region_entries), 0)
        self.assertIn("グラン水源：地の底へ", region_entries)
        self.assertNotIn("古代都市：地の底へ", region_entries)
        self.assertNotIn("大尖塔：地の底へ", region_entries)
        self.assertIn("古代都市：静かなる都市", region_entries)
        self.assertIn("大尖塔：天を衝く大尖塔", region_entries)

    def test_dummy_quests_are_excluded_and_event_name_is_not_invented(self):
        self.assertNotIn("ダミーデータ", self.body)
        self.assertNotIn("DLCイベント配布", self.body)
        self.assertEqual(
            self.body.count("DLCイベント付与（イベント名未特定）"),
            2,
        )

    def test_field_and_quest_rewards_remain_aggregated(self):
        field_rows = [row for row in self.rows if row["class"] == "field-source"]
        quest_reward_rows = [
            row for row in self.rows
            if row["class"] == "quest-reward-source"
        ]
        self.assertGreater(len(field_rows), 0)
        self.assertGreater(len(quest_reward_rows), 0)

        for row in field_rows:
            self.assertEqual(row["source"], "フィールドドロップ")
            self.assertTrue(row["detail_entries"])

        for row in quest_reward_rows:
            self.assertEqual(row["source"], "クエスト報酬")
            self.assertTrue(row["detail_entries"])

    def test_acquisition_types_are_grouped_in_fixed_order_per_item(self):
        def rank(row):
            if row["class"] == "enemy-source":
                return 0
            return {
                "フィールドドロップ": 1,
                "地域フォールバック": 2,
                "共通フォールバック": 3,
                "クエスト報酬": 4,
                "エマージェンシー報酬": 5,
                "プロミスオーダー報酬": 6,
                "探索隊報酬": 7,
                "イベント入手": 8,
            }.get(row["source"], 9)

        current = []
        groups = 0
        for row in self.rows:
            if row["starts_item"]:
                if current:
                    self.assertEqual(current, sorted(current))
                current = []
                groups += 1
            current.append(rank(row))
        if current:
            self.assertEqual(current, sorted(current))
        self.assertEqual(groups, 820)

    def test_detail_columns_are_adaptive_not_forced_for_short_rows(self):
        self.assertIn("#drop-table tbody td.detail-cell {", self.html)
        self.assertIn(
            "#drop-table tbody td.detail-cell.detail-multi {",
            self.html,
        )
        self.assertIn("column-count: 3;", self.html)
        self.assertNotIn("#drop-table tbody td:last-child {", self.html)

        short_rows = 0
        multi_rows = 0
        for row in self.rows:
            detail_cell = row["cells"][-1]
            classes = re.search(r'class="([^"]+)"', detail_cell["attrs"])
            class_names = set(classes.group(1).split()) if classes else set()
            count = len(row["detail_entries"])
            if count < 6:
                short_rows += 1
                self.assertNotIn("detail-multi", class_names)
            else:
                multi_rows += 1
                self.assertIn("detail-multi", class_names)

        self.assertGreater(short_rows, 0)
        self.assertGreater(multi_rows, 0)

    def test_all_displayed_rows_have_nonempty_detail(self):
        self.assertGreater(len(self.rows), 0)
        for row in self.rows:
            self.assertTrue(row["detail_entries"])
            for entry in row["detail_entries"]:
                self.assertTrue(entry.strip())
                self.assertNotEqual(entry, "—")

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
