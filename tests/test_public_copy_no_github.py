from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def public_html_files():
    return [
        path
        for path in sorted(DOCS.rglob("*.html"))
        if "分類中" not in path.parts
    ]


def test_public_copy_does_not_advertise_github_contribution_channels():
    banned = (
        "github.com/",
        "githubの",
        "github issues",
        "pull request",
        "pullリクエスト",
        "issueを投げ",
    )

    for path in public_html_files():
        text = path.read_text(encoding="utf-8").lower()
        for phrase in banned:
            with __import__("contextlib").nullcontext():
                assert phrase.lower() not in text, f"{path.relative_to(ROOT)} contains {phrase!r}"


def test_known_legacy_github_notices_are_removed():
    homepage = (DOCS / "index.html").read_text(encoding="utf-8")
    material = (DOCS / "pages" / "material.html").read_text(encoding="utf-8")

    assert "データの修正はgithub" not in homepage
    assert "githubの方でissue" not in material
    assert not (DOCS / "issue.html").exists()
    assert not (DOCS / "copyright.html").exists()


