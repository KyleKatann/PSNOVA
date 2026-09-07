from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path

from bs4 import BeautifulSoup, Tag


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "docs" / "pages" / "分類中" / "!quest工事中excelが土方"
DEST_DIR = ROOT / "docs" / "pages" / "quest"


@dataclass(frozen=True)
class PageConfig:
    source: str
    dest: str
    title: str
    description: str
    lead: str


PAGES = (
    PageConfig(
        "鋼の荒野 - ファンタシースターノヴァ PSNOVA 攻略Wiki.html",
        "steel-wilderness.html",
        "鋼の荒野",
        "PSNOVAの鋼の荒野で受注できるクエストについて、同行者、クリア・失敗条件、難易度、敵レベル、出現エネミー、攻略情報を確認できます。",
        "鋼の荒野で受注できるクエストをエリア区分ごとにまとめる。同行者、クリア条件、失敗条件、難易度、敵レベル、出現エネミーまで確認できる。各任務の条件や攻略上の注意点を確認するときに利用できる。",
    ),
    PageConfig(
        "グラン水源 - ファンタシースターノヴァ PSNOVA 攻略Wiki.html",
        "gran-water-source.html",
        "グラン水源",
        "PSNOVAのグラン水源で受注できるクエストについて、同行者、クリア・失敗条件、難易度、敵レベル、出現エネミー、攻略情報を確認できます。",
        "グラン水源で受注できるクエストをエリア区分ごとにまとめる。同行者、クリア条件、失敗条件、難易度、敵レベル、出現エネミーまで確認できる。各任務の条件や攻略上の注意点を確認するときに利用できる。",
    ),
    PageConfig(
        "炎の高地 - ファンタシースターノヴァ PSNOVA 攻略Wiki.html",
        "flame-highlands.html",
        "炎の高地",
        "PSNOVAの炎の高地で受注できるクエストについて、同行者、クリア・失敗条件、難易度、敵レベル、出現エネミー、攻略情報を確認できます。",
        "炎の高地で受注できるクエストをエリア区分ごとにまとめる。同行者、クリア条件、失敗条件、難易度、敵レベル、出現エネミーまで確認できる。各任務の条件や攻略上の注意点を確認するときに利用できる。",
    ),
    PageConfig(
        "古代都市 - ファンタシースターノヴァ PSNOVA 攻略Wiki.html",
        "ancient-city.html",
        "古代都市",
        "PSNOVAの古代都市で受注できるクエストについて、同行者、クリア・失敗条件、難易度、敵レベル、出現エネミー、攻略情報を確認できます。",
        "古代都市で受注できるクエストをエリア区分ごとにまとめる。同行者、クリア条件、失敗条件、難易度、敵レベル、出現エネミーまで確認できる。各任務の条件や攻略上の注意点を確認するときに利用できる。",
    ),
    PageConfig(
        "ノヴァ内部 - ファンタシースターノヴァ PSNOVA 攻略Wiki.html",
        "nova-interior.html",
        "ノヴァ内部",
        "PSNOVAのノヴァ内部で受注できるクエストについて、同行者、クリア・失敗条件、難易度、敵レベル、出現エネミー、攻略情報を確認できます。",
        "ノヴァ内部で受注できるクエストをまとめる。同行者、クリア条件、失敗条件、難易度、敵レベル、出現エネミーまで確認できる。各任務の条件や攻略上の注意点を確認するときに利用できる。",
    ),
    PageConfig(
        "追加クエスト - ファンタシースターノヴァ PSNOVA 攻略Wiki.html",
        "additional.html",
        "追加クエスト",
        "PSNOVAのバージョンアップやDLCで追加されたクエストについて、同行者、クリア・失敗条件、難易度、敵レベル、出現エネミー、攻略情報を確認できます。",
        "バージョンアップやダウンロードコンテンツで追加されたクエストをまとめる。無料・有料の区分に加え、クリア条件、失敗条件、難易度、敵レベル、出現エネミーまで確認できる。追加任務の条件や攻略上の注意点を確認するときに利用できる。",
    ),
)


def heading_text(tag: Tag) -> str:
    clone = BeautifulSoup(str(tag), "html.parser")
    for node in clone.select("a.anchor_super"):
        node.decompose()
    return " ".join(clone.get_text(" ", strip=True).split())


def text_fragment(tag: Tag | None) -> str:
    if tag is None:
        return ""
    clone = BeautifulSoup(str(tag), "html.parser")
    for node in clone.find_all("img"):
        node.decompose()
    for node in clone.find_all("a"):
        node.unwrap()
    for node in clone.find_all("br"):
        node.replace_with("\n")
    lines = [" ".join(line.split()) for line in clone.get_text("\n").splitlines()]
    lines = [line for line in lines if line]
    return "<br>".join(escape(line) for line in lines)


def plain_text(tag: Tag | None) -> str:
    if tag is None:
        return ""
    clone = BeautifulSoup(str(tag), "html.parser")
    for node in clone.select("a.anchor_super, img"):
        node.decompose()
    return " ".join(clone.get_text(" ", strip=True).split())


def find_body_start(soup: BeautifulSoup) -> Tag:
    start = soup.find(id="content_1_0")
    if not isinstance(start, Tag):
        raise RuntimeError("main article start not found")
    return start


def iter_article_nodes(start: Tag):
    node = start
    while node is not None:
        if isinstance(node, Tag):
            if node.name in {"h2", "h3", "h4"} and heading_text(node).startswith("コメント"):
                break
            yield node
        node = node.next_sibling


def quest_table_after(heading: Tag) -> Tag | None:
    node = heading.next_sibling
    while node is not None:
        if isinstance(node, Tag) and node.name in {"h2", "h3", "h4"}:
            return None
        if isinstance(node, Tag) and node.name == "div" and "ie5" in (node.get("class") or []):
            table = node.find("table")
            return table if isinstance(table, Tag) else None
        node = node.next_sibling
    return None


