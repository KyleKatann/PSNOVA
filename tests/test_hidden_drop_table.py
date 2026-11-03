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
        self.assertIn('<th scope="col">出現候補クエスト / 入手先</th>', self.html)
        self.assertEqual(self.html.count('class="item-name"'), 822)
        names = re.findall(r'class="item-name">([^<]+)</td>', self.html)
        self.assertEqual(names[:2], ['モノメイト', 'ディメイト'])
        self.assertIn('822種類。取得定義：80,492件', self.html)
        self.assertNotIn('<iframe', self.html)
    def test_complete_rows(self):
        ids = [int(s) for _, group in self.groups for s in group.split(',')]
        self.assertEqual(len(ids), 80492)
        self.assertEqual(len(set(ids)), 80492)
        self.assertEqual((min(ids), max(ids)), (0, 80491))
    def test_source_counts(self):
        counts = Counter()
        for source, group in self.groups:
            counts[source] += group.count(',') + 1
        self.assertEqual(counts, Counter({'emergency_reward': 1847, 'enemy': 66873, 'field_gimmick': 6164, 'native_refill': 2, 'promise_reward': 183, 'quest_reward': 1174, 'coldsleep_series_reward': 19, 'event_grant': 4, 'search_corps_reward': 321, 'region': 304, 'common': 3601}))
    def test_no_old_data_fallback(self):
        self.assertFalse(DATA.exists())
        self.assertNotIn('drop-table-data/', self.html)
        self.assertIn('noindex,nofollow,noarchive', self.html)
        self.assertNotIn('drop-table-4f6e9a2c', (ROOT/'docs/sitemap.xml').read_text(encoding='utf-8'))
if __name__ == '__main__':
    unittest.main()
