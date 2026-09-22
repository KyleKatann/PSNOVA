from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "pages" / "quest" / "emergency-call.html"
QUEST_INDEX = ROOT / "docs" / "pages" / "quest.html"
SITEMAP = ROOT / "docs" / "sitemap.xml"


def page_html() -> str:
    return PAGE.read_text(encoding="utf-8")


def page_soup() -> BeautifulSoup:
    return BeautifulSoup(page_html(), "html.parser")


def test_emergency_call_page_keeps_all_public_variants():
    soup = page_soup()
    tables = soup.select("main#main .table-scroll > table")
    rows = [row for table in tables for row in table.select("tbody > tr")]

    assert len(tables) == 6
    assert len(rows) == 408

    quest_names = {
        cells[0].get_text(" ", strip=True)
        for row in rows
        if len(cells := row.find_all("td")) >= 2
    }
    assert len(quest_names) == 115


def test_emergency_call_page_uses_public_difficulty_labels():
    text = page_soup().get_text(" ", strip=True)

    for label in (
        "ノーマル",
        "ハード",
        "ベリーハード",
        "スーパーハード",
        "エクストラハード",
    ):
        assert label in text


def test_emergency_call_page_explains_invalid_item_reward_without_internal_id():
    html = page_html()
    text = page_soup().get_text(" ", strip=True)

    assert "極：漆黒の鉄馬と光線獣" in text
    assert "ファラレイバンサー討伐" in text
    assert "アイテム付与なし" in text
    assert "7|7|0|0" not in html
    assert "invalid_definition" not in html


def test_emergency_call_page_is_linked_from_quest_index_and_sitemap():
    quest_index = QUEST_INDEX.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")

    path = "/PSNOVA/pages/quest/emergency-call.html"

    assert f'href="{path}"' in quest_index
    assert ">エマージェンシーコール</span>" in quest_index
    assert f"https://kylekatann.github.io{path}" in sitemap