def strategy_after(table: Tag) -> str:
    wrapper = table.parent
    node = wrapper.next_sibling if isinstance(wrapper, Tag) else None
    while node is not None:
        if isinstance(node, Tag) and node.name in {"h2", "h3", "h4"}:
            return ""
        if isinstance(node, Tag) and node.name in {"ul", "p"}:
            text = plain_text(node)
            if text.startswith("攻略"):
                strategy = text[len("攻略"):].lstrip()
                if strategy.startswith(("：", ":")):
                    return strategy[1:].strip()
                return ""
        node = node.next_sibling
    return ""


def parse_quest(table: Tag) -> dict[str, object]:
    body = table.find("tbody")
    rows = body.find_all("tr", recursive=False) if isinstance(body, Tag) else table.find_all("tr", recursive=False)
    if len(rows) < 4:
        raise RuntimeError("unexpected quest table shape")

    identity_cells = rows[1].find_all(["td", "th"], recursive=False)
    identity = [text_fragment(cell) for cell in identity_cells[:4]]
    while len(identity) < 4:
        identity.append("")

    enemy_html = ""
    difficulties: list[tuple[str, str]] = []
    for row in rows[3:]:
        cells = row.find_all(["td", "th"], recursive=False)
        if not cells:
            continue
        difficulty = text_fragment(cells[0])
        level = text_fragment(cells[1]) if len(cells) > 1 else ""
        if len(cells) > 2:
            candidate = text_fragment(cells[2])
            if candidate:
                enemy_html = candidate
        if difficulty:
            difficulties.append((difficulty, level))

    return {
        "name": identity[0],
        "companion": identity[1],
        "clear": identity[2],
        "fail": identity[3],
        "difficulties": difficulties,
        "enemies": enemy_html,
    }


def quest_markup(data: dict[str, object], strategy: str) -> str:
    difficulties = data["difficulties"]
    difficulty_html = "<br>".join(f"{d} / {level}" if level else d for d, level in difficulties)
    strategy_markup = (
        f'                    <p><strong>攻略:</strong> {escape(strategy)}</p>\n'
        if strategy
        else ""
    )
    return f'''                    <h4>{data["name"]}</h4>
                    <table>
                        <thead>
                            <tr>
                                <th scope="col">クエスト名</th>
                                <th scope="col">同行者</th>
                                <th scope="col">クリア条件</th>
                                <th scope="col">失敗条件</th>
                                <th scope="col">難易度 / 敵レベル</th>
                                <th scope="col">エネミー</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>{data["name"]}</td>
                                <td>{data["companion"] or "-"}</td>
                                <td>{data["clear"] or "-"}</td>
                                <td>{data["fail"] or "-"}</td>
                                <td>{difficulty_html or "-"}</td>
                                <td>{data["enemies"] or "-"}</td>
                            </tr>
                        </tbody>
                    </table>
{strategy_markup}'''


def overview_markup(start: Tag) -> str:
    parts: list[str] = []
    node = start.next_sibling
    while node is not None:
        if isinstance(node, Tag) and node.name in {"h2", "h3", "h4"}:
            break
        if isinstance(node, Tag) and node.name == "p":
            text = text_fragment(node)
            if text:
                parts.append(f"                    <p>{text}</p>\n")
        node = node.next_sibling
    return "".join(parts)


def build_page(config: PageConfig) -> tuple[str, int]:
    source_path = SOURCE_DIR / config.source
    soup = BeautifulSoup(source_path.read_text(encoding="utf-8"), "html.parser")
    start = find_body_start(soup)
    body: list[str] = ["                    <h3>概要</h3>\n", overview_markup(start)]
    quest_count = 0

    for node in iter_article_nodes(start):
        if node is start or node.name not in {"h2", "h3", "h4"}:
            continue
        title = heading_text(node)
        if not title or title == "概要":
            continue
        if node.name == "h2":
            body.append(f"                    <h3>{escape(title)}</h3>\n")
            continue
        table = quest_table_after(node)
        if table is None:
            continue
        data = parse_quest(table)
        if not data["name"]:
            data["name"] = escape(title)
        body.append(quest_markup(data, strategy_after(table)))
        quest_count += 1

    canonical = f"https://kylekatann.github.io/PSNOVA/pages/quest/{config.dest}"
    page = f'''<!doctype html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>PSNOVA攻略サイト - {config.title}</title>
    <meta name="description" content="{config.description}">
    <link rel="canonical" href="{canonical}">
    <meta property="og:title" content="PSNOVA攻略サイト - {config.title}">
    <meta property="og:description" content="{config.description}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="https://kylekatann.github.io/PSNOVA/img/logo.png">
    <meta property="og:image:alt" content="PSNOVA 攻略サイト">
    <meta property="og:site_name" content="PSNOVA攻略サイト">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="/PSNOVA/img/logo.png" type="image/png">
    <link rel="stylesheet" href="/PSNOVA/css/style.css">
    <link rel="stylesheet" href="/PSNOVA/css/page.css">
    <script defer src="/PSNOVA/js/openclose.js"></script>
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
                    <h2>{config.title}</h2>
                    <p class="page-lead">{config.lead}</p>

{''.join(body)}                </section>
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
    return page, quest_count


def main() -> None:
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    total = 0
    for config in PAGES:
        page, count = build_page(config)
        (DEST_DIR / config.dest).write_text(page, encoding="utf-8", newline="\n")
        print(f"{config.dest}: {count} quests")
        total += count
    if total < 40:
        raise RuntimeError(f"too few quests migrated: {total}")
    print(f"total: {total} quests")


if __name__ == "__main__":
    main()
