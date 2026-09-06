from __future__ import annotations

from bs4 import BeautifulSoup

import quest_migrate as qm


def main() -> None:
    mismatches = []
    for config in qm.PAGES:
        soup = BeautifulSoup((qm.SOURCE_DIR / config.source).read_text(encoding="utf-8"), "html.parser")
        start = qm.find_body_start(soup)
        for node in qm.iter_article_nodes(start):
            if node is start or node.name not in {"h3", "h4"}:
                continue
            table = qm.quest_table_after(node)
            if table is None:
                continue
            heading = qm.heading_text(node)
            table_name = str(qm.parse_quest(table)["name"]).replace("<br>", " / ")
            if heading != table_name:
                mismatches.append((config.dest, heading, table_name))

    for filename, heading, table_name in mismatches:
        print(f"{filename}: heading={heading!r} table={table_name!r}")
    print(f"mismatches: {len(mismatches)}")


if __name__ == "__main__":
    main()
