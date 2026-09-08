from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
THIS_FILE = Path(__file__).resolve()


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
