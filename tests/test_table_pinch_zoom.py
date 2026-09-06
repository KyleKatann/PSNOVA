import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TABLE_JS = ROOT / "docs" / "js" / "menubar.js"
DOCS = ROOT / "docs"


def test_table_scrollers_allow_native_pinch_zoom():
    js = TABLE_JS.read_text(encoding="utf-8")

    assert 'wrapper.style.touchAction = "pan-x pan-y pinch-zoom";' in js


def test_public_viewports_do_not_disable_user_zoom():
    for path in DOCS.rglob("*.html"):
        if "分類中" in path.parts:
            continue

        text = path.read_text(encoding="utf-8")
        match = re.search(r'<meta\s+name="viewport"\s+content="([^"]+)"', text)
        if not match:
            continue

        viewport = match.group(1).replace(" ", "").lower()
        assert "user-scalable=no" not in viewport, path
        assert "user-scalable=0" not in viewport, path
        assert "maximum-scale=1" not in viewport, path
