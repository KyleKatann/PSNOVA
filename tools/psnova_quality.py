from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

FULL_INTERVAL = 5
CADENCE_FILE = ROOT / ".git" / "psnova-quality-cadence"


def run(command):
    print()
    print(">", subprocess.list2cmdline(command))
    subprocess.run(command, cwd=ROOT, check=True)


def npx_command():
    if os.name == "nt":
        command = shutil.which("npx.cmd") or shutil.which("npx")
    else:
        command = shutil.which("npx")

    if not command:
        raise RuntimeError("npx was not found on PATH")

    return command


def run_fast():
    run(["git", "diff", "--check"])
    run([sys.executable, "-m", "pytest", "-q"])


def run_full_ui():
    run([
        npx_command(),
        "playwright",
        "test",
        "tests/ui/ui-health.spec.js",
    ])


def run_axe():
    run([
        npx_command(),
        "playwright",
        "test",
        "tests/ui/accessibility.spec.js",
        "--project=desktop-chromium",
    ])


def run_targeted_ui(project=None, grep=None):
    command = [
        npx_command(),
        "playwright",
        "test",
        "tests/ui/ui-health.spec.js",
    ]

    if project:
        command.append(f"--project={project}")

    if grep:
        command.extend(["--grep", grep])

    run(command)


