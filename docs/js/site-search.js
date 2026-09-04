(function () {
    var pages = [
        { title: "初心者Q&A", url: "/PSNOVA/pages/faq.html", keywords: "FAQ 質問 初心者 体験版 システム 高難易度 PSO2" },
        { title: "クラス", url: "/PSNOVA/pages/class.html", keywords: "クラス ハンター レンジャー フォース バスター class" },
        { title: "スキル", url: "/PSNOVA/pages/skill.html", keywords: "スキル skill ハンター レンジャー フォース バスター" },
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

    function normalize(value) {
        return (value || "").normalize("NFKC").toLowerCase().trim();
    }

    function initSiteSearch() {
        if (document.getElementById("site-data-search")) return;

        var container = document.getElementById("container");
        var header = container && container.querySelector(":scope > header");
        if (!container || !header) return;

        var wrapper = document.createElement("div");
        wrapper.className = "site-search";
        wrapper.innerHTML = '<label class="site-search-label" for="site-data-search">攻略データを検索</label><form class="site-search-box" role="search" aria-label="攻略データ検索"><div class="site-search-controls"><input id="site-data-search" type="search" role="combobox" aria-autocomplete="list" autocomplete="off" placeholder="武器、防具、素材、エネミー..." aria-controls="site-search-results" aria-expanded="false"><button class="site-search-submit" type="submit">検索</button></div><div id="site-search-results" class="site-search-results" role="listbox" hidden></div></form>';
        container.insertBefore(wrapper, header.nextSibling);

        var form = wrapper.querySelector("form");
        var input = document.getElementById("site-data-search");
        var results = document.getElementById("site-search-results");
        var activeIndex = -1;
        var currentMatches = [];

        function optionElements() {
            return Array.prototype.slice.call(
                results.querySelectorAll('[role="option"]')
            );
        }

        function clearActiveOption() {
            activeIndex = -1;
            input.removeAttribute("aria-activedescendant");

            optionElements().forEach(function (option) {
                option.classList.remove("is-active");
                option.setAttribute("aria-selected", "false");
            });
        }

        function closeResults() {
            clearActiveOption();
            results.hidden = true;
            results.innerHTML = "";
            currentMatches = [];
            input.setAttribute("aria-expanded", "false");
        }

        function renderResults() {
            var query = normalize(input.value);
            clearActiveOption();

            if (!query) {
                closeResults();
                return;
            }

            currentMatches = pages.filter(function (page) {
                return normalize(page.title + " " + page.keywords).indexOf(query) !== -1;
            }).slice(0, 8);

            results.innerHTML = currentMatches.length
                ? currentMatches.map(function (page, index) {
                    return '<a id="site-search-option-' + index + '" role="option" tabindex="-1" aria-selected="false" href="' + page.url + '">' + page.title + '</a>';
                }).join("")
                : '<p class="site-search-empty">該当するデータカテゴリがありません</p>';

            results.hidden = false;
            input.setAttribute("aria-expanded", "true");
        }

        function setActiveOption(index) {
            var options = optionElements();
            if (!options.length) {
                clearActiveOption();
                return;
            }

            activeIndex = (index + options.length) % options.length;

            options.forEach(function (option, optionIndex) {
                var selected = optionIndex === activeIndex;
                option.classList.toggle("is-active", selected);
                option.setAttribute("aria-selected", String(selected));
            });

            input.setAttribute(
                "aria-activedescendant",
                options[activeIndex].id
            );
            options[activeIndex].scrollIntoView({ block: "nearest" });
        }

        function submitSearch() {
            if (!normalize(input.value)) {
                closeResults();
                input.focus();
                return;
            }

            if (!currentMatches.length) {
                renderResults();
            }

            if (!currentMatches.length) {
                input.focus();
                return;
            }

            var targetIndex = activeIndex >= 0 ? activeIndex : 0;
            window.location.assign(currentMatches[targetIndex].url);
        }

        input.addEventListener("input", renderResults);
        input.addEventListener("focus", function () {
            if (normalize(input.value) && results.hidden) {
                renderResults();
            }
        });

        input.addEventListener("keydown", function (event) {
            if (event.key === "ArrowDown") {
                if (results.hidden) {
                    renderResults();
                }
                if (currentMatches.length) {
                    event.preventDefault();
                    setActiveOption(activeIndex + 1);
                }
                return;
            }

            if (event.key === "ArrowUp") {
                if (results.hidden) {
                    renderResults();
                }
                if (currentMatches.length) {
                    event.preventDefault();
                    setActiveOption(activeIndex < 0 ? currentMatches.length - 1 : activeIndex - 1);
                }
                return;
            }

            if (event.key === "Escape") {
                if (!results.hidden) {
                    event.preventDefault();
                    closeResults();
                } else if (input.value) {
                    input.value = "";
                }
            }
        });

        form.addEventListener("submit", function (event) {
            event.preventDefault();
            submitSearch();
        });

        document.addEventListener("click", function (event) {
            if (!wrapper.contains(event.target)) closeResults();
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initSiteSearch, { once: true });
    } else {
        initSiteSearch();
    }
})();
