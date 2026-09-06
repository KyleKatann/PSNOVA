from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TABLE_JS = ROOT / "docs" / "js" / "table-enhancements.js"
TECHNIC_DIR = ROOT / "docs" / "pages" / "technic"
NOTE = (
    "追加素材: ホ※=ホワイトチケット×1 / "
    "ブ※=ブラックチケット×2 / "
    "マ※=マキアファクター×1"
)


def test_technic_pages_keep_one_static_material_legend_as_source_data():
    for filename in ("fire.html", "ice.html"):
        html = (TECHNIC_DIR / filename).read_text(encoding="utf-8")
        assert html.count('class="technic-material-note"') == 1
        assert html.count(NOTE) == 1


def test_table_enhancement_places_material_legend_after_each_second_level_table():
    js = TABLE_JS.read_text(encoding="utf-8")

    for token in (
        "function placeTechnicMaterialNotes()",
        'main.querySelector(".technic-material-note")',
        'section.querySelectorAll(".technic-level-scroll").length === 2',
        'tables[1].insertAdjacentElement("afterend", pageNote.cloneNode(true))',
        "pageNote.remove()",
        "placeTechnicMaterialNotes();",
    ):
        assert token in js


def test_table_enhancement_does_not_hardcode_material_data():
    js = TABLE_JS.read_text(encoding="utf-8")

    for game_data in (
        "ホワイトチケット",
        "ブラックチケット",
        "マキアファクター",
        "ホ※",
        "ブ※",
        "マ※",
    ):
        assert game_data not in js
