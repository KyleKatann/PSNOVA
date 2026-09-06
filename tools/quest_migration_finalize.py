from __future__ import annotations

from html import escape

from bs4 import BeautifulSoup, Tag

import quest_migrate as qm


def source_quest_names(config: qm.PageConfig) -> list[str]:
    soup = BeautifulSoup((qm.SOURCE_DIR / config.source).read_text(encoding="utf-8"), "html.parser")
    start = qm.find_body_start(soup)
    names: list[str] = []
    for node in qm.iter_article_nodes(start):
        if node is start or node.name not in {"h3", "h4"}:
            continue
        if qm.quest_table_after(node) is None:
            continue
        names.append(qm.heading_text(node))
    return names


def finalize(config: qm.PageConfig) -> int:
    path = qm.DEST_DIR / config.dest
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    names = source_quest_names(config)
    headings = soup.select("#main h4")
    tables = soup.select("#main h4 + table")
    if len(headings) != len(names) or len(tables) != len(names):
        raise RuntimeError(
            f"quest count mismatch for {config.dest}: names={len(names)} headings={len(headings)} tables={len(tables)}"
        )

    changed = 0
    for heading, table, name in zip(headings, tables, names):
        current_heading = " ".join(heading.get_text(" ", strip=True).split())
        first_cell = table.select_one("tbody tr td")
        if not isinstance(first_cell, Tag):
            raise RuntimeError(f"missing quest-name cell in {config.dest}: {name}")
        current_cell = " ".join(first_cell.get_text(" ", strip=True).split())
        if current_heading != name or current_cell != name:
            heading.clear()
            heading.append(name)
            first_cell.clear()
            first_cell.append(name)
            changed += 1

    rendered = str(soup)
    rendered = rendered.replace("<html lang=\"ja\">", '<html lang="ja">', 1)
    rendered = rendered.replace("<!DOCTYPE html>", "<!doctype html>", 1)
    path.write_text(rendered + ("\n" if not rendered.endswith("\n") else ""), encoding="utf-8", newline="\n")
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
