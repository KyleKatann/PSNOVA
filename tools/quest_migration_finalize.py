from __future__ import annotations

from html import escape

from bs4 import BeautifulSoup

import quest_migrate as qm


def source_pairs(config: qm.PageConfig) -> list[tuple[str, str]]:
    soup = BeautifulSoup((qm.SOURCE_DIR / config.source).read_text(encoding="utf-8"), "html.parser")
    start = qm.find_body_start(soup)
    pairs: list[tuple[str, str]] = []
    for node in qm.iter_article_nodes(start):
        if node is start or node.name not in {"h3", "h4"}:
            continue
        table = qm.quest_table_after(node)
        if table is None:
            continue
        heading = qm.heading_text(node)
        table_name = str(qm.parse_quest(table)["name"])
        pairs.append((heading, table_name))
    return pairs


def replace_after(text: str, needle: str, replacement: str, start: int) -> tuple[str, int]:
    index = text.find(needle, start)
    if index < 0:
        raise RuntimeError(f"generated quest fragment not found: {needle}")
    text = text[:index] + replacement + text[index + len(needle):]
    return text, index + len(replacement)


def finalize(config: qm.PageConfig) -> int:
    path = qm.DEST_DIR / config.dest
    text = path.read_text(encoding="utf-8")
    cursor = 0
    changed = 0

    for heading, table_name in source_pairs(config):
        current_name = table_name
        expected_name = escape(heading)
        current_heading = f"<h4>{current_name}</h4>"
        expected_heading = f"<h4>{expected_name}</h4>"
        text, cursor = replace_after(text, current_heading, expected_heading, cursor)

        current_cell = f"<td>{current_name}</td>"
        expected_cell = f"<td>{expected_name}</td>"
        text, cursor = replace_after(text, current_cell, expected_cell, cursor)

        if current_name != expected_name:
            changed += 1

    path.write_text(text, encoding="utf-8", newline="\n")
    return changed


def main() -> None:
    total = 0
    for config in qm.PAGES:
        changed = finalize(config)
        print(f"{config.dest}: corrected {changed} quest names")
        total += changed
    print(f"corrected total: {total}")


if __name__ == "__main__":
    main()
