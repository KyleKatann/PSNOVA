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
    "technic-thunder-page": (
        "thunder.html",
        (
            "ゾンデ",
            "ギ・ゾンデ",
            "ラ・ゾンデ",
            "サ・ゾンデ",
            "ゾンディール",
        ),
    ),
    "technic-wind-page": (
        "wind.html",
        (
            "ザン",
            "ギ・ザン",
            "ラ・ザン",
            "サ・ザン",
            "ナ・ザン",
        ),
    ),
    "technic-light-page": (
        "light.html",
        (
            "グランツ",
            "ギ・グランツ",
            "ラ・グランツ",
            "レスタ",
            "アンティ",
        ),
    ),
    "technic-dark-page": (
        "dark.html",
        (
            "メギド",
            "ギ・メギド",
            "ラ・メギド",
            "メギバース",
            "サ・メギド",
        ),
    ),
}


def test_published_technic_entries_use_visible_individual_icons():
    css = PAGE_CSS.read_text(encoding="utf-8")
    css_without_comments = re.sub(r"/\*.*?\*/", "", css, flags=re.S)

    assert "background: transparent no-repeat center / contain;" in css

    selectors = re.findall(r"([^{}]+)\{", css_without_comments)
    for selector in selectors:
        if "technic-" in selector:
            assert ":has(" not in selector

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

    for page_class in TECHNICS:
        assert f"#main.{page_class} .technic-entry-title::before" not in css
