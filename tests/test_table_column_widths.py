from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEST_PAGES = (
    "great-spire.html",
    "steel-wilderness.html",
    "gran-water-source.html",
    "flame-highlands.html",
    "ancient-city.html",
    "nova-interior.html",
    "additional.html",
)


def test_quest_pages_share_six_column_width_contract():
    page_css = (ROOT / "docs" / "css" / "page.css").read_text(encoding="utf-8")

    for filename in QUEST_PAGES:
        html = (ROOT / "docs" / "pages" / "quest" / filename).read_text(encoding="utf-8")
        assert '<link rel="stylesheet" href="/PSNOVA/css/page.css">' in html

    assert 'html:has(link[rel="canonical"][href*="/PSNOVA/pages/quest/"]) #main table {' in page_css
    assert "table-layout: fixed;" in page_css
    for index, width in enumerate((18, 11, 16, 15, 20, 20), start=1):
        rule = f'#main table tr > :nth-child({index}) {{ width: {width}%; }}'
        assert rule in page_css


def test_food_tables_share_identical_static_colgroup():
    html = (ROOT / "docs" / "pages" / "food.html").read_text(encoding="utf-8")
    colgroup = (
        '<colgroup><col style="width:24%"><col style="width:27%">'
        '<col style="width:9%"><col style="width:40%"></colgroup>'
    )

    assert html.count("<table>") == 3
    assert html.count(colgroup) == 3
