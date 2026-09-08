import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "pages" / "promise-order.html"
DETAIL_DIR = ROOT / "docs" / "pages" / "promise-order"
SIDEBAR = ROOT / "docs" / "js" / "sidebar.js"
SITEMAP = ROOT / "docs" / "sitemap.xml"

PAGES = {
    "fildia": ("フィルディア", 16, "アイテムショップ建設", "コスチュームショップ改築"),
    "lutina": ("ルティナ", 22, "ルティナの訓練", "お風呂の思い出"),
    "sail": ("セイル", 22, "セイルの訓練", "究極の鉱物・グラン水源"),
    "izuna": ("イズナ", 21, "イズナの訓練", "究極の資材・大尖塔"),
    "lithia": ("リーティア", 19, "状態異常訓練", "対ダーカー侵食薬研究"),
    "kisara": ("キサラ", 25, "ブーストエネミー撃破訓練", "究極の資材・古代都市"),
    "orcuss": ("オルクス", 21, "スキルボード拡張", "究極ギガンテス討伐"),
    "yomi": ("ヨミ", 19, "部位破壊訓練", "究極のギガンテス素材"),
    "callisto": ("カリスト", 19, "グラン器片の入手", "超一流の仕事"),
    "hyperion": ("ヒュペリオン", 20, "岩塩の調達", "XHエネミーの食材研究"),
    "sharon": ("シャロン", 20, "バスターの訓練", "至高の鉱物資源2"),
}

EXPECTED_HEADERS = (
    "オーダー内容",
    "達成条件",
    "達成報酬",
    "グランエナジー",
    "経験値",
    "発生条件",
    "備考",
)


def tbody_row_count(page):
    tbody = re.search(r"<tbody>(.*?)</tbody>", page, re.S)
    assert tbody, "tbodyがない"
    return len(re.findall(r"<tr>", tbody.group(1)))


def test_promise_order_index_preserves_general_mechanics_and_links():
    page = INDEX.read_text(encoding="utf-8")

    assert "回数制限の無いプロミスオーダーは、クエストをどれでもいいので3回クリアすると復活する。" in page
    assert "パーティーメンバーにとどめをさされると達成されない。" in page

    for slug, (name, count, _, _) in PAGES.items():
        assert f'href="/PSNOVA/pages/promise-order/{slug}.html"' in page
        assert name in page
        assert f"<td>{count}</td>" in page


def test_promise_order_detail_pages_preserve_all_224_rows():
    total = 0

    for slug, (name, expected_count, first_order, last_order) in PAGES.items():
        page = (DETAIL_DIR / f"{slug}.html").read_text(encoding="utf-8")

        assert f"<title>PSNOVA攻略サイト - {name}のプロミスオーダー</title>" in page
        assert f'<link rel="canonical" href="https://kylekatann.github.io/PSNOVA/pages/promise-order/{slug}.html">' in page
        assert '<main id="main">' in page
        assert '<div class="table-scroll">' in page
        assert first_order in page
        assert last_order in page

        for header in EXPECTED_HEADERS:
            assert f'<th scope="col">{header}</th>' in page

        assert "web.archive.org" not in page
        assert "paraedit" not in page
        assert "表を編集" not in page
        assert "行を追加" not in page
        assert "[image]" not in page

        count = tbody_row_count(page)
        assert count == expected_count, f"{name}: {expected_count}件を期待したが{count}件だった"
        total += count

    assert total == 224


def test_promise_order_important_unlocks_and_repeat_rules_are_preserved():
    kisara = (DETAIL_DIR / "kisara.html").read_text(encoding="utf-8")
    yomi = (DETAIL_DIR / "yomi.html").read_text(encoding="utf-8")
    orcuss = (DETAIL_DIR / "orcuss.html").read_text(encoding="utf-8")
    lithia = (DETAIL_DIR / "lithia.html").read_text(encoding="utf-8")
    sharon = (DETAIL_DIR / "sharon.html").read_text(encoding="utf-8")

    assert "クエスト1回クリアで<br>再受注可能" in kisara
    assert "武器エクステンドが<br>可能になる" in yomi
    assert "難易度SH開放" in orcuss
    assert "難易度XH開放" in orcuss
    assert "再キャラクタークリエイトが<br>可能になる" in lithia
    assert "リーティアがクエストに<br>同行可能になる" in lithia
    assert "施設「コア製錬所」追加" in sharon


def test_promise_order_pages_are_registered_in_navigation_and_sitemap():
    sidebar = SIDEBAR.read_text(encoding="utf-8")
    sitemap = SITEMAP.read_text(encoding="utf-8")

    assert '<a href="/PSNOVA/pages/promise-order.html">プロミスオーダー</a>' in sidebar
    assert "var promiseOrderChild =" in sidebar
    assert 'linkPath === "/PSNOVA/pages/promise-order.html"' in sidebar
    assert "https://kylekatann.github.io/PSNOVA/pages/promise-order.html" in sitemap

    for slug in PAGES:
        assert f"https://kylekatann.github.io/PSNOVA/pages/promise-order/{slug}.html" in sitemap
