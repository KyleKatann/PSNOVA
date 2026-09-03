import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATERIAL = ROOT / "docs" / "pages" / "material.html"


class MaterialPageIntroTests(unittest.TestCase):
    def test_material_page_has_reader_facing_intro_before_data_sections(self):
        html = MATERIAL.read_text(encoding="utf-8")

        match = re.search(
            r"<h2>素材</h2>\s*"
            r'<p class="page-lead">(.+?)</p>\s*'
            r"<h3>材料</h3>",
            html,
            re.S,
        )
        self.assertIsNotNone(match)

        lead = match.group(1)
        self.assertEqual(3, lead.count("。"))
        self.assertIn("入手", lead)
        self.assertIn("一覧", lead)


if __name__ == "__main__":
    unittest.main()
