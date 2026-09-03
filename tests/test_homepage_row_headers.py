import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "index.html"


class HomepageRowHeaderTests(unittest.TestCase):
    def test_homepage_descriptive_tables_use_row_headers(self):
        html = INDEX.read_text(encoding="utf-8")

        expected = (
            "商品名",
            "対応機種",
            "発売日",
            "価格",
            "ジャンル",
            "プレイ人数",
            "発売・販売",
            "CERO表記",
            "PSNOVA 公式サイト",
            "PSO2 公式サイト",
        )

        for label in expected:
            with self.subTest(label=label):
                self.assertIn(
                    f'<th scope="row">{label}</th>',
                    html,
                )

    def test_homepage_has_no_unscoped_th_cells(self):
        html = INDEX.read_text(encoding="utf-8")

        unscoped = re.findall(
            r"<th(?![^>]*\bscope=)[^>]*>",
            html,
            re.IGNORECASE,
        )

        self.assertEqual([], unscoped)

    def test_homepage_row_header_count_is_stable(self):
        html = INDEX.read_text(encoding="utf-8")

        row_headers = re.findall(
            r'<th\b[^>]*\bscope=["\']row["\']',
            html,
            re.IGNORECASE,
        )

        self.assertEqual(10, len(row_headers))


if __name__ == "__main__":
    unittest.main()
