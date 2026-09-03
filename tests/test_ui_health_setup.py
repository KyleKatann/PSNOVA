import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "package.json"
CONFIG = ROOT / "playwright.config.js"
UI_TEST = ROOT / "tests" / "ui" / "ui-health.spec.js"
SERVER = ROOT / "tools" / "serve_psnova.py"
WORKFLOW = ROOT / ".github" / "workflows" / "tests.yml"


class UiHealthSetupTests(unittest.TestCase):
    def test_playwright_dependency_and_command_are_pinned(self):
        package = json.loads(PACKAGE.read_text(encoding="utf-8"))

        self.assertEqual("playwright test", package["scripts"]["test:ui"])
        self.assertEqual("1.62.1", package["devDependencies"]["@playwright/test"])

    def test_ui_health_uses_failure_artifacts_without_snapshot_baseline(self):
        config = CONFIG.read_text(encoding="utf-8")
        test = UI_TEST.read_text(encoding="utf-8")

        self.assertIn("screenshot: 'only-on-failure'", config)
        self.assertIn("trace: 'retain-on-failure'", config)
        self.assertIn("desktop-chromium", config)
        self.assertIn("mobile-chromium", config)
        self.assertNotIn("toHaveScreenshot", test)

    def test_ui_health_covers_public_routes_and_obvious_rendering_failures(self):
        test = UI_TEST.read_text(encoding="utf-8")

        for token in (
            "sitemap.xml",
            "pages', 'weapon",
            "page.on('pageerror'",
            "page.on('console'",
            "page.on('requestfailed'",
            "document.documentElement.scrollWidth",
            "image.naturalWidth === 0",
            "document.styleSheets",
            "#main and #sub should not overlap on desktop",
            "aria-expanded",
        ):
            with self.subTest(token=token):
                self.assertIn(token, test)

    def test_local_server_preserves_psnova_path_prefix(self):
        server = SERVER.read_text(encoding="utf-8")

        self.assertIn('request_path.startswith("/PSNOVA/")', server)
        self.assertIn('request_path[len("/PSNOVA"):]', server)
        self.assertIn('ROOT / "docs"', server)

    def test_actions_remain_manual_only_and_run_ui_health(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("workflow_dispatch:", workflow)
        self.assertIsNone(re.search(r"(?m)^\s*(?:push|pull_request):", workflow))
        self.assertIn("actions/setup-node@v4", workflow)
        self.assertIn("npx playwright install --with-deps chromium", workflow)
        self.assertIn("npm run test:ui", workflow)


if __name__ == "__main__":
    unittest.main()
