import re
from pathlib import Path
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITEMAP = DOCS / "sitemap.xml"
CSS = DOCS / "css" / "wiki-table.css"
CONFIG = DOCS / "_config.yml"
AGENT = ROOT / "Agent.md"
SITE_PREFIX = "/PSNOVA/"


TABLE_RE = re.compile(
    r"<table\b[^>]*>(.*?)</table>",
    re.I | re.S,
)

ROW_RE = re.compile(
    r"<tr\b[^>]*>.*?</tr>",
    re.I | re.S,
)

CELL_RE = re.compile(
    r"<(?P<tag>th|td)\b(?P<attrs>[^>]*)>"
    r"(?P<body>.*?)"
    r"</(?P=tag)>",
    re.I | re.S,
)


def public_html_paths():
    root = ElementTree.parse(SITEMAP).getroot()
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    result = set()

    for loc in root.findall("sm:url/sm:loc", ns):
        parsed = urlparse((loc.text or "").strip())
        path = unquote(parsed.path)

        if not path.startswith(SITE_PREFIX):
            continue

        relative = path[len(SITE_PREFIX):] or "index.html"

        if relative.endswith(".html"):
            result.add(DOCS / relative)

    return sorted(result)


def test_shared_header_style_is_semantic_only():
    css = CSS.read_text(encoding="utf-8")

    assert "#main table > thead th {" in css
    assert "font-weight: 800;" in css
    assert "background: var(--accent-soft);" in css
    assert "text-align: center !important;" in css

    for forbidden in (
        "[bgcolor]",
        "tbody th:not([bgcolor])",
        "not(:has(> thead))",
        "tbody:first-of-type > tr:first-child",
    ):
        assert forbidden not in css


def test_public_data_table_headers_use_thead_and_scope_col():
    failures = []

    for path in public_html_paths():
        html = path.read_text(encoding="utf-8")

        for index, table_match in enumerate(
            TABLE_RE.finditer(html),
            start=1,
        ):
            table = table_match.group(1)

            if "<thead" not in table.lower():
                continue

            assert "<tbody" in table.lower(), (
                f"{path.relative_to(ROOT)} "
                f"table {index}: tbody missing"
            )

            thead = re.search(
                r"<thead\b[^>]*>(.*?)</thead>",
                table,
                re.I | re.S,
            )

            assert thead is not None

            cells = list(
                CELL_RE.finditer(
                    thead.group(1)
                )
            )

            assert cells

            for cell in cells:
                if cell.group("tag").lower() != "th":
                    failures.append(
                        f"{path.relative_to(ROOT)} "
                        f"table {index}: header is not TH"
                    )

                if not re.search(
                    r'\bscope\s*=\s*["\']col["\']',
                    cell.group("attrs"),
                    re.I,
                ):
                    failures.append(
                        f"{path.relative_to(ROOT)} "
                        f"table {index}: TH lacks scope=col"
                    )

                if re.search(
                    r"\bbgcolor\s*=",
                    cell.group("attrs"),
                    re.I,
                ):
                    failures.append(
                        f"{path.relative_to(ROOT)} "
                        f"table {index}: header bgcolor remains"
                    )

    assert not failures, "\n".join(failures)


def test_public_semantic_table_body_does_not_use_all_th_rows():
    failures = []

    for path in public_html_paths():
        html = path.read_text(encoding="utf-8")

        for index, table_match in enumerate(
            TABLE_RE.finditer(html),
            start=1,
        ):
            table = table_match.group(1)

            tbody = re.search(
                r"<tbody\b[^>]*>(.*?)</tbody>",
                table,
                re.I | re.S,
            )

            if not tbody:
                continue

            for row in ROW_RE.finditer(
                tbody.group(1)
            ):
                cells = list(
                    CELL_RE.finditer(
                        row.group(0)
                    )
                )

                if cells and all(
                    cell.group("tag").lower() == "th"
                    for cell in cells
                ):
                    failures.append(
                        f"{path.relative_to(ROOT)} "
                        f"table {index}: all-TH body row"
                    )

    assert not failures, "\n".join(failures)


def test_enemy_and_gigantes_share_semantic_header_contract():
    enemy = (
        DOCS / "pages" / "enemy.html"
    ).read_text(encoding="utf-8")

    gigantes = (
        DOCS / "pages" / "gigantes.html"
    ).read_text(encoding="utf-8")

    assert "<thead>" in enemy
    assert '<th scope="col">名前</th>' in enemy

    assert "<thead>" in gigantes
    assert '<th scope="col">種別</th>' in gigantes


def test_historical_classification_tree_is_not_part_of_public_build():
    config = CONFIG.read_text(encoding="utf-8")

    assert "exclude:" in config
    assert "- pages/分類中" in config


def test_agent_prohibits_legacy_table_compatibility():
    agent = AGENT.read_text(encoding="utf-8")

    assert (
        "Legacy table compatibility styling is prohibited."
        in agent
    )

    assert (
        "`docs/pages/分類中/` is historical staging/reference material"
        in agent
    )
