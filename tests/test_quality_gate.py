import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUALITY = ROOT / "tools" / "psnova_quality.py"


class QualityGateTests(unittest.TestCase):
    def test_uses_five_fix_playwright_cadence(self):
        source = QUALITY.read_text(encoding="utf-8")

        self.assertIn("FULL_INTERVAL = 5", source)
        self.assertIn(
            'CADENCE_FILE = ROOT / ".git" / "psnova-quality-cadence"',
            source,
        )

    def test_fast_runs_diff_check_and_all_pytest(self):
        source = QUALITY.read_text(encoding="utf-8")

        self.assertIn(
            'run(["git", "diff", "--check"])',
            source,
        )
        self.assertIn(
            'run([sys.executable, "-m", "pytest", "-q"])',
            source,
        )

    def test_full_runs_ui_health(self):
        source = QUALITY.read_text(encoding="utf-8")

        self.assertIn(
            '"tests/ui/ui-health.spec.js"',
            source,
        )
        self.assertIn("run_full_ui()", source)

    def test_targeted_supports_project_and_grep(self):
        source = QUALITY.read_text(encoding="utf-8")

        self.assertIn(
            'command.append(f"--project={project}")',
            source,
        )
        self.assertIn(
            'command.extend(["--grep", grep])',
            source,
        )

    def test_inventory_does_not_modify_repository_files(self):
        source = QUALITY.read_text(encoding="utf-8")

        start = source.index("def inventory():")
        end = source.index("\ndef show_status():", start)
        body = source[start:end]

        self.assertNotIn(".write_text(", body)
        self.assertNotIn("subprocess.run(", body)


if __name__ == "__main__":
    unittest.main()