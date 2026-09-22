import unittest
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "pages" / "quest" / "emergency-call.html"
QUEST_INDEX = ROOT / "docs" / "pages" / "quest.html"
SITEMAP = ROOT / "docs" / "sitemap.xml"


class EmergencyCallPageTests(unittest.TestCase):
    @staticmethod
    def page_html() -> str:
        return PAGE.read_text(encoding="utf-8")

    @classmethod
    def page_soup(cls) -> BeautifulSoup:
        return BeautifulSoup(cls.page_html(), "html.parser")

    def test_keeps_all_public_variants(self):
        soup = self.page_soup()
        tables = soup.select("main#main .table-scroll > table")
        rows = [row for table in tables for row in table.select("tbody > tr")]

        self.assertEqual(len(tables), 6)
        self.assertEqual(len(rows), 408)

        quest_names = set()
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 2:
                quest_names.add(cells[0].get_text(" ", strip=True))

        self.assertEqual(len(quest_names), 115)

    def test_uses_public_difficulty_labels(self):
        text = self.page_soup().get_text(" ", strip=True)

        for label in (
            "ノーマル",
            "ハード",
            "ベリーハード",
            "スーパーハード",
            "エクストラハード",
        ):
            with self.subTest(label=label):
                self.assertIn(label, text)

    def test_explains_invalid_item_reward_without_internal_id(self):
        html = self.page_html()
        text = self.page_soup().get_text(" ", strip=True)

        self.assertIn("極：漆黒の鉄馬と光線獣", text)
        self.assertIn("ファラレイバンサー討伐", text)
        self.assertIn("アイテム付与なし", text)
        self.assertNotIn("7|7|0|0", html)
        self.assertNotIn("invalid_definition", html)

    def test_is_linked_from_quest_index_and_sitemap(self):
        quest_index = QUEST_INDEX.read_text(encoding="utf-8")
        sitemap = SITEMAP.read_text(encoding="utf-8")

        path = "/PSNOVA/pages/quest/emergency-call.html"

        self.assertIn(f'href="{path}"', quest_index)
        self.assertIn(">エマージェンシーコール</span>", quest_index)
        self.assertIn(f"https://kylekatann.github.io{path}", sitemap)


if __name__ == "__main__":
    unittest.main()
