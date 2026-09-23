import unittest
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "pages" / "quest" / "emergency-call.html"
QUEST_INDEX = ROOT / "docs" / "pages" / "quest.html"
SITEMAP = ROOT / "docs" / "sitemap.xml"
QUEST_PAGES = (
    ROOT / "docs" / "pages" / "quest" / "steel-wilderness.html",
    ROOT / "docs" / "pages" / "quest" / "gran-water-source.html",
    ROOT / "docs" / "pages" / "quest" / "flame-highlands.html",
    ROOT / "docs" / "pages" / "quest" / "great-spire.html",
    ROOT / "docs" / "pages" / "quest" / "ancient-city.html",
    ROOT / "docs" / "pages" / "quest" / "nova-interior.html",
)


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

    def test_table_layout_contract(self):
        soup = self.page_soup()
        tables = soup.select("table.emergency-call-table")

        self.assertEqual(len(tables), 6)

        for table in tables:
            with self.subTest(table=table):
                header_cells = table.select("thead th")
                self.assertEqual(header_cells[1].get_text("", strip=True), "エマージェンシーコール名")
                self.assertIsNotNone(header_cells[1].find("br"))

                cols = table.select("colgroup > col")
                self.assertEqual(len(cols), 7)
                self.assertEqual(sum("ec-col-difficulty" in (col.get("class") or []) for col in cols), 5)

        css = (ROOT / "docs" / "css" / "page.css").read_text(encoding="utf-8")
        html = self.page_html()

        self.assertIn("body.emergency-call-page #main .emergency-call-table", css)
        self.assertIn("min-width: 0;", css)
        self.assertIn("max-width: 100%;", css)
        self.assertIn(".ec-col-quest", css)
        self.assertIn("width: 20% !important;", css)
        self.assertIn(".ec-col-name", css)
        self.assertIn("width: 15% !important;", css)
        self.assertIn(".ec-col-difficulty", css)
        self.assertIn("width: 13% !important;", css)
        self.assertIn("tr > :first-child", css)
        self.assertIn("white-space: nowrap !important;", css)
        self.assertIn("tr > :nth-child(n + 2)", css)
        self.assertIn("white-space: normal !important;", css)
        self.assertIn("overflow-wrap: anywhere;", css)
        self.assertIn("tbody td:nth-child(n + 3)", css)
        self.assertIn("text-align: left !important;", css)
        self.assertIn("vertical-align: middle;", css)
        self.assertNotIn("vertical-align: top;", css)
        self.assertNotIn("min-width: 1120px;", css)
        self.assertIn('/PSNOVA/css/page.css?v=20260922-ec4', html)

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

    @staticmethod
    def normalize_quest_name(name: str) -> str:
        normalized = name.replace("為", "ため").replace("２", "2").replace("･", "・")
        aliases = {
            "鋼野に穿つ杭": "荒野に穿つ杭",
            "仲間の捜索": "仲間の探索",
            "難：デェフキュオネ決戦": "難：デュフキュオネ決戦",
            "超：昏闇のファンアフォル": "超：昏闇のフォンアフォル",
        }
        return aliases.get(normalized, normalized)

    def test_unavailable_difficulties_match_quest_database(self):
        labels = (
            "ノーマル",
            "ハード",
            "ベリーハード",
            "スーパーハード",
            "エクストラハード",
        )
        quest_difficulties = {}

        for path in QUEST_PAGES:
            soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
            for row in soup.select("tbody > tr"):
                cells = row.find_all("td")
                if len(cells) != 6:
                    continue
                quest = self.normalize_quest_name(cells[0].get_text(" ", strip=True))
                parts = cells[4].get_text("|", strip=True).split("|")
                quest_difficulties[quest] = {
                    index
                    for index, label in enumerate(labels, start=2)
                    if any(part.startswith(label) for part in parts)
                }

        matched_quests = set()
        for row in self.page_soup().select("table.emergency-call-table tbody > tr"):
            cells = row.find_all("td")
            self.assertEqual(len(cells), 7)
            quest = self.normalize_quest_name(cells[0].get_text(" ", strip=True))
            available = quest_difficulties.get(quest)
            if available is None:
                continue

            matched_quests.add(quest)
            for index in range(2, 7):
                value = cells[index].get_text(" ", strip=True)
                with self.subTest(quest=quest, difficulty=labels[index - 2]):
                    if index in available:
                        self.assertNotEqual(value, "－")
                    else:
                        self.assertEqual(value, "－")

        self.assertEqual(len(matched_quests), 109)

    def test_invalid_item_reward_stays_reader_facing(self):
        html = self.page_html()
        text = self.page_soup().get_text(" ", strip=True)

        self.assertIn("極：漆黒の鉄馬と光線獣", text)
        self.assertIn("ファラレイバンサー討伐", text)
        self.assertIn("アイテム付与なし", text)
        self.assertNotIn("7|7|0|0", html)
        self.assertNotIn("invalid_definition", html)
        self.assertNotIn("有効なアイテム定義", text)
        self.assertNotIn("データ上はアイテム数量", text)

    def test_intro_is_reader_facing(self):
        soup = self.page_soup()
        lead = soup.select_one(".page-lead").get_text(" ", strip=True)

        self.assertIn("成功時にもらえる報酬", lead)
        self.assertIn("報酬比較や周回先の確認", lead)
        for developer_term in ("監査", "表示対象", "player-facing", "trial", "ItemID"):
            with self.subTest(developer_term=developer_term):
                self.assertNotIn(developer_term, lead)

    def test_uses_audited_display_names(self):
        html = self.page_html()

        for expected in (
            "鋼の荒野哨戒任務",
            "極：伏す猛銃と天舞う砲凰",
            "超：氷塊のギガティオン",
            "水源を這う脚",
            "源流を塞ぐ杭",
            "★戦士に贈る愛",
            "拠点を守れ　　拠点耐久",
            "赤い樹枝",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, html)

        for obsolete in (
            "銅の荒野",
            "冷：",
            "劇珪",
            "劇産",
            "水装を這う脚",
            "装流を塞ぐ杭",
            "★戦土",
            "拠点を守れ   拠点耐久",
            "赤い樹液",
        ):
            with self.subTest(obsolete=obsolete):
                self.assertNotIn(obsolete, html)

    def test_navigation_wording_avoids_return_links(self):
        soup = self.page_soup()

        self.assertIn("地域へ移動", soup.get_text(" ", strip=True))
        self.assertNotIn("地域から移動", soup.get_text(" ", strip=True))
        for link in soup.find_all("a"):
            self.assertFalse(link.get_text(" ", strip=True).endswith("へ戻る"))


    def test_is_linked_from_quest_index_sidebar_and_sitemap(self):
        quest_index = QUEST_INDEX.read_text(encoding="utf-8")
        sidebar = (ROOT / "docs" / "js" / "sidebar.js").read_text(encoding="utf-8")
        sitemap = SITEMAP.read_text(encoding="utf-8")

        path = "/PSNOVA/pages/quest/emergency-call.html"

        self.assertIn(f'href="{path}"', quest_index)
        self.assertIn(">エマージェンシーコール</span>", quest_index)
        self.assertIn(f'<li><a href="{path}">エマージェンシーコール</a></li>', sidebar)
        self.assertIn(f"https://kylekatann.github.io{path}", sitemap)


if __name__ == "__main__":
    unittest.main()
