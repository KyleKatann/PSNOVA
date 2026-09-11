import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class AnchorParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.anchors = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            self.anchors.append(dict(attrs))


def public_html_files():
    yield from DOCS.rglob("*.html")


class PublicExternalLinkTests(unittest.TestCase):
    def test_public_external_web_links_do_not_use_plain_http(self):
        violations = []

        for path in public_html_files():
            parser = AnchorParser()
            parser.feed(path.read_text(encoding="utf-8"))

            for attrs in parser.anchors:
                href = (attrs.get("href") or "").strip()
                if urlsplit(href).scheme == "http":
                    violations.append(
                        f"{path.relative_to(ROOT)} -> {href}"
                    )

        self.assertEqual(
            [],
            violations,
            "HTTPの外部リンクが見つかった:\n" + "\n".join(violations),
        )

    def test_blank_external_links_explicitly_use_noopener(self):
        violations = []

        for path in public_html_files():
            parser = AnchorParser()
            parser.feed(path.read_text(encoding="utf-8"))

            for attrs in parser.anchors:
                href = (attrs.get("href") or "").strip()
                target = (attrs.get("target") or "").lower()
                rel = set((attrs.get("rel") or "").lower().split())

                parts = urlsplit(href)
                if (
                    target == "_blank"
                    and parts.scheme in ("http", "https")
                    and "noopener" not in rel
                ):
                    violations.append(
                        f"{path.relative_to(ROOT)} -> {href}"
                    )

        self.assertEqual(
            [],
            violations,
            "target=_blank のリンクに明示的な noopener がない:\n"
            + "\n".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