def read_cadence():
    if not CADENCE_FILE.exists():
        return 0

    try:
        value = int(CADENCE_FILE.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return 0

    if 0 <= value < FULL_INTERVAL:
        return value

    return 0


def write_cadence(value):
    CADENCE_FILE.write_text(str(value), encoding="utf-8")


def finish_fix():
    run_fast()

    current = read_cadence()
    next_count = current + 1

    if next_count >= FULL_INTERVAL:
        print(
            f"\n=== {FULL_INTERVAL}/{FULL_INTERVAL}: "
            "running full Playwright UI health ==="
        )
        run_full_ui()
        write_cadence(0)
        print("\nPASS: cadence reset to 0/5")
        return

    write_cadence(next_count)

    print(
        f"\nPASS: Playwright cadence {next_count}/{FULL_INTERVAL}. "
        f"Full UI in {FULL_INTERVAL - next_count} fix(es)."
    )


class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.images = []
        self.links = []
        self.tables = []
        self.table_stack = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attributes = dict(attrs)

        self.tags.append((tag, attributes))

        if tag == "img":
            self.images.append(attributes)

        if tag == "link":
            self.links.append(attributes)

        if tag == "table":
            table = {
                "caption": False,
                "ths": [],
            }
            self.tables.append(table)
            self.table_stack.append(table)

        elif tag == "caption" and self.table_stack:
            self.table_stack[-1]["caption"] = True

        elif tag == "th" and self.table_stack:
            self.table_stack[-1]["ths"].append(attributes)

    def handle_endtag(self, tag):
        if tag.lower() == "table" and self.table_stack:
            self.table_stack.pop()


def public_html_files():
    for path in DOCS.rglob("*.html"):
        if "分類中" not in path.parts:
            yield path


def inventory():
    findings = {
        "skip_link": [],
        "main": [],
        "aside": [],
        "table_caption": [],
        "th_scope": [],
        "inline_style": [],
        "inline_script": [],
        "event_handler": [],
        "javascript_url": [],
        "http_url": [],
        "external_resource": [],
        "image_dimensions": [],
        "blocking_script": [],
        "favicon": [],
    }

    html_files = list(public_html_files())

    sidebar_source = (
        DOCS / "js" / "sidebar.js"
    ).read_text(encoding="utf-8")

    shared_sidebar_is_aside = (
        '<aside id="sub">' in sidebar_source
        and "</aside>" in sidebar_source
    )

    for path in html_files:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()

        parser = AuditParser()
        parser.feed(text)
        parser.close()

        tags = [tag for tag, _ in parser.tags]

        if not re.search(
            r'<a\b[^>]*href=["\']#(?:main|main-content)["\']',
            text,
            re.IGNORECASE,
        ):
            findings["skip_link"].append(rel)

        if "main" not in tags:
            findings["main"].append(rel)

        has_shared_sidebar_script = any(
            tag == "script"
            and (attrs.get("src") or "").strip()
            == "/PSNOVA/js/sidebar.js"
            for tag, attrs in parser.tags
        )

        has_shared_sidebar = (
            has_shared_sidebar_script
            and shared_sidebar_is_aside
        )

        if "aside" not in tags and not has_shared_sidebar:
            findings["aside"].append(rel)

        missing_caption = sum(
            1 for table in parser.tables
            if not table["caption"]
        )
        if missing_caption:
            findings["table_caption"].append(
                f"{rel}: {missing_caption}"
            )

        missing_scope = sum(
            1
            for table in parser.tables
            for th in table["ths"]
            if not (th.get("scope") or "").strip()
        )
        if missing_scope:
            findings["th_scope"].append(
                f"{rel}: {missing_scope}"
            )

        inline_style = sum(
            1
            for _, attrs in parser.tags
            if "style" in attrs
        )
        if inline_style:
            findings["inline_style"].append(
                f"{rel}: {inline_style}"
            )

        inline_script = len(
            re.findall(
                r"<script\b(?![^>]*\bsrc=)[^>]*>",
                text,
                re.IGNORECASE,
            )
        )
        if inline_script:
            findings["inline_script"].append(
                f"{rel}: {inline_script}"
            )

        event_handlers = sum(
            1
            for _, attrs in parser.tags
            for name in attrs
            if name.lower().startswith("on")
        )
        if event_handlers:
            findings["event_handler"].append(
                f"{rel}: {event_handlers}"
            )

        javascript_urls = sum(
            1
            for _, attrs in parser.tags
            for name in ("href", "src", "action")
            if (attrs.get(name) or "")
            .strip()
            .lower()
            .startswith("javascript:")
        )
        if javascript_urls:
            findings["javascript_url"].append(
                f"{rel}: {javascript_urls}"
            )

        http_urls = re.findall(
            r"(?:href|src|content)=[\"'](http://[^\"']+)[\"']",
            text,
            re.IGNORECASE,
        )
        for url in http_urls:
            findings["http_url"].append(
                f"{rel}: {url}"
            )

        for tag, attrs in parser.tags:
            url = ""

            if tag in {"img", "script"}:
                url = (attrs.get("src") or "").strip()

            elif tag == "link":
                rel_values = set(
                    (attrs.get("rel") or "").lower().split()
                )
                if "stylesheet" in rel_values:
                    url = (attrs.get("href") or "").strip()

            if not url:
                continue

            parts = urlsplit(url)

            if (
                parts.scheme in {"http", "https"}
                and parts.netloc
                and parts.netloc != "kylekatann.github.io"
            ):
                findings["external_resource"].append(
                    f"{rel}: {url}"
                )

        missing_dimensions = sum(
            1
            for image in parser.images
            if not image.get("width") or not image.get("height")
        )
        if missing_dimensions:
            findings["image_dimensions"].append(
                f"{rel}: {missing_dimensions}"
            )

        head = re.search(
            r"<head\b[^>]*>(.*?)</head>",
            text,
            re.IGNORECASE | re.DOTALL,
        )

        if head:
            blocking = re.findall(
                r"<script\b"
                r"(?=[^>]*\bsrc=)"
                r"(?![^>]*\bdefer\b)"
                r"(?![^>]*\basync\b)"
                r"(?![^>]*\btype=[\"']module[\"'])"
                r"[^>]*>",
                head.group(1),
                re.IGNORECASE,
            )

            if blocking:
                findings["blocking_script"].append(
                    f"{rel}: {len(blocking)}"
                )

        has_icon = False

        for link in parser.links:
            rel_values = set(
                (link.get("rel") or "").lower().split()
            )
            if "icon" in rel_values:
                has_icon = True
                break

        if not has_icon:
            findings["favicon"].append(rel)

    labels = {
        "skip_link": "Skip link missing",
        "main": "<main> missing",
        "aside": "<aside> missing",
        "table_caption": "Tables without caption",
        "th_scope": "TH without scope",
        "inline_style": "Inline style attributes",
        "inline_script": "Inline scripts",
        "event_handler": "Inline event handlers",
        "javascript_url": "javascript: URLs",
        "http_url": "Plain HTTP URLs",
        "external_resource": "External CSS/JS/image resources",
        "image_dimensions": "Images without width/height",
        "blocking_script": "Blocking head scripts",
        "favicon": "Favicon declaration missing",
    }

    print("\n=== PSNOVA QUALITY INVENTORY ===")

    for key, label in labels.items():
        values = findings[key]

        print(f"\n[{len(values):>3}] {label}")

        for value in values[:25]:
            print("   ", value)

        if len(values) > 25:
            print(f"    ... +{len(values) - 25} more")

    sitemap = DOCS / "sitemap.xml"

    if sitemap.exists():
        sitemap_text = sitemap.read_text(encoding="utf-8")

        sitemap_paths = {
            match.group(1) or "index.html"
            for match in re.finditer(
                r"<loc>"
                r"https://kylekatann\.github\.io/PSNOVA/"
                r"([^<]*)"
                r"</loc>",
                sitemap_text,
            )
        }

        public_paths = {
            path.relative_to(DOCS).as_posix()
            for path in html_files
        }

        missing = sorted(public_paths - sitemap_paths)
        stale = sorted(sitemap_paths - public_paths)

        print(
            f"\n[{len(missing):>3}] "
            "Public HTML missing from sitemap"
        )
        for value in missing[:30]:
            print("   ", value)

        print(
            f"\n[{len(stale):>3}] "
            "Sitemap entries without public HTML"
        )
        for value in stale[:30]:
            print("   ", value)

    print("\nDynamic audits still planned:")
    for item in (
        "keyboard-only traversal",
        "focus order and visibility",
        "200% / 400% zoom and reflow",
        "touch target sizing",
        "prefers-reduced-motion",
        "runtime game-text immutability",
        "runtime table-structure immutability",
        "runtime DOM mutation allow-list",
        "page-weight budget",
        "dead / duplicate CSS",
    ):
        print("  -", item)


def show_status():
    count = read_cadence()

    print(f"Playwright cadence: {count}/{FULL_INTERVAL}")
    print(
        "Full UI health in "
        f"{FULL_INTERVAL - count} completed fix(es)."
    )


def reset_cadence():
    write_cadence(0)
    print("Playwright cadence reset to 0/5")


def main():
    parser = argparse.ArgumentParser(
        description="PSNOVA quality gate"
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    sub.add_parser("fast")
    sub.add_parser("finish")
    sub.add_parser("full")
    sub.add_parser("axe")
    sub.add_parser("inventory")
    sub.add_parser("status")
    sub.add_parser("reset")

    targeted = sub.add_parser("targeted")

    targeted.add_argument(
        "--project",
        choices=(
            "desktop-chromium",
            "mobile-chromium",
            "desktop-site-touch",
        ),
    )

    targeted.add_argument(
        "--grep",
    )

    args = parser.parse_args()

    if args.command == "fast":
        run_fast()

    elif args.command == "finish":
        finish_fix()

    elif args.command == "full":
        run_fast()
        run_full_ui()

    elif args.command == "axe":
        run_axe()

    elif args.command == "targeted":
        run_fast()
        run_targeted_ui(
            project=args.project,
            grep=args.grep,
        )

    elif args.command == "inventory":
        inventory()

    elif args.command == "status":
        show_status()

    elif args.command == "reset":
        reset_cadence()


if __name__ == "__main__":
    main()