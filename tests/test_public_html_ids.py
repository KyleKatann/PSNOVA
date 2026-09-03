import unittest
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class IdParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        element_id = attributes.get("id")
        if element_id is not None:
            self.ids.append(element_id)


def public_html_files():
    for path in DOCS.rglob("*.html"):
        if "分類中" not in path.parts:
            yield path


class PublicHtmlIdTests(unittest.TestCase):
    def test_public_html_ids_are_nonempty_and_unique(self):
        violations = []

        for path in public_html_files():
            parser = IdParser()
            parser.feed(path.read_text(encoding="utf-8"))
            parser.close()

            empty_ids = [value for value in parser.ids if not value.strip()]
            if empty_ids:
                violations.append(
                    f"{path.relative_to(ROOT)}: empty id attribute"
                )

            counts = Counter(parser.ids)
            duplicates = sorted(
                element_id
                for element_id, count in counts.items()
                if element_id and count > 1
            )

            for element_id in duplicates:
                violations.append(
                    f"{path.relative_to(ROOT)}: duplicate id={element_id!r} "
                    f"x{counts[element_id]}"
                )

        self.assertEqual(
            [],
            violations,
            "Invalid public HTML IDs found:\n" + "\n".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
