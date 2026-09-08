from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PROHIBITED_SOURCE_PROVENANCE = (
    "原典",
    "旧PSNOVA攻略Wiki",
    "旧Wiki",
    "旧wiki",
    "アーカイブでは",
    "参考元では",
    "移植元では",
    "元ページでは",
    "出典では",
    "Tipsでは",
    "reference原本",
    "移植",
    "記録されている",
    "記録されていた",
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

    assert not violations, "公開文言は情報源を示唆しない表現でなければならない:\n" + "\n".join(violations)
