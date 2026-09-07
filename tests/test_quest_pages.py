from pathlib import Path

from bs4 import BeautifulSoup

from tools import quest_migrate


ROOT = Path(__file__).resolve().parents[1]
QUEST_PAGES = {
    "steel-wilderness.html": ("鋼の荒野", "仲間の探索", "極:伏す猛銃と天舞う砲凰", 29),
    "gran-water-source.html": ("グラン水源", "ヨミの要求", "超：氷塊のギガティオン", 25),
    "flame-highlands.html": ("炎の高地", "リーティアのお願い", "極:棘と大火球の輪舞曲", 16),
    "ancient-city.html": ("古代都市", "静かなる都市", "極:漆黒の鉄馬と光線獣", 16),
    "nova-interior.html": ("ノヴァ内部", "果たすべき使命", "極:魂の解放", 9),
    "additional.html": ("追加クエスト", "タイムアタック・鋼の荒野", "経験値フィーバー", 9),
}


def page_text(filename: str) -> str:
    return (ROOT / "docs" / "pages" / "quest" / filename).read_text(encoding="utf-8")


def test_quest_pages_use_public_site_shell():
    scripts = (
        "/PSNOVA/js/openclose.js",
        "/PSNOVA/js/menubar.js",
        "/PSNOVA/js/sidebar.js",
    )

    for filename, (title, _, _, _) in QUEST_PAGES.items():
        html = page_text(filename)
        assert html.count('<main id="main">') == 1
        assert '<a class="skip-link" href="#main">本文へスキップ</a>' in html
        assert f"<title>PSNOVA攻略サイト - {title}</title>" in html
        assert f"<h2>{title}</h2>" in html
        assert '<p class="page-lead">' in html
        assert '/PSNOVA/img/logo.png' in html
        for script in scripts:
            assert f'<script defer src="{script}"></script>' in html


def test_quest_pages_strip_historical_site_chrome():
    forbidden = (
        "web.archive.org",
        "?cmd=",
        "adsbygoogle",
        "anchor_super",
        "paraedit.png",
        "mini_add.png",
        "Wayback",
    )

    for filename in QUEST_PAGES:
        html = page_text(filename)
        for token in forbidden:
            assert token not in html


def test_quest_pages_keep_quest_group_sentinels():
    for filename, (title, first_quest, last_quest, _) in QUEST_PAGES.items():
        html = page_text(filename)
        assert title in html
        assert first_quest in html
        assert last_quest in html
        assert "クエスト名" in html


def test_quest_pages_preserve_full_detail_fields_and_counts():
    required_headers = (
        "同行者",
        "クリア条件",
        "失敗条件",
        "難易度 / 敵レベル",
        "エネミー",
    )

    total = 0
    for filename, (_, _, _, expected_count) in QUEST_PAGES.items():
        html = page_text(filename)
        assert html.count("<h4>") == expected_count
        assert html.count("<table>") == expected_count
        for header in required_headers:
            assert header in html
        total += expected_count

    assert total == 104


def test_quest_pages_omit_empty_strategy_placeholders():
    for filename in QUEST_PAGES:
        assert "<strong>攻略:</strong> -" not in page_text(filename)


