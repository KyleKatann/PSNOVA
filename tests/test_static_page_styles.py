from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

STATIC_PAGE_STYLE_TARGETS = (
    DOCS / "pages" / "weapon.html",
    DOCS / "pages" / "weapon" / "doublesaber.html",
    DOCS / "pages" / "weapon" / "halo.html",
    DOCS / "pages" / "weapon" / "knuckle.html",
    DOCS / "pages" / "weapon" / "partizan.html",
    DOCS / "pages" / "weapon" / "pile.html",
    DOCS / "pages" / "weapon" / "rifle.html",
    DOCS / "pages" / "weapon" / "rod.html",
    DOCS / "pages" / "weapon" / "sword.html",
    DOCS / "pages" / "weapon" / "talis.html",
    DOCS / "pages" / "weapon" / "tmachinegun.html",
    DOCS / "pages" / "weapon" / "wand.html",
    DOCS / "pages" / "gigantes.html",
)


def test_runtime_page_style_targets_load_page_css_statically():
    marker = '<link rel="stylesheet" href="/PSNOVA/css/page.css" data-psnova-page-style="true">'

    for path in STATIC_PAGE_STYLE_TARGETS:
        html = path.read_text(encoding="utf-8")
        assert html.count(marker) == 1, path.relative_to(ROOT)
        assert html.count('/PSNOVA/css/page.css') == 1, path.relative_to(ROOT)
