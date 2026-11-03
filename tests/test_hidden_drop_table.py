from collections import Counter
from pathlib import Path
import re
import unittest
ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/"docs"/"pages"/"drop-table-4f6e9a2c.html"
PARTS=ROOT/"docs"/"pages"/"drop-table-data"
class HiddenDropTableTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index=PAGE.read_text(encoding="utf-8")
        cls.parts=sorted(PARTS.glob("[0-9][0-9].html"))
        cls.body=[p.read_text(encoding="utf-8") for p in cls.parts]
    def test_hidden_page(self):
        self.assertIn("noindex,nofollow,noarchive",self.index)
        self.assertNotIn("drop-table-4f6e9a2c",(ROOT/"docs"/"sitemap.xml").read_text(encoding="utf-8"))
        self.assertIn("822種類・80,492件",self.index)
        self.assertNotIn("<script",self.index.lower())
    def test_all_rows(self):
        self.assertGreater(len(self.parts),1)
        ids=[int(n) for p in self.body for n in re.findall(r'data-row-id="(\d+)"',p)]
        self.assertEqual(len(ids),80492)
        self.assertEqual(len(set(ids)),80492)
        self.assertEqual((min(ids),max(ids)),(0,80491))
        self.assertEqual(sum(p.count('<details class="item"') for p in self.body),822)
    def test_sources(self):
        got=Counter(n for p in self.body for n in re.findall(r'data-source="([^"]+)"',p))
        expected=Counter({'enemy': 66873, 'search_corps_reward': 321, 'region': 304, 'promise_reward': 183, 'field_gimmick': 6164, 'quest_reward': 1174, 'emergency_reward': 1847, 'coldsleep_series_reward': 19, 'common': 3601, 'native_refill': 2, 'event_grant': 4})
        self.assertEqual(got,expected)
    def test_index_links(self):
        links=re.findall(r'href="(drop-table-data/\d\d.html#item-\d+)"',self.index)
        self.assertEqual(len(links),822)
        for link in links:
            file,anchor=link.split("#")
            self.assertTrue((ROOT/"docs"/"pages"/file).exists())
if __name__=="__main__":unittest.main()
