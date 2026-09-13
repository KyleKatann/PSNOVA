import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATERIAL = ROOT / "docs" / "pages" / "material.html"


class MaterialPageIntroTests(unittest.TestCase):
    def test_material_page_has_reader_facing_intro_before_data_sections(self):
        html = MATERIAL.read_text(encoding="utf-8")

        match = re.search(
            r"<h1>素材</h1>\s*"
            r'<p class="page-lead">(.+?)</p>\s*'
            r"<h2>材料</h2>",
            html,
            re.S,
        )
        self.assertIsNotNone(match)

        lead = match.group(1)
        self.assertEqual(3, lead.count("。"))
        self.assertIn("入手", lead)
        self.assertIn("種類別", lead)


if __name__ == "__main__":
    unittest.main()
