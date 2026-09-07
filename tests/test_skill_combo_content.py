import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_PAGE = ROOT / "docs" / "pages" / "skill.html"


class SkillComboContentTests(unittest.TestCase):
    def test_combo_skill_sections_keep_all_migrated_tables(self):
        html = SKILL_PAGE.read_text(encoding="utf-8")
        start = html.index('<h3 id="combo-skills">')
        section = html[start : html.index("</section>", start)]

        self.assertIn('<h3 id="combo-skills-many">組み合わせの多いコンボスキル</h3>', section)
        self.assertEqual(section.count("<table>"), 46)
        self.assertEqual(section.count('<div class="table-scroll">'), 46)

        for text in (
            "HPアップⅢ",
            "ガードGP変換",
            "スーパーアーマー",
            "HPアップⅤ",
            "ウォンドリアクター",
            "射撃力・法撃力の40%をウォンドの打撃力に加算する。",
        ):
            self.assertIn(text, section)

        for forbidden in (
            "web.archive.org",
            "paraedit.png",
            "mini_add.png",
            "攻略Wiki",
        ):
            self.assertNotIn(forbidden, section)

    def test_combo_skill_internal_list_links_have_targets(self):
        html = SKILL_PAGE.read_text(encoding="utf-8")
        start = html.index('<h3 id="combo-skills">')
        section = html[start : html.index("</section>", start)]

        targets = set(re.findall(r'\sid="([A-Za-z0-9_-]+)"', section))
        links = set(re.findall(r'href="#([A-Za-z0-9_-]+)"', section))
        self.assertTrue(links)
        self.assertFalse(links - targets, f"missing combo-skill link targets: {sorted(links - targets)}")


if __name__ == "__main__":
    unittest.main()
