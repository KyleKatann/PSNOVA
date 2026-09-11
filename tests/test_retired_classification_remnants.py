from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RETIRED_MARKER = "".join(chr(value) for value in (20998, 39006, 20013))


def test_deleted_classification_marker_is_absent_from_repository_text():
    violations = []

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        if RETIRED_MARKER in text:
            violations.append(str(path.relative_to(ROOT)))

    assert not violations, (
        "削除済み分類ディレクトリの参照が残っている:\n"
        + "\n".join(violations)
    )
