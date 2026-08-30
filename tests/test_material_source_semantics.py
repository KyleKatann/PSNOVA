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


if __name__ == "__main__":
    unittest.main()
