(function () {
    var SITEMAP_URL = "/PSNOVA/sitemap.xml";
    var MAX_RESULTS = 12;
    var FETCH_CONCURRENCY = 4;

    function normalize(value) {
        return (value || "")
            .normalize("NFKC")
            .toLowerCase()
            .replace(/\s+/g, " ")
            .trim();
    }

    function cleanText(value) {
        return (value || "").replace(/\s+/g, " ").trim();
    }

    function canonicalPath(url) {
        return new URL(url, window.location.href).pathname.replace(/\/index\.html$/, "/");
    }

    function isPublicPageUrl(url) {
        var parsed;
        try {
            parsed = new URL(url, window.location.href);
        } catch (error) {
            return false;
        }

        if (parsed.origin !== window.location.origin) return false;
        if (parsed.pathname.indexOf("/PSNOVA/") !== 0) return false;
        if (parsed.pathname.indexOf("/分類中/") !== -1) return false;

        return parsed.pathname.endsWith("/") || parsed.pathname.endsWith(".html");
    }

    function pageTitleFromDocument(doc) {
        var heading = doc.querySelector("#main h2");
        if (heading && cleanText(heading.textContent)) {
            return cleanText(heading.textContent);
        }

        var title = cleanText(doc.title);
        return title.replace(/^PSNOVA攻略サイト\s*-\s*/, "") || "PSNOVA攻略サイト";
    }

    function sourceFromDocument(doc, url) {
        return {
            title: pageTitleFromDocument(doc),
            url: canonicalPath(url)
        };
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
            return cleanText(summary.textContent);
        }

        var headings = Array.prototype.slice.call(
            doc.querySelectorAll("#main h2, #main h3")
        );
        var latest = "";

        headings.forEach(function (heading) {
            if (heading.compareDocumentPosition(table) & 4) {
                latest = cleanText(heading.textContent);
            }
        });

        return latest;
    }

    function extractDocumentEntries(doc, source) {
        var entries = [{
            kind: "page",
            pageTitle: source.title,
            section: "",
            label: source.title,
            text: source.title,
            cells: [],
            url: source.url,
            tableIndex: null,
            rowIndex: null
        }];

        var tables = Array.prototype.slice.call(doc.querySelectorAll("#main table"));

        tables.forEach(function (table, tableIndex) {
            var section = sectionForTable(doc, table);

            dataRows(table).forEach(function (row, rowIndex) {
                var cells = Array.prototype.slice.call(row.cells).map(function (cell) {
                    return cleanText(cell.textContent);
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

        var normalizedCells = entry.cells.map(normalize);
        var section = normalize(entry.section);
        var label = normalize(entry.label);
        var score = entry.kind === "row" ? 200 : 100;

        if (normalizedCells.some(function (cell) { return cell === normalizedQuery; })) {
            score += 1200;
        } else if (normalizedCells.some(function (cell) { return cell.indexOf(normalizedQuery) === 0; })) {
            score += 900;
        } else if (normalizedCells.some(function (cell) { return cell.indexOf(normalizedQuery) !== -1; })) {
            score += 700;
        }

        if (entry.kind === "page") {
            if (label === normalizedQuery) score += 1400;
            else if (label.indexOf(normalizedQuery) === 0) score += 1000;
            else if (label.indexOf(normalizedQuery) !== -1) score += 800;
        }

        if (section === normalizedQuery) score += 500;
        else if (section.indexOf(normalizedQuery) !== -1) score += 300;

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

        var table = document.querySelectorAll("#main table")[tableIndex];
        if (!table) return;

        var row = dataRows(table)[rowIndex];
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

    function loadSitemapSources() {
        return fetch(SITEMAP_URL, { credentials: "same-origin" })
            .then(function (response) {
                if (!response.ok) {
                    throw new Error("Sitemap fetch failed: " + response.status);
                }
                return response.text();
            })
            .then(function (xmlText) {
                var xml = new DOMParser().parseFromString(xmlText, "application/xml");
                if (xml.querySelector("parsererror")) {
                    throw new Error("Sitemap XML parse failed");
                }

                var seen = Object.create(null);
                var sources = [];
                var locNodes = Array.prototype.slice.call(
                    xml.getElementsByTagNameNS("*", "loc")
                );

                locNodes.forEach(function (loc) {
                    var rawUrl = cleanText(loc.textContent);
                    if (!isPublicPageUrl(rawUrl)) return;

                    var path = canonicalPath(rawUrl);
                    if (seen[path]) return;
                    seen[path] = true;
                    sources.push({ url: path });
                });

                return sources;
            });
    }

    function fetchDocumentEntries(source) {
        return fetch(source.url, { credentials: "same-origin" })
            .then(function (response) {
                if (!response.ok) {
                    throw new Error("Search source fetch failed: " + response.status);
                }
                return response.text();
            })
            .then(function (html) {
                var doc = new DOMParser().parseFromString(html, "text/html");
                return extractDocumentEntries(
                    doc,
                    sourceFromDocument(doc, source.url)
                );
            })
            .catch(function () {
                return [];
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
        var indexPromise = null;
        var indexComplete = false;
        var indexFailed = false;

        var currentSource = sourceFromDocument(document, window.location.href);
        var searchIndex = extractDocumentEntries(document, currentSource);

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
                .slice(0, MAX_RESULTS)
                .map(function (item) {
                    return item.entry;
                });
        }

        function appendResult(entry, index, query) {
            var option = document.createElement("a");
            option.id = "site-search-option-" + index;
            option.setAttribute("role", "option");
            option.setAttribute("tabindex", "-1");
            option.setAttribute("aria-selected", "false");
            option.href = resultUrl(entry, query);

            var title = document.createElement("span");
            title.className = "site-search-result-title";
            title.textContent = entry.label;
            option.appendChild(title);

            if (entry.kind === "row") {
                var context = document.createElement("span");
                context.className = "site-search-result-context";
                context.textContent = entry.pageTitle + (entry.section ? " › " + entry.section : "");
                option.appendChild(context);

                var matchedCell = matchingCellText(entry, normalize(query));
                var snippet = document.createElement("span");
                snippet.className = "site-search-result-snippet";
                snippet.textContent = cleanText(matchedCell).slice(0, 180);
                option.appendChild(snippet);
            }

            results.appendChild(option);
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
                    appendResult(entry, index, query);
                });
            } else {
                var empty = document.createElement("p");
                empty.className = "site-search-empty";
                empty.textContent = indexComplete
                    ? "該当するデータがありません"
                    : "全ページの表を検索中です…";
                results.appendChild(empty);
            }

            results.hidden = false;
            input.setAttribute("aria-expanded", "true");

            if (indexFailed) {
                status.textContent = "一部ページを読み込めませんでした。表示済みデータから検索しています。";
            } else if (!indexComplete) {
                status.textContent = "公開ページの表を動的に検索中…";
            } else {
                status.textContent = currentMatches.length + "件の候補を表示";
            }
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

        function loadSourcesWithLimit(sources, limit) {
            var queueIndex = 0;

            function worker() {
                if (queueIndex >= sources.length) {
                    return Promise.resolve();
                }

                var source = sources[queueIndex];
                queueIndex += 1;

                return fetchDocumentEntries(source).then(function (entries) {
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

            indexPromise = loadSitemapSources()
                .then(function (sources) {
                    var current = canonicalPath(window.location.href);
                    var remoteSources = sources.filter(function (source) {
                        return canonicalPath(source.url) !== current;
                    });
                    return loadSourcesWithLimit(remoteSources, FETCH_CONCURRENCY);
                })
                .catch(function () {
                    indexFailed = true;
                })
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
                if (results.hidden) renderResults();
                if (currentMatches.length) {
                    event.preventDefault();
                    setActiveOption(activeIndex + 1);
                }
                return;
            }

            if (event.key === "ArrowUp") {
                if (results.hidden) renderResults();
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
