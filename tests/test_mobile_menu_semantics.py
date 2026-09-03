import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
JS = DOCS / "js" / "openclose.js"

MENU_ID_RE = re.compile(
    r"<(?P<tag>[a-zA-Z0-9]+)\b(?P<attrs>[^>]*)"
    r'\bid=["\']menubar_hdr["\'](?P<rest>[^>]*)>',
    re.IGNORECASE,
)


def public_html_files():
    for path in DOCS.rglob("*.html"):
        if "分類中" not in path.parts:
            yield path


class MobileMenuSemanticsTests(unittest.TestCase):
    def test_mobile_menu_trigger_uses_native_button(self):
        violations = []

        for path in public_html_files():
            text = path.read_text(encoding="utf-8")

            for match in MENU_ID_RE.finditer(text):
                markup = match.group(0)
                tag = match.group("tag").lower()

                if tag != "button":
                    violations.append(
                        f"{path.relative_to(ROOT)}: menubar_hdr uses <{tag}>"
                    )
                    continue

                if not re.search(
                    r'\btype=["\']button["\']',
                    markup,
                    re.IGNORECASE,
                ):
                    violations.append(
                        f"{path.relative_to(ROOT)}: menubar_hdr missing type=button"
                    )

        self.assertEqual(
            [],
            violations,
            "Mobile menu trigger must use native button semantics:\n"
            + "\n".join(violations),
        )

    def test_openclose_does_not_reimplement_native_button_keyboard_behavior(self):
        js = JS.read_text(encoding="utf-8")

        self.assertNotIn(
            'button.setAttribute("role", "button")',
            js,
        )
        self.assertNotIn(
            'button.setAttribute("tabindex", "0")',
            js,
        )
        self.assertNotIn(
            'event.key === "Enter" || event.key === " "',
            js,
        )

        # State/accessibility information still belongs in JS.
        self.assertIn(
            'button.setAttribute("aria-expanded", String(open))',
            js,
        )
        self.assertIn(
            'button.setAttribute("aria-controls", menu.id)',
            js,
        )
        self.assertIn(
            'button.setAttribute("aria-label"',
            js,
        )


if __name__ == "__main__":
    unittest.main()
