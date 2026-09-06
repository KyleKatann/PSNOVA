from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE_CSS = ROOT / "docs" / "css" / "page.css"
TECH_IMG = ROOT / "docs" / "img" / "tech"


TECHNICS = {
    "technic-fire-page": (
        "フォイエ",
        "ギ・フォイエ",
        "ラ・フォイエ",
        "サ・フォイエ",
        "シフタ",
    ),
    "technic-ice-page": (
        "バータ",
        "ギ・バータ",
        "ラ・バータ",
        "サ・バータ",
        "デバンド",
    ),
}


def test_published_technic_entries_use_individual_icons():
    css = PAGE_CSS.read_text(encoding="utf-8")

    for page_class, names in TECHNICS.items():
        for name in names:
            selector = (
                f'#main.{page_class} .technic-entry:has('
                f'.technic-level-scroll[aria-label^="{name} "]) '
                '.technic-entry-title::before'
            )
            asset = f'background-image: url("/PSNOVA/img/tech/{name}.png");'

            assert selector in css
            assert asset in css
            assert (TECH_IMG / f"{name}.png").is_file()


def test_published_technic_entries_do_not_use_attribute_common_heading_icons():
    css = PAGE_CSS.read_text(encoding="utf-8")

    assert '#main.technic-fire-page .technic-entry-title::before' not in css
    assert '#main.technic-ice-page .technic-entry-title::before' not in css
