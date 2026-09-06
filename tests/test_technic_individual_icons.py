import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE_CSS = ROOT / "docs" / "css" / "page.css"
TECH_IMG = ROOT / "docs" / "img" / "tech"
TECHNIC_PAGES = ROOT / "docs" / "pages" / "technic"


TECHNICS = {
    "technic-fire-page": (
        "fire.html",
        (
            "フォイエ",
            "ギ・フォイエ",
            "ラ・フォイエ",
            "サ・フォイエ",
            "シフタ",
        ),
    ),
    "technic-ice-page": (
        "ice.html",
        (
            "バータ",
            "ギ・バータ",
            "ラ・バータ",
            "サ・バータ",
            "デバンド",
        ),
    ),
}


def test_published_technic_entries_use_visible_individual_icons():
    css = PAGE_CSS.read_text(encoding="utf-8")

    assert "background: transparent no-repeat center / contain;" in css
    assert ":has(" not in css

    for page_class, (filename, names) in TECHNICS.items():
        html = (TECHNIC_PAGES / filename).read_text(encoding="utf-8")
        headings = tuple(
            re.findall(r'<h2 class="technic-entry-title">([^<]+)</h2>', html)
        )
        assert headings == names

        for section_index, name in enumerate(names, start=2):
            selector = (
                f"#main.{page_class} > .technic-entry:nth-of-type({section_index}) "
                "> .technic-entry-title::before"
            )
            asset = f'background-image: url("/PSNOVA/img/tech/{name}.png");'

            assert selector in css
            assert asset in css
            assert (TECH_IMG / f"{name}.png").is_file()


def test_published_technic_entries_do_not_use_attribute_common_heading_icons():
    css = PAGE_CSS.read_text(encoding="utf-8")

    assert '#main.technic-fire-page .technic-entry-title::before' not in css
    assert '#main.technic-ice-page .technic-entry-title::before' not in css
