from collections import Counter
from pathlib import Path
import re
import unittest
ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs/pages/drop-table-4f6e9a2c.html"
DATA = ROOT / "docs/pages/drop-table-data"
class HiddenDropTableTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.groups = re.findall(r'<tr class="[^"]+" data-source="([^"]+)" data-row-ids="([0-9,]+)">', cls.html)
    def test_original_four_column_format(self):
        self.assertIn('<table id="drop-table">', self.html)
        self.assertIn('<th scope="col">エネミー</th>', self.html)
        self.assertIn('<th scope="col">出現候補クエスト・地域 / 入手先</th>', self.html)
        self.assertEqual(self.html.count('class="item-name"'), 822)
        names = re.findall(r'class="item-name">([^<]+)</td>', self.html)
        self.assertEqual(names[:2], ['モノメイト', 'ディメイト'])
        self.assertIn('822種類。元DB取得定義：80,492件', self.html)
        self.assertNotIn('<iframe', self.html)
    def test_complete_rows(self):
        ids = [int(s) for _, group in self.groups for s in group.split(',')]
        self.assertEqual(len(ids), 79604)
        self.assertEqual(len(set(ids)), 79604)
        self.assertTrue(all(0 <= n < 80492 for n in ids))
        self.assertEqual(80492 - len(ids), 888)
    def test_source_counts(self):
        counts = Counter()
        for source, group in self.groups:
            counts[source] += group.count(',') + 1
        self.assertEqual(counts, Counter({'enemy': 66078, 'field_gimmick': 6164, 'quest_reward': 1174, 'emergency_reward': 1847, 'promise_reward': 183, 'native_refill': 2, 'coldsleep_series_reward': 19, 'event_grant': 4, 'search_corps_reward': 321, 'region': 304, 'common': 3508}))
    def test_bare_region_locations_are_labeled_as_non_quest_candidates(self):
        regions = {"鋼の荒野", "グラン水源", "炎の高地", "古代都市", "大尖塔", "ノヴァ内部"}
        enemy_rows = re.findall(r'<tr class="enemy-source"[^>]*>[\s\S]*?</tr>', self.html)
        self.assertGreater(len(enemy_rows), 0)
        region_tokens = 0
        for row in enemy_rows:
            detail = re.search(r'<td class="detail-cell(?: detail-multi)?">([\s\S]*?)</td>', row)
            self.assertIsNotNone(detail)
            tokens = detail.group(1).split("<br>")
            self.assertFalse(regions.intersection(tokens), "地域名を単独のクエストとして表示している")
            region_tokens += sum(token.startswith("地域：") and token.endswith("（クエスト未特定）")
                                 for token in tokens)
        self.assertGreater(region_tokens, 0)
        self.assertIn('地域：鋼の荒野（クエスト未特定）', self.html)
    def test_no_old_data_fallback(self):
        self.assertFalse(DATA.exists())
        self.assertNotIn('drop-table-data/', self.html)
        self.assertIn('noindex,nofollow,noarchive', self.html)
        self.assertNotIn('drop-table-4f6e9a2c', (ROOT/'docs/sitemap.xml').read_text(encoding='utf-8'))
if __name__ == '__main__':
    unittest.main()
