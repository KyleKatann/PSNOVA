from __future__ import annotations

from html import escape
from pathlib import Path
import re

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "reference/psnovanet/psnova/コールドスリープ - ファンタシースターノヴァ PSNOVA 攻略Wiki.html"
OUTPUT = ROOT / "docs/pages/npc-coldsleep.html"

HEADERS = ["名前", "種族", "性別", "クラス", "スタイル", "特徴", "コメント", "備考"]
COLS = [
    "npc-col-name", "npc-col-species", "npc-col-sex", "npc-col-class",
    "npc-col-style", "npc-col-feature", "npc-col-join", "npc-col-effect",
]


def lines(node: Tag) -> list[str]:
    text = node.get_text("\n", strip=True)
    return [re.sub(r"\s+", " ", part).strip() for part in text.splitlines() if part.strip()]


def text_html(node: Tag) -> str:
    return "<br>\n".join(escape(part) for part in lines(node))


def clean_heading(node: Tag) -> str:
    clone = BeautifulSoup(str(node), "html.parser")
    for a in clone.find_all("a"):
        a.decompose()
    return re.sub(r"\s+", " ", clone.get_text(" ", strip=True)).strip()


def source_rows(table: Tag) -> list[tuple[str, ...]]:
    tbody = table.find("tbody")
    if not tbody:
        return []
    rows: list[tuple[str, ...]] = []
    for tr in tbody.find_all("tr", recursive=False):
        cells = tr.find_all(["td", "th"], recursive=False)[:8]
        if len(cells) != 8:
            continue
        rows.append(tuple("\n".join(lines(cell)) for cell in cells))
    return rows


def render_table(table: Tag) -> str:
    rows = source_rows(table)
    out = [
        '                    <div class="table-scroll">',
        '                        <table class="npc-table">',
        '                            <colgroup>',
    ]
    out.extend(f'                                <col class="{cls}">' for cls in COLS)
    out.extend([
        '                            </colgroup>',
        '                            <thead>',
        '                                <tr>',
    ])
    out.extend(f'                                    <th scope="col">{escape(header)}</th>' for header in HEADERS)
    out.extend([
        '                                </tr>',
        '                            </thead>',
        '                            <tbody>',
    ])
    for row in rows:
        out.append('                                <tr>')
        for index, value in enumerate(row):
            cls = ' class="npc-prose"' if index in (5, 6, 7) else ""
            cell = "<br>\n                                        ".join(escape(part) for part in value.split("\n"))
            out.append(f'                                    <td{cls}>{cell}</td>')
        out.append('                                </tr>')
    out.extend([
        '                            </tbody>',
        '                        </table>',
        '                    </div>',
    ])
    return "\n".join(out)


def direct_siblings_between(start: Tag, end: Tag | None):
    node = start.next_sibling
    while node is not None and node is not end:
        yield node
        node = node.next_sibling


def first_table_before_next_heading(heading: Tag, next_heading: Tag | None) -> Tag | None:
    for node in direct_siblings_between(heading, next_heading):
        if isinstance(node, Tag):
            if node.name == "table" and "style_table" in node.get("class", []):
                return node
            table = node.find("table", class_="style_table")
            if table:
                return table
    return None


def render_info_nodes(heading: Tag, next_heading: Tag | None, stop_at_table: bool = True) -> list[str]:
    rendered: list[str] = []
    for node in direct_siblings_between(heading, next_heading):
        if not isinstance(node, Tag):
            continue
        if node.find("table", class_="style_table") or (node.name == "table" and "style_table" in node.get("class", [])):
            if stop_at_table:
                break
            continue
        if node.name == "p":
            value = text_html(node).replace("ネタバレ注意。", "").strip()
            if value:
                rendered.append(f'                    <p>{value}</p>')
        elif node.name in ("ul", "ol"):
            tag = node.name
            rendered.append(f'                    <{tag}>')
            for li in node.find_all("li", recursive=False):
                value = text_html(li).replace("ネタバレ注意。", "").strip()
                if value:
                    rendered.append(f'                        <li>{value}</li>')
            rendered.append(f'                    </{tag}>')
    return rendered


def render_facility_section(heading: Tag, next_heading: Tag | None) -> tuple[list[str], list[Tag]]:
    out = [f'                    <h3>{escape(clean_heading(heading))}</h3>']
    tables: list[Tag] = []
    for node in direct_siblings_between(heading, next_heading):
        if not isinstance(node, Tag):
            continue
        if node.name == "p":
            value = text_html(node)
            if value:
                out.append(f'                    <p>{value}</p>')
        elif "plugin_fold_title_plus" in node.get("class", []):
            title = re.sub(r"\s+", " ", node.get_text(" ", strip=True)).strip()
            body = node.find_next_sibling("div", class_="plugin_fold_body")
            if title and body:
                table = body.find("table", class_="style_table")
                if table:
                    out.append(f'                    <h4>{escape(title)}</h4>')
                    out.append(render_table(table))
                    tables.append(table)
    return out, tables