def test_quest_pages_match_source_migration_content():
    configs = {config.dest: config for config in quest_migrate.PAGES}

    for filename, (_, _, _, expected_count) in QUEST_PAGES.items():
        generated, source_count = quest_migrate.build_page(configs[filename])
        public = page_text(filename)

        assert source_count == expected_count

        generated_soup = BeautifulSoup(generated, "html.parser")
        public_soup = BeautifulSoup(public, "html.parser")

        generated_headings = generated_soup.select("h4")
        generated_table_nodes = generated_soup.select("table")
        public_names = [node.get_text(" ", strip=True) for node in public_soup.select("h4")]
        generated_names = [node.get_text(" ", strip=True) for node in generated_headings]
        assert public_names == generated_names
        assert len(generated_headings) == len(generated_table_nodes)

        # 保存元には、記事見出しと表内「クエスト名」が食い違う既知の誤記がある。
        # 公開ページでは記事見出し名を正としているため、比較時も1列目だけ見出し名へ正規化する。
        for heading, table in zip(generated_headings, generated_table_nodes):
            name_cell = table.select_one("tbody tr td")
            assert name_cell is not None
            name_cell.clear()
            name_cell.append(heading.get_text(" ", strip=True))

        generated_tables = [table.get_text("|", strip=True) for table in generated_table_nodes]
        public_tables = [table.get_text("|", strip=True) for table in public_soup.select("table")]
        assert public_tables == generated_tables

        generated_strategy = [
            paragraph.get_text(" ", strip=True)
            for paragraph in generated_soup.select("p")
            if paragraph.find("strong")
            and paragraph.find("strong").get_text(strip=True) == "攻略:"
        ]
        public_strategy = {
            paragraph.get_text(" ", strip=True)
            for paragraph in public_soup.select("p")
            if paragraph.find("strong")
            and paragraph.find("strong").get_text(strip=True) == "攻略:"
        }
        for strategy in generated_strategy:
            assert strategy in public_strategy


def test_quest_name_mismatches_use_article_heading_names():
    steel = page_text("steel-wilderness.html")
    gran = page_text("gran-water-source.html")
    ancient = page_text("ancient-city.html")
    additional = page_text("additional.html")

    sentinels = (
        (steel, "<h4>グラン安定供給の為に</h4>"),
        (steel, "<h4>超:狂風の暴君</h4>"),
        (steel, "<h4>超:棘の嵐</h4>"),
        (steel, "<h4>難:鋼の荒野殲滅任務</h4>"),
        (gran, "<h4>超：氷塊のギガティオン</h4>"),
        (ancient, "<h4>★スイーツ･メルヘン</h4>"),
        (additional, "<h4>PTアタック・グラン水源</h4>"),
        (additional, "<h4>難:炎の支配者</h4>"),
        (additional, "<h4>サンシャウト編 第1話：疑惑の捜査官</h4>"),
        (additional, "<h4>ガーネット編 第1話：無敵艦隊、発進</h4>"),
    )

    for html, sentinel in sentinels:
        assert sentinel in html


def test_quest_pages_keep_detail_sentinels():
    steel = page_text("steel-wilderness.html")
    additional = page_text("additional.html")

    assert "先遣隊の救出" in steel
    assert "Gクラーダ" in steel
    assert "Lv.31~" in steel
    assert "制限時間15分" in additional


def test_quest_pages_are_registered_in_sidebar_and_sitemap():
    sidebar = (ROOT / "docs" / "js" / "sidebar.js").read_text(encoding="utf-8")
    sitemap = (ROOT / "docs" / "sitemap.xml").read_text(encoding="utf-8")

    for filename, (title, _, _, _) in QUEST_PAGES.items():
        path = f"/PSNOVA/pages/quest/{filename}"
        assert f'href="{path}"' in sidebar
        assert f">{title}</a>" in sidebar
        assert f"https://kylekatann.github.io{path}" in sitemap


def test_great_spire_is_registered_in_sidebar_and_sitemap():
    sidebar = (ROOT / "docs" / "js" / "sidebar.js").read_text(encoding="utf-8")
    sitemap = (ROOT / "docs" / "sitemap.xml").read_text(encoding="utf-8")
    path = "/PSNOVA/pages/quest/great-spire.html"

    assert f'href="{path}"' in sidebar
    assert ">大尖塔</a>" in sidebar
    assert f"https://kylekatann.github.io{path}" in sitemap


def test_quest_sidebar_heading_links_to_difficulty_page():
    sidebar = (ROOT / "docs" / "js" / "sidebar.js").read_text(encoding="utf-8")

    assert '<a class="quest-data-link" href="/PSNOVA/pages/difficulty.html">クエスト</a>' in sidebar
    assert '<li><p>クエスト</p></li>' not in sidebar
    assert '>難易度</a>' not in sidebar
    assert 'aria-label="クエストエリア"' in sidebar
