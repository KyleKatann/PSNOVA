from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PROHIBITED_SOURCE_PROVENANCE = (
    "原典では",
    "旧Wikiでは",
    "旧wikiでは",
    "アーカイブでは",
    "参考元では",
    "移植元では",
    "元ページでは",
    "出典では",
)


def public_html_files():
    for path in DOCS.rglob("*.html"):
        relative = path.relative_to(DOCS)
        if "分類中" in relative.parts:
            continue
        yield path


def test_public_copy_does_not_expose_source_provenance():
    violations = []

    for path in public_html_files():
        text = path.read_text(encoding="utf-8")
        for phrase in PROHIBITED_SOURCE_PROVENANCE:
            if phrase in text:
                violations.append(f"{path.relative_to(ROOT)}: {phrase}")

    assert not violations, "public copy must be source-neutral:\n" + "\n".join(violations)
