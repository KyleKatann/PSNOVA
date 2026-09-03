import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITE_NAME = "PSNOVA攻略サイト"
SITE_ORIGIN = "https://kylekatann.github.io"
SITE_PREFIX = "/PSNOVA/"


class MetadataParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.title_parts = []
        self.descriptions = []
        self.canonicals = []
        self.og = {}

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attributes = dict(attrs)

        if tag == "title":
            self.in_title = True
            return

        if tag == "meta":
            name = (attributes.get("name") or "").lower()
            prop = (attributes.get("property") or "").lower()
            content = attributes.get("content")

            if name == "description":
                self.descriptions.append(content)

            if prop.startswith("og:"):
                self.og.setdefault(prop, []).append(content)

        if tag == "link":
            rel = (attributes.get("rel") or "").lower().split()
            if "canonical" in rel:
                self.canonicals.append(attributes.get("href"))

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    @property
    def title(self):
        return "".join(self.title_parts).strip()


def public_html_files():
    for path in DOCS.rglob("*.html"):
        if "分類中" not in path.parts:
            yield path


class PublicMetadataTests(unittest.TestCase):
    def test_public_metadata_is_complete_and_consistent(self):
        violations = []

        for path in public_html_files():
            parser = MetadataParser()
            parser.feed(path.read_text(encoding="utf-8"))
            parser.close()

            rel = path.relative_to(ROOT)

            if not parser.title:
                violations.append(f"{rel}: missing or empty title")

            if len(parser.descriptions) != 1:
                violations.append(
                    f"{rel}: expected 1 meta description, "
                    f"found {len(parser.descriptions)}"
                )

            if len(parser.canonicals) != 1:
                violations.append(
                    f"{rel}: expected 1 canonical, "
                    f"found {len(parser.canonicals)}"
                )

            required_og = (
                "og:title",
                "og:description",
                "og:type",
                "og:url",
                "og:site_name",
            )

            for prop in required_og:
                values = parser.og.get(prop, [])
                if len(values) != 1:
                    violations.append(
                        f"{rel}: expected 1 {prop}, found {len(values)}"
                    )
                elif not (values[0] or "").strip():
                    violations.append(f"{rel}: empty {prop}")

            description = (
                (parser.descriptions[0] or "").strip()
                if len(parser.descriptions) == 1
                else None
            )
            canonical = (
                (parser.canonicals[0] or "").strip()
                if len(parser.canonicals) == 1
                else None
            )

            og_title = (
                (parser.og.get("og:title", [None])[0] or "").strip()
                if len(parser.og.get("og:title", [])) == 1
                else None
            )
            og_description = (
                (parser.og.get("og:description", [None])[0] or "").strip()
                if len(parser.og.get("og:description", [])) == 1
                else None
            )
            og_url = (
                (parser.og.get("og:url", [None])[0] or "").strip()
                if len(parser.og.get("og:url", [])) == 1
                else None
            )
            og_site_name = (
                (parser.og.get("og:site_name", [None])[0] or "").strip()
                if len(parser.og.get("og:site_name", [])) == 1
                else None
            )

            if og_title is not None and parser.title != og_title:
                violations.append(
                    f"{rel}: title and og:title differ "
                    f"({parser.title!r} != {og_title!r})"
                )

            if (
                description is not None
                and og_description is not None
                and description != og_description
            ):
                violations.append(
                    f"{rel}: description and og:description differ"
                )

            if canonical is not None and og_url is not None:
                if canonical != og_url:
                    violations.append(
                        f"{rel}: canonical and og:url differ "
                        f"({canonical!r} != {og_url!r})"
                    )

            if og_site_name is not None and og_site_name != SITE_NAME:
                violations.append(
                    f"{rel}: unexpected og:site_name={og_site_name!r}"
                )

            if path == DOCS / "index.html":
                if parser.title != SITE_NAME:
                    violations.append(
                        f"{rel}: homepage title must be {SITE_NAME!r}"
                    )
            elif parser.title and not parser.title.startswith(
                SITE_NAME + " - "
            ):
                violations.append(
                    f"{rel}: non-homepage title violates naming convention "
                    f"({parser.title!r})"
                )

            if canonical:
                parts = urlsplit(canonical)

                if parts.scheme != "https":
                    violations.append(
                        f"{rel}: canonical must use HTTPS ({canonical})"
                    )

                if parts.netloc != "kylekatann.github.io":
                    violations.append(
                        f"{rel}: unexpected canonical host ({canonical})"
                    )

                if not parts.path.startswith(SITE_PREFIX):
                    violations.append(
                        f"{rel}: canonical outside /PSNOVA/ ({canonical})"
                    )

        self.assertEqual(
            [],
            violations,
            "Metadata violations:\n" + "\n".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
