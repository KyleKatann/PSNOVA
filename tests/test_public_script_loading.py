import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SIDEBAR = DOCS / "js" / "sidebar.js"

PUBLIC_SCRIPTS = (
    "/PSNOVA/js/openclose.js",
    "/PSNOVA/js/menubar.js",
    "/PSNOVA/js/sidebar.js",
)


def public_html_files():
    yield from DOCS.rglob("*.html")


class PublicScriptLoadingTests(unittest.TestCase):
    def test_shared_head_scripts_are_deferred(self):
        violations = []

        for path in public_html_files():
            html = path.read_text(encoding="utf-8")

            for src in PUBLIC_SCRIPTS:
                pattern = re.compile(
                    r'<script\b'
                    r'(?=[^>]*\bdefer\b)'
                    r'(?=[^>]*\bsrc=["\']'
                    + re.escape(src)
                    + r'["\'])'
                    r'[^>]*></script>',
                    re.IGNORECASE,
                )

                if not pattern.search(html):
                    violations.append(
                        f"{path.relative_to(ROOT)}: {src}"
                    )

        self.assertEqual(
            [],
            violations,
            "共通scriptにはdeferが必要:\n"
            + "\n".join(violations),
        )

    def test_retired_page_top_script_is_not_referenced(self):
        violations = []
        retired = "/PSNOVA/js/fixmenu_pagetop.js"

        for path in public_html_files():
            html = path.read_text(encoding="utf-8")
            if retired in html:
                violations.append(str(path.relative_to(ROOT)))

        self.assertEqual(
            [],
            violations,
            "廃止済みpage-top scriptへの参照が残っている:\n"
            + "\n".join(violations),
        )

    def test_public_html_has_no_inline_scripts(self):
        violations = []

        pattern = re.compile(
            r"<script\b(?![^>]*\bsrc=)[^>]*>",
            re.IGNORECASE,
        )

        for path in public_html_files():
            html = path.read_text(encoding="utf-8")

            matches = pattern.findall(html)

            if matches:
                violations.append(
                    f"{path.relative_to(ROOT)}: {len(matches)}"
                )

        self.assertEqual(
            [],
            violations,
            "公開HTMLにinline scriptが残っている:\n"
            + "\n".join(violations),
        )

    def test_sidebar_self_initializes(self):
        js = SIDEBAR.read_text(encoding="utf-8")

        self.assertIn(
            "function initSidebar()",
            js,
        )
        self.assertIn(
            "side();",
            js,
        )
        self.assertIn(
            'typeof initResponsiveContentsMenu === "function"',
            js,
        )
        self.assertIn(
            "initResponsiveContentsMenu();",
            js,
        )

        init_start = js.index("function initSidebar()")
        side_call = js.index("side();", init_start)
        menu_bind = js.index(
            "initResponsiveContentsMenu();",
            init_start,
        )

        self.assertLess(
            side_call,
            menu_bind,
            "モバイルメニューは#sub生成後にbindしなければならない。",
        )
        self.assertIn(
            '"DOMContentLoaded"',
            js,
        )
        self.assertIn(
            'contents.querySelector("#main")',
            js,
        )

    def test_sidebar_does_not_depend_on_document_current_script(self):
        js = SIDEBAR.read_text(encoding="utf-8")

        self.assertNotIn(
            "document.currentScript",
            js,
        )


if __name__ == "__main__":
    unittest.main()