def modern_shell(body: str) -> str:
    return f'''<!doctype html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>PSNOVA攻略サイト - コールドスリープ</title>
    <meta name="description" content="PSNOVAのコールドスリープで解凍できるクルーを一覧掲載。解凍条件、費用、コンプリートボーナス、各クルーの種族・クラス・特徴・施設スキルを確認できます。">
    <link rel="canonical" href="https://kylekatann.github.io/PSNOVA/pages/npc-coldsleep.html">
    <meta property="og:title" content="PSNOVA攻略サイト - コールドスリープ">
    <meta property="og:description" content="PSNOVAのコールドスリープで解凍できるクルーを一覧掲載。解凍条件、費用、コンプリートボーナス、各クルーの種族・クラス・特徴・施設スキルを確認できます。">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://kylekatann.github.io/PSNOVA/pages/npc-coldsleep.html">
    <meta property="og:image" content="https://kylekatann.github.io/PSNOVA/img/logo.png">
    <meta property="og:image:alt" content="PSNOVA 攻略サイト">
    <meta property="og:site_name" content="PSNOVA攻略サイト">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="/PSNOVA/img/logo.png" type="image/png">
    <link rel="stylesheet" href="/PSNOVA/css/style.css">
    <link rel="stylesheet" href="/PSNOVA/css/page.css">
    <script defer src="/PSNOVA/js/openclose.js"></script>
    <script defer src="/PSNOVA/js/fixmenu_pagetop.js"></script>
    <script defer src="/PSNOVA/js/menubar.js"></script>
    <script defer src="/PSNOVA/js/sidebar.js"></script>
</head>
<body class="guide-page">
    <a class="skip-link" href="#main">本文へスキップ</a>
    <div id="container">
        <header>
            <h1 id="logo"><a href="/PSNOVA/"><img src="/PSNOVA/img/logo.png" alt="PSNOVA 攻略サイト" width="676" height="100"></a></h1>
        </header>
        <div id="contents">
            <main id="main">
                <section>
                    <h2>コールドスリープ</h2>
                    <p class="page-lead">コールドスリープカウンターから「カプセル解凍」を選ぶとクルーを解凍できる。キャラクター性能が良いクルーが出る時は警音と赤ランプの明滅が起こり、能力が良いクルーは赤色、特に優れたクルーは虹色のカプセルで出現する。各クルーの種族、クラス、スタイル、特徴、コメント、備考と、解凍費用・条件・コンプリートボーナスを一覧で確認できる。</p>
{body}
                </section>
            </main>
        </div>
        <footer>
            <small>Copyright&copy; <a href="/PSNOVA/">PSNOVA 攻略サイト</a> All Rights Reserved.</small>
        </footer>
    </div>
    <p class="nav-fix-pos-pagetop"><a href="#">↑</a></p>
    <button type="button" id="menubar_hdr" class="close"></button>
</body>
</html>
'''


def main() -> None:
    soup = BeautifulSoup(SOURCE.read_text(encoding="utf-8", errors="replace"), "html.parser")
    headings = []
    for index in range(1, 19):
        heading = soup.find("h3", id=f"content_1_{index}")
        if heading is None:
            raise SystemExit(f"missing source section content_1_{index}")
        headings.append(heading)

    body: list[str] = []
    migrated_tables: list[Tag] = []
    for index, heading in enumerate(headings):
        next_heading = soup.find("h3", id=f"content_1_{index + 2}") if index < 17 else soup.find("h3", id="content_1_19")
        if heading.get("id") == "content_1_18":
            section, tables = render_facility_section(heading, next_heading)
            body.extend(section)
            migrated_tables.extend(tables)
            continue
        body.append(f'                    <h3>{escape(clean_heading(heading))}</h3>')
        body.extend(render_info_nodes(heading, next_heading))
        table = first_table_before_next_heading(heading, next_heading)
        if table is None:
            raise SystemExit(f"missing table for {heading.get('id')}")
        body.append(render_table(table))
        migrated_tables.append(table)

    output = modern_shell("\n".join(body))
    OUTPUT.write_text(output, encoding="utf-8", newline="\n")

    generated = BeautifulSoup(output, "html.parser")
    generated_tables = generated.select("table.npc-table")
    if len(generated_tables) != len(migrated_tables):
        raise SystemExit(f"table count mismatch: {len(migrated_tables)} -> {len(generated_tables)}")
    expected_rows = [source_rows(table) for table in migrated_tables]
    actual_rows = [source_rows(table) for table in generated_tables]
    if expected_rows != actual_rows:
        raise SystemExit("source/public table row mismatch")

    forbidden = ["<iframe", "<object", "<embed", "web.archive.org", "cmd=table_edit2", "cmd=secedit", "旧Wiki", "アーカイブ"]
    lowered = output.lower()
    for token in forbidden:
        if token.lower() in lowered:
            raise SystemExit(f"forbidden public token: {token}")
    print(f"migrated {len(migrated_tables)} tables / {sum(len(rows) for rows in expected_rows)} rows")


if __name__ == "__main__":
    main()
