from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
THIS_FILE = Path(__file__).resolve()
AGENT_GUIDE = ROOT / "Agent.md"
MIN_AGENT_GUIDE_BYTES = 28_000
MIN_AGENT_GUIDE_LINES = 140


def test_tests_do_not_treat_agent_md_prose_as_a_contract():
    violations = []

    for path in sorted(TESTS.glob("test_*.py")):
        if path.resolve() == THIS_FILE:
            continue

        source = path.read_text(encoding="utf-8")

        if "Agent.md" in source:
            violations.append(
                str(path.relative_to(ROOT))
            )

    assert not violations, (
        "テストはAgent.mdの自然言語ではなく、"
        "実装の動作・状態を検証しなければならない:\n"
        + "\n".join(violations)
    )


def test_agent_md_is_not_catastrophically_truncated():
    raw = AGENT_GUIDE.read_bytes()
    text = raw.decode("utf-8")

    assert len(raw) >= MIN_AGENT_GUIDE_BYTES, (
        "Agent.mdのbyte数が安全下限を下回っている。"
        "意図しない全文置換または大量欠落を確認すること。"
    )
    assert len(text.splitlines()) >= MIN_AGENT_GUIDE_LINES, (
        "Agent.mdの行数が安全下限を下回っている。"
        "意図しない全文置換または大量欠落を確認すること。"
    )
