(function () {
    var pages = [
        { title: "よくある質問", url: "/PSNOVA/pages/faq.html", keywords: "FAQ 質問 体験版 システム 高難易度 PSO2" },
        { title: "武器データ", url: "/PSNOVA/pages/weapon.html", keywords: "武器 ウェポン 武器種" },
        { title: "ソード", url: "/PSNOVA/pages/weapon/sword.html", keywords: "武器 ソード sword" },
        { title: "パルチザン", url: "/PSNOVA/pages/weapon/partizan.html", keywords: "武器 パルチザン partizan" },
        { title: "ダブルセイバー", url: "/PSNOVA/pages/weapon/doublesaber.html", keywords: "武器 ダブルセイバー doublesaber" },
        { title: "ナックル", url: "/PSNOVA/pages/weapon/knuckle.html", keywords: "武器 ナックル knuckle" },
        { title: "アサルトライフル", url: "/PSNOVA/pages/weapon/rifle.html", keywords: "武器 ライフル rifle" },
        { title: "ツインマシンガン", url: "/PSNOVA/pages/weapon/tmachinegun.html", keywords: "武器 ツインマシンガン machinegun" },
        { title: "ロッド", url: "/PSNOVA/pages/weapon/rod.html", keywords: "武器 ロッド rod" },
        { title: "タリス", url: "/PSNOVA/pages/weapon/talis.html", keywords: "武器 タリス talis" },
        { title: "ウォンド", url: "/PSNOVA/pages/weapon/wand.html", keywords: "武器 ウォンド wand" },
        { title: "ヘイロウ", url: "/PSNOVA/pages/weapon/halo.html", keywords: "武器 ヘイロウ halo" },
        { title: "パイル", url: "/PSNOVA/pages/weapon/pile.html", keywords: "武器 パイル pile" },
        { title: "防具データ", url: "/PSNOVA/pages/armor.html", keywords: "防具 アーマー armor" },
        { title: "アタッチパーツ", url: "/PSNOVA/pages/attachment.html", keywords: "アタッチ パーツ attachment" },
        { title: "特殊能力", url: "/PSNOVA/pages/specialability.html", keywords: "特殊能力 ability" },
        { title: "素材", url: "/PSNOVA/pages/material.html", keywords: "素材 material コア" },
        { title: "消費アイテム", url: "/PSNOVA/pages/item.html", keywords: "アイテム item 消費" },
        { title: "エネミー", url: "/PSNOVA/pages/enemy.html", keywords: "敵 enemy エネミー" },
        { title: "ギガンテス", url: "/PSNOVA/pages/gigantes.html", keywords: "ギガンテス gigantes ボス" },
        { title: "難易度", url: "/PSNOVA/pages/difficulty.html", keywords: "難易度 difficulty クエスト" },
        { title: "種族", url: "/PSNOVA/pages/species.html", keywords: "種族 species キャラクター" },
        { title: "外見・コスチューム", url: "/PSNOVA/pages/appearance.html", keywords: "外見 ヘアスタイル コスチューム アクセサリー appearance" },
        { title: "トロフィー", url: "/PSNOVA/pages/trophy.html", keywords: "トロフィー trophy" }
    ];

    function normalize(value) { return (value || "").normalize("NFKC").toLowerCase().trim(); }
    function initSiteSearch() {
        if (document.getElementById("site-data-search")) return;
        var primaryNav = document.getElementById("menubar");
        if (!primaryNav || !primaryNav.parentNode) return;
        var wrapper = document.createElement("div");
        wrapper.className = "site-search";
        wrapper.innerHTML = '<label class="site-search-label" for="site-data-search">攻略データを検索</label><div class="site-search-box"><input id="site-data-search" type="search" autocomplete="off" placeholder="武器、防具、素材、エネミー..." aria-controls="site-search-results" aria-expanded="false"><div id="site-search-results" class="site-search-results" role="listbox" hidden></div></div>';
        primaryNav.parentNode.insertBefore(wrapper, primaryNav.nextSibling);
        var input = document.getElementById("site-data-search"); var results = document.getElementById("site-search-results");
        function closeResults() { results.hidden = true; results.innerHTML = ""; input.setAttribute("aria-expanded", "false"); }
        function renderResults() {
            var query = normalize(input.value); if (!query) { closeResults(); return; }
            var matches = pages.filter(function (page) { return normalize(page.title + " " + page.keywords).indexOf(query) !== -1; }).slice(0, 8);
            results.innerHTML = matches.length ? matches.map(function (page) { return '<a role="option" href="' + page.url + '">' + page.title + '</a>'; }).join("") : '<p class="site-search-empty">該当するデータカテゴリがありません</p>';
            results.hidden = false; input.setAttribute("aria-expanded", "true");
        }
        input.addEventListener("input", renderResults);
        input.addEventListener("keydown", function (event) { if (event.key === "Escape") { input.value = ""; closeResults(); } });
        document.addEventListener("click", function (event) { if (!wrapper.contains(event.target)) closeResults(); });
    }
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initSiteSearch, { once: true }); else initSiteSearch();
})();
