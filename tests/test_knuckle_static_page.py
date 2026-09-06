from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
KNUCKLE = ROOT / "docs" / "pages" / "weapon" / "knuckle.html"


class KnuckleStaticPageTests(unittest.TestCase):
    def test_knuckle_page_is_static_and_single_weapon(self):
        html = KNUCKLE.read_text(encoding="utf-8")

        self.assertIn(
            'data-weapon-static="true"',
            html,
        )
        self.assertIn(
            'data-weapon-type="ナックル"',
            html,
        )

        self.assertNotIn("<details", html)
        self.assertNotIn("<summary", html)

    def test_knuckle_table_uses_static_semantics_and_reader_labels(self):
        html = KNUCKLE.read_text(encoding="utf-8")

        self.assertIn("<thead>", html)
        self.assertIn("<tbody>", html)
        self.assertIn(
            '<th scope="col">ショップレベル</th>',
            html,
        )

        self.assertNotIn("ショップLv", html)
        self.assertNotIn("bgcolor=", html)
        self.assertNotIn('border="1"', html)
        self.assertNotIn("border-collapse", html)

    def test_knuckle_data_sentinels_and_row_count_are_preserved(self):
        html = KNUCKLE.read_text(encoding="utf-8")

        tbody = re.search(
            r"<tbody>(.*?)</tbody>",
            html,
            re.S,
        )

        self.assertIsNotNone(tbody)

        rows = re.findall(
            r"<tr>",
            tbody.group(1),
        )

        self.assertEqual(29, len(rows))

        self.assertIn("<td>ナックル</td>", html)
        self.assertIn("<td>エイトオンス</td>", html)
        self.assertIn("<td>ノヴァクローグ</td>", html)
        self.assertIn("<td>ファイバーロア</td>", html)

    def test_static_page_keeps_one_icon_and_catalog_navigation(self):
        html = KNUCKLE.read_text(encoding="utf-8")

        self.assertEqual(
            1,
            html.count(
                "/PSNOVA/img/weapon/knuckle.png"
            ),
        )

        self.assertIn(
            '<a class="weapon-page-nav-index" href="/PSNOVA/pages/weapon.html">武器一覧</a>',
            html,
        )
        self.assertNotIn('rel="prev"', html)
        self.assertNotIn('rel="next"', html)


if __name__ == "__main__":
    unittest.main()
