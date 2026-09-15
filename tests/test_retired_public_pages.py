from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

RETIRED_PATHS = (
    "/PSNOVA/copyright.html",
    "/PSNOVA/issue.html",
    "/PSNOVA/pages/faq.html",
    "/PSNOVA/pages/difficulty.html",
    "/PSNOVA/pages/weapon.html",
)


def test_retired_public_pages_are_not_restored():
    assert not (DOCS / "copyright.html").exists()
    assert not (DOCS / "issue.html").exists()
    assert not (DOCS / "pages" / "faq.html").exists()
    assert not (DOCS / "pages" / "difficulty.html").exists()
    assert not (DOCS / "pages" / "weapon.html").exists()


def test_retired_public_pages_are_not_linked_or_indexed():
    public_files = [
        path
        for path in DOCS.rglob("*")
        if path.is_file() and path.suffix.lower() in {".html", ".xml", ".js"}
    ]

    for path in public_files:
        text = path.read_text(encoding="utf-8")
        for retired in RETIRED_PATHS:
            assert retired not in text, (
                f"廃止済み公開ページへの参照が残っている: {path.relative_to(ROOT)} -> {retired}"
            )
