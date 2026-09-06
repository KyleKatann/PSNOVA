from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TABLE_JS = ROOT / "docs" / "js" / "table-enhancements.js"
SIDEBAR_JS = ROOT / "docs" / "js" / "sidebar.js"
TECHNIC_DIR = ROOT / "docs" / "pages" / "technic"
NOTE = (
    "追加素材: ホ※=ホワイトチケット×1 / "
    "ブ※=ブラックチケット×2 / "
    "マ※=マキアファクター×1"
)
NOTE_HTML = f'<p class="technic-material-note">{NOTE}</p>'


def test_each_technic_keeps_static_material_legend_after_second_level_table():
    for filename in ("fire.html", "ice.html"):
        html = (TECHNIC_DIR / filename).read_text(encoding="utf-8")

        assert html.count('class="technic-material-note"') == 5
        assert html.count(NOTE) == 5
        assert html.count(f"</table></div>{NOTE_HTML}</section>") == 5

        intro = html.split('<section class="technic-entry">', 1)[0]
        assert "technic-material-note" not in intro


def test_runtime_javascript_does_not_repair_technic_static_content():
    table_js = TABLE_JS.read_text(encoding="utf-8")
    sidebar_js = SIDEBAR_JS.read_text(encoding="utf-8")

    for forbidden in (
        "placeTechnicMaterialNotes",
        "pageNote.cloneNode",
        "pageNote.remove",
        "technic-material-note",
    ):
        assert forbidden not in table_js

    for forbidden in (
        "ensurePageStylesheet",
        "initTechnicDetailPresentation",
        "technic-detail-page",
        "technic-entry-title",
        "technic-summary-table",
    ):
        assert forbidden not in sidebar_js
