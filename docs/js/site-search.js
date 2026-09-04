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

    var searchSources = [
        { title: "ゲーム紹介", url: "/PSNOVA/", keywords: "PSNOVA ファンタシースター ノヴァ ゲーム紹介" }
    ].concat(pages);

    function normalize(value) {
        return (value || "")
            .normalize("NFKC")
            .toLowerCase()
            .replace(/\s+/g, " ")
            .trim();
    }

    function textOf(node) {
        return normalize(node && node.textContent).replace(/\s+/g, " ");
    }

    function sourcePath(url) {
        var path = new URL(url, window.location.href).pathname;
        return path.replace(/\/index\.html$/, "/");
    }

    function currentPath() {
        return window.location.pathname.replace(/\/index\.html$/, "/");
    }

    function dataRows(table) {
        return Array.prototype.slice.call(table.rows).filter(function (row) {
            return Array.prototype.slice.call(row.cells).some(function (cell) {
                return cell.tagName.toLowerCase() === "td";
            });
        });
    }

    function sectionForTable(doc, table) {
        var details = table.closest("details");
        var summary = details && details.querySelector(":scope > summary");
        if (summary) {
            return summary.textContent.replace(/\s+/g, " ").trim();
        }

        var headings = Array.prototype.slice.call(
            doc.querySelectorAll("#main h2, #main h3")
        );
        var latest = "";

        headings.forEach(function (heading) {
            if (heading.compareDocumentPosition(table) & 4) {
                latest = heading.textContent.replace(/\s+/g, " ").trim();
            }
        });

        return latest;
    }

    function extractTableEntries(doc, source) {
        var tables = Array.prototype.slice.call(doc.querySelectorAll("#main table"));
        var entries = [];

        tables.forEach(function (table, tableIndex) {
            var section = sectionForTable(doc, table);

            dataRows(table).forEach(function (row, rowIndex) {
                var cells = Array.prototype.slice.call(row.cells).map(function (cell) {
                    return cell.textContent.replace(/\s+/g, " ").trim();
                });
                var rowText = cells.join(" / ").trim();

                if (!rowText) return;

                entries.push({
                    kind: "row",
                    pageTitle: source.title,
                    section: section,
                    label: cells[0] || section || source.title,
                    text: rowText,
                    cells: cells,
                    url: source.url,
                    tableIndex: tableIndex,
                    rowIndex: rowIndex
                });
            });
        });

        return entries;
    }

    function metadataEntries() {
        return searchSources.map(function (source) {
            return {
                kind: "page",
                pageTitle: source.title,
                section: "",
                label: source.title,
                text: source.title + " " + source.keywords,
                cells: [],
                url: source.url,
                tableIndex: null,
                rowIndex: null
            };
        });
    }

    function matchesQuery(entry, normalizedQuery) {
        var haystack = normalize(entry.text);
        if (haystack.indexOf(normalizedQuery) !== -1) return true;

        var terms = normalizedQuery.split(" ").filter(Boolean);
        return terms.length > 1 && terms.every(function (term) {
            return haystack.indexOf(term) !== -1;
        });
    }

    function scoreEntry(entry, normalizedQuery) {
        if (!matchesQuery(entry, normalizedQuery)) return -1;

        var label = normalize(entry.label);
        var section = normalize(entry.section);
        var text = normalize(entry.text);
        var score = entry.kind === "row" ? 200 : 100;

        if (label === normalizedQuery) score += 1200;
        else if (label.indexOf(normalizedQuery) === 0) score += 900;
        else if (label.indexOf(normalizedQuery) !== -1) score += 700;

        if (section === normalizedQuery) score += 500;
        else if (section.indexOf(normalizedQuery) !== -1) score += 300;

        if (text.indexOf(normalizedQuery) !== -1) score += 250;

        if (entry.kind === "page" && label === normalizedQuery) {
            score += 500;
        }

        return score;
    }

    function matchingCellText(entry, normalizedQuery) {
        var match = entry.cells.find(function (cell) {
            return normalize(cell).indexOf(normalizedQuery) !== -1;
        });

        if (match) return match;

        var terms = normalizedQuery.split(" ").filter(Boolean);
        match = entry.cells.find(function (cell) {
            var normalizedCell = normalize(cell);
            return terms.length > 1 && terms.every(function (term) {
                return normalizedCell.indexOf(term) !== -1;
            });
        });

        return match || entry.label;
    }

    function resultUrl(entry, query) {
        var url = new URL(entry.url, window.location.href);

        if (entry.kind === "row") {
            url.searchParams.set("site-search", query);
            url.searchParams.set("site-search-table", String(entry.tableIndex));
            url.searchParams.set("site-search-row", String(entry.rowIndex));

            var fragmentText = matchingCellText(entry, normalize(query));
            if (fragmentText) {
                url.hash = ":~:text=" + encodeURIComponent(fragmentText.slice(0, 120));
            }
        }

        return url.pathname + url.search + url.hash;
    }

    function revealSearchTarget() {
        var params = new URLSearchParams(window.location.search);
        var query = params.get("site-search");
        var tableIndex = Number(params.get("site-search-table"));
        var rowIndex = Number(params.get("site-search-row"));

        if (!query || !Number.isInteger(tableIndex) || !Number.isInteger(rowIndex)) {
            return;
        }

        var tables = document.querySelectorAll("#main table");
        var table = tables[tableIndex];
        if (!table) return;

        var rows = dataRows(table);
        var row = rows[rowIndex];
        if (!row) return;

        var details = row.closest("details");
        if (details) details.open = true;

        row.setAttribute("data-site-search-target", "true");

        var normalizedQuery = normalize(query);
        Array.prototype.slice.call(row.cells).forEach(function (cell) {
            if (normalize(cell.textContent).indexOf(normalizedQuery) !== -1) {
                cell.setAttribute("data-site-search-hit", "true");
            }
        });

        window.requestAnimationFrame(function () {
            window.requestAnimationFrame(function () {
                row.scrollIntoView({ block: "center", inline: "nearest" });
            });
        });
    }

    function initSiteSearch() {
        if (document.getElementById("site-data-search")) {
            revealSearchTarget();
            return;
        }

        var container = document.getElementById("container");
        var header = container && container.querySelector(":scope > header");
        if (!container || !header) return;

        var wrapper = document.createElement("div");
        wrapper.className = "site-search";
        wrapper.innerHTML = '<label class="site-search-label" for="site-data-search">攻略データを検索</label><form class="site-search-box" role="search" aria-label="攻略データ検索"><div class="site-search-controls"><input id="site-data-search" type="search" role="combobox" aria-autocomplete="list" autocomplete="off" placeholder="武器名、素材名、入手先など..." aria-controls="site-search-results" aria-expanded="false"><button class="site-search-submit" type="submit">検索</button></div><div id="site-search-results" class="site-search-results" role="listbox" hidden></div><p id="site-search-status" class="site-search-status" role="status" aria-live="polite"></p></form>';
        container.insertBefore(wrapper, header.nextSibling);

        var form = wrapper.querySelector("form");
        var input = document.getElementById("site-data-search");
        var results = document.getElementById("site-search-results");
        var status = document.getElementById("site-search-status");
        var submitButton = wrapper.querySelector(".site-search-submit");
        var activeIndex = -1;
        var currentMatches = [];
        var searchIndex = metadataEntries();
        var indexPromise = null;
        var indexComplete = false;

        var currentSource = searchSources.find(function (source) {
            return sourcePath(source.url) === currentPath();
        });

        if (currentSource) {
            searchIndex = searchIndex.concat(
                extractTableEntries(document, currentSource)
            );
        }

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
            status.textContent = "";
        }

        function rankedMatches(query) {
            var normalizedQuery = normalize(query);
            if (!normalizedQuery) return [];

            return searchIndex
                .map(function (entry, order) {
                    return {
                        entry: entry,
                        order: order,
                        score: scoreEntry(entry, normalizedQuery)
                    };
                })
                .filter(function (item) {
                    return item.score >= 0;
                })
                .sort(function (left, right) {
                    return right.score - left.score || left.order - right.order;
                })
                .slice(0, 12)
                .map(function (item) {
                    return item.entry;
                });
        }

        function renderResults() {
            var query = input.value.trim();
            clearActiveOption();

            if (!normalize(query)) {
                closeResults();
                return;
            }

            currentMatches = rankedMatches(query);
            results.innerHTML = "";

            if (currentMatches.length) {
                currentMatches.forEach(function (entry, index) {
                    var option = document.createElement("a");
                    option.id = "site-search-option-" + index;
                    option.setAttribute("role", "option");
                    option.setAttribute("tabindex", "-1");
                    option.setAttribute("aria-selected", "false");
                    option.href = resultUrl(entry, query);

                    if (entry.kind === "row") {
                        var context = entry.pageTitle;
                        if (entry.section && entry.section !== entry.pageTitle) {
                            context += " › " + entry.section;
                        }
                        option.textContent = entry.label + " — " + context + " — " + entry.text;
                    } else {
                        option.textContent = entry.label;
                    }

                    results.appendChild(option);
                });
            } else {
                var empty = document.createElement("p");
                empty.className = "site-search-empty";
                empty.textContent = indexComplete
                    ? "該当するデータがありません"
                    : "全ページのデータを検索中です…";
                results.appendChild(empty);
            }

            results.hidden = false;
            input.setAttribute("aria-expanded", "true");
            status.textContent = indexComplete
                ? (currentMatches.length + "件の候補を表示")
                : "表の全列を検索中…";
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

        function fetchSource(source) {
            return fetch(source.url, { credentials: "same-origin" })
                .then(function (response) {
                    if (!response.ok) {
                        throw new Error("Search source fetch failed: " + response.status);
                    }
                    return response.text();
                })
                .then(function (html) {
                    var doc = new DOMParser().parseFromString(html, "text/html");
                    return extractTableEntries(doc, source);
                })
                .catch(function () {
                    return [];
                });
        }

        function loadSourcesWithLimit(sources, limit) {
            var queueIndex = 0;

            function worker() {
                if (queueIndex >= sources.length) {
                    return Promise.resolve();
                }

                var source = sources[queueIndex];
                queueIndex += 1;

                return fetchSource(source).then(function (entries) {
                    searchIndex = searchIndex.concat(entries);

                    if (normalize(input.value) && activeIndex < 0) {
                        renderResults();
                    }

                    return worker();
                });
            }

            var workers = [];
            var workerCount = Math.min(limit, sources.length);
            for (var index = 0; index < workerCount; index += 1) {
                workers.push(worker());
            }

            return Promise.all(workers);
        }

        function ensureSearchIndex() {
            if (indexPromise) return indexPromise;

            var remoteSources = searchSources.filter(function (source) {
                return sourcePath(source.url) !== currentPath();
            });

            indexPromise = loadSourcesWithLimit(remoteSources, 4)
                .then(function () {
                    indexComplete = true;
                    if (normalize(input.value) && activeIndex < 0) {
                        renderResults();
                    }
                    return searchIndex;
                });

            return indexPromise;
        }

        function navigateTo(entry, query) {
            window.location.assign(resultUrl(entry, query));
        }

        function submitSearch() {
            var submittedQuery = input.value.trim();
            if (!normalize(submittedQuery)) {
                closeResults();
                input.focus();
                return;
            }

            if (activeIndex >= 0 && currentMatches[activeIndex]) {
                navigateTo(currentMatches[activeIndex], submittedQuery);
                return;
            }

            submitButton.disabled = true;
            submitButton.textContent = "検索中…";

            ensureSearchIndex().then(function () {
                if (input.value.trim() !== submittedQuery) return;

                renderResults();
                if (currentMatches.length) {
                    navigateTo(currentMatches[0], submittedQuery);
                } else {
                    input.focus();
                }
            }).finally(function () {
                submitButton.disabled = false;
                submitButton.textContent = "検索";
            });
        }

        input.addEventListener("input", function () {
            renderResults();
            if (normalize(input.value)) {
                ensureSearchIndex();
            }
        });

        input.addEventListener("focus", function () {
            if (normalize(input.value) && results.hidden) {
                renderResults();
                ensureSearchIndex();
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

        revealSearchTarget();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initSiteSearch, { once: true });
    } else {
        initSiteSearch();
    }
})();
