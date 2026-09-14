import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATERIAL = ROOT / "docs" / "pages" / "material.html"


class MaterialSourceSemanticsTests(unittest.TestCase):
    def test_material_tables_are_semantic_in_source_html(self):
        html = MATERIAL.read_text(encoding="utf-8")
        self.assertNotIn("bgcolor=", html.lower())
        self.assertNotRegex(html, r"<table[^>]+(?:border|style)=")

        tables = re.findall(r"<table>(.*?)</table>", html, flags=re.I | re.S)
        self.assertGreater(len(tables), 0)
        for table in tables:
            self.assertIn("<thead>", table.lower())
            self.assertIn("<tbody>", table.lower())
            body_match = re.search(r"<tbody>(.*?)</tbody>", table, flags=re.I | re.S)
            self.assertIsNotNone(body_match)
            self.assertNotIn("<th", body_match.group(1).lower())

    def test_material_sections_are_always_visible_without_collapsible_markup(self):
        html = MATERIAL.read_text(encoding="utf-8")
        lower = html.lower()
        self.assertNotIn("<details", lower)
        self.assertNotIn("<summary", lower)

        for heading in (
            "食材",
            "鉱石・資材",
            "原生種素材",
            "ダーカー素材",
            "ギガンテス素材",
            "メモリーフラグメント・グランピース・チケット・その他",
            "コア",
        ):
            self.assertIn(f"<h3>{heading}</h3>", html)


if __name__ == "__main__":
    unittest.main()
