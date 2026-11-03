import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs/pages/drop-table-4f6e9a2c.html"
TBODY = re.compile(r"<tbody>([\s\S]*?)</tbody>")
TR = re.compile(r"<tr\b[^>]*>[\s\S]*?</tr>")
ITEM = re.compile(r'<td rowspan="(\d+)" class="item-name">([^<]+)</td>')

class HiddenDropTableTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        m = TBODY.search(cls.html)
        if not m:
            raise AssertionError("tbody欠落")
        cls.rows = TR.findall(m[1])

    def test_structure(self):
        self.assertIn('<table id="drop-table">', self.html)
        for title in ("アイテム", "入手元", "エネミー", "出現候補クエスト / 入手先"):
            self.assertIn('<th scope="col">' + title + '</th>', self.html)
        self.assertIn("正本DB：822種類・取得定義80,492件", self.html)
        self.assertNotIn("<iframe", self.html)

    def test_rowspan_and_references(self):
        spans = []
        for row in self.rows:
            item = ITEM.search(row)
            if item:
                spans.append([int(item[1]), 0, item[2]])
            self.assertTrue(spans)
            spans[-1][1] += 1
            for ids in re.findall(r'data-row-ids="([0-9,]+)"', row):
                refs = [int(x) for x in ids.split(",")]
                self.assertEqual(len(refs), len(set(refs)))
                self.assertTrue(all(0 <= x < 80492 for x in refs))
        self.assertTrue(all(expected == actual for expected, actual, _ in spans))
        self.assertEqual(len(spans), self.html.count('class="item-name"'))

    def test_monsters_are_only_quest_attributed(self):
        self.assertNotIn("地域フォールバック", self.html)
        self.assertNotIn("共通フォールバック", self.html)
        self.assertNotIn("地域：鋼の荒野（クエスト未特定）", self.html)
        self.assertNotIn('data-source="region"', self.html)
        self.assertNotIn('data-source="common"', self.html)
        n = 0
        for row in self.rows:
            if 'data-source="enemy"' in row:
                n += 1
                self.assertRegex(row, r'<td class="enemy-name">[^<]+</td>')
                self.assertRegex(row, r'<td class="detail-cell detail-multi">[^<]+(?:<br>[^<]+)*</td>')
        self.assertGreater(n, 0)

    def test_no_old_fallback_data(self):
        self.assertFalse((ROOT / "docs/pages/drop-table-data").exists())
        self.assertNotIn("drop-table-data/", self.html)
        self.assertIn("noindex,nofollow,noarchive", self.html)
        self.assertNotIn("drop-table-4f6e9a2c", (ROOT / "docs/sitemap.xml").read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
