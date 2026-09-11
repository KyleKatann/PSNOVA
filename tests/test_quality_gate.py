import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUALITY = ROOT / "tools" / "psnova_quality.py"
ACCESSIBILITY = ROOT / "tests" / "ui" / "accessibility.spec.js"
COLOR_CONTRACT = ROOT / "tests" / "test_accessible_color_contract.py"
WORKFLOW = ROOT / ".github" / "workflows" / "tests.yml"


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

    def test_axe_runs_public_accessibility_audit(self):
        source = QUALITY.read_text(encoding="utf-8")

        self.assertIn("def run_axe():", source)
        self.assertIn(
            '"tests/ui/accessibility.spec.js"',
            source,
        )
        self.assertIn(
            '"--project=desktop-chromium"',
            source,
        )
        start = source.index("def run_axe():")
        end = source.index("\ndef run_targeted_ui", start)
        axe_body = source[start:end]

        self.assertNotIn(
            '"--workers=1"',
            axe_body,
        )
        self.assertIn(
            'sub.add_parser("axe")',
            source,
        )

        inventory_start = source.index("def inventory():")
        inventory_end = source.index(
            "\ndef show_status():",
            inventory_start,
        )
        inventory = source[inventory_start:inventory_end]

        self.assertNotIn(
            '"axe accessibility scan"',
            inventory,
        )
        self.assertNotIn(
            '"color contrast"',
            inventory,
        )

    def test_color_contrast_enforcement_is_intentionally_disabled(self):
        source = ACCESSIBILITY.read_text(encoding="utf-8")

        self.assertIn(
            ".disableRules(['color-contrast'])",
            source,
        )
        self.assertFalse(
            COLOR_CONTRACT.exists(),
            "専用の自動color-contractテストは削除済みの状態を維持しなければならない",
        )

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

    def test_actions_tests_workflow_is_manual_dispatch_only(self):
        source = WORKFLOW.read_text(encoding="utf-8")
        trigger_section = source.split("\njobs:", 1)[0]

        self.assertIn("on:\n  workflow_dispatch:", trigger_section)
        for forbidden in ("push:", "pull_request:", "schedule:", "workflow_call:"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, trigger_section)


if __name__ == "__main__":
    unittest.main()
