(function () {
    var weaponPages = [
        { slug: "sword", label: "ソード" },
        { slug: "partizan", label: "パルチザン" },
        { slug: "doublesaber", label: "ダブルセイバー" },
        { slug: "knuckle", label: "ナックル" },
        { slug: "rifle", label: "アサルトライフル" },
        { slug: "tmachinegun", label: "ツインマシンガン" },
        { slug: "rod", label: "ロッド" },
        { slug: "talis", label: "タリス" },
        { slug: "wand", label: "ウォンド" },
        { slug: "halo", label: "ヘイロウ" },
        { slug: "pile", label: "パイル" }
    ];

    function normalizeText(value) {
        return (value || "").normalize("NFKC").toLowerCase().trim();
    }

    function numericValue(value) {
        var match = String(value || "").replace(/,/g, "").match(/-?\d+(?:\.\d+)?/);
        return match ? Number(match[0]) : null;
    }

    function maxNumeric(cells, indexes) {
        var values = indexes.map(function (index) {
            return cells[index] ? numericValue(cells[index].textContent) : null;
        }).filter(function (value) {
            return value !== null;
        });
        return values.length ? Math.max.apply(Math, values) : null;
    }

    function childPage() {
        var match = window.location.pathname.match(/\/PSNOVA\/pages\/weapon\/([^/]+)\.html$/);
        if (!match) return null;
        return weaponPages.filter(function (item) { return item.slug === match[1]; })[0] || null;
    }

    /* Compatibility path for weapon child pages that have not yet been migrated.
       Migrated pages must contain only their own static table and never depend on
       this function to delete unrelated weapon sections. */
    function prepareLegacyChildPage(main, current) {
        if (!current) return;

        main.classList.add("weapon-detail-page");
        var section = main.querySelector("section");
        if (!section) return;

        var heading = section.querySelector("h2");
        if (heading) heading.textContent = current.label + " 武器データ";
        var oldSubheading = section.querySelector("h3");
        if (oldSubheading) oldSubheading.remove();
        var oldImage = section.querySelector(":scope > img");
        if (oldImage) oldImage.remove();
        var intro = section.querySelector(":scope > p");
        if (intro) intro.textContent = "PSNOVA（ファンタシースターノヴァ）の" + current.label + "一覧。レアリティ、攻撃力、ショップレベル、必要素材を確認できる。";

        var detailsSections = Array.prototype.slice.call(section.querySelectorAll(":scope > details"));
        var selected = null;
        detailsSections.forEach(function (details) {
            var summary = details.querySelector("summary");
            if (summary && summary.textContent.trim() === current.label) selected = details;
            else details.remove();
        });
        if (!selected) return;
        selected.open = true;

        var index = weaponPages.indexOf(current);
        var previous = weaponPages[(index + weaponPages.length - 1) % weaponPages.length];
        var next = weaponPages[(index + 1) % weaponPages.length];
        var nav = document.createElement("nav");
        nav.className = "weapon-page-nav";
        nav.setAttribute("aria-label", "武器種ナビゲーション");
        nav.innerHTML = '<a href="/PSNOVA/pages/weapon/' + previous.slug + '.html" rel="prev">← ' + previous.label + '</a>' +
            '<a class="weapon-page-nav-index" href="/PSNOVA/pages/weapon.html">武器一覧</a>' +
            '<a href="/PSNOVA/pages/weapon/' + next.slug + '.html" rel="next">' + next.label + ' →</a>';
        selected.parentNode.insertBefore(nav, selected);
    }

    function sectionModels(main, current) {
        if (current) {
            var staticTable = main.querySelector('table.weapon-data-table[data-weapon-static="true"]');
            if (staticTable) {
                return [{
                    table: staticTable,
                    details: null,
                    type: normalizeText(current.label),
                    typeLabel: current.label
                }];
            }
        }

        return Array.prototype.slice.call(main.querySelectorAll("details")).map(function (details) {
            var table = details.querySelector("table");
            var summary = details.querySelector("summary");
            if (!table || !summary) return null;
            var label = summary.textContent.trim();
            return { table: table, details: details, type: normalizeText(label), typeLabel: label };
        }).filter(Boolean);
    }

    function uniqueInOrder(records, key, labelKey) {
        var seen = new Set();
        var values = [];
        records.forEach(function (record) {
            var value = record[key];
            if (!value || seen.has(value)) return;
            seen.add(value);
            values.push({ value: value, label: record[labelKey] });
        });
        return values;
    }

    function populateSelect(select, values, allLabel) {
        if (!select) return;
        var all = document.createElement("option");
        all.value = "";
        all.textContent = allLabel;
        select.appendChild(all);
        values.forEach(function (item) {
            var option = document.createElement("option");
            option.value = item.value;
            option.textContent = item.label;
            select.appendChild(option);
        });
    }

    function compareNullableNumbers(left, right, direction) {
        if (left === null && right === null) return 0;
        if (left === null) return 1;
        if (right === null) return -1;
        return (left - right) * direction;
    }

    function decorateCompactCells(cells, rarityNumber, shopNumber) {
        if (cells[1] && rarityNumber !== null) {
            cells[1].classList.add("rarity-cell");
            cells[1].setAttribute("data-rarity", String(rarityNumber));
            cells[1].setAttribute("aria-label", "レアリティ " + rarityNumber);
        }
        if (cells[5] && shopNumber !== null) {
            cells[5].classList.add("shop-level-cell");
            cells[5].setAttribute("data-shop-level", String(shopNumber));
        }

        [
            { index: 2, className: "weapon-stat-melee" },
            { index: 3, className: "weapon-stat-ranged" },
            { index: 4, className: "weapon-stat-tech" }
        ].forEach(function (stat) {
            var cell = cells[stat.index];
            if (!cell) return;
            var hasValue = cell.textContent.trim() !== "";
            cell.classList.add("weapon-stat-cell", stat.className, hasValue ? "has-value" : "is-empty");
        });
    }

    function initWeaponTools() {
        var main = document.getElementById("main");
        if (!main || document.getElementById("weapon-search")) return;

        var current = childPage();
        var hasStaticChild = Boolean(current && main.querySelector('table.weapon-data-table[data-weapon-static="true"]'));
        if (!hasStaticChild) prepareLegacyChildPage(main, current);

        var sections = sectionModels(main, current);
        if (!sections.length) return;

        var records = [];
        sections.forEach(function (section) {
            var table = section.table;
            var rows = table.tBodies.length
                ? Array.prototype.slice.call(table.tBodies[0].rows)
                : Array.prototype.slice.call(table.rows, 1);
            rows.forEach(function (row, index) {
                var cells = row.cells;
                if (!cells || !cells[0]) return;
                var rarityLabel = cells[1] ? cells[1].textContent.trim() : "";
                var shopLabel = cells[5] ? cells[5].textContent.trim() : "";
                var rarityNumber = numericValue(rarityLabel);
                var shopNumber = numericValue(shopLabel);
                decorateCompactCells(cells, rarityNumber, shopNumber);
                records.push({
                    row: row,
                    parent: row.parentNode,
                    section: section,
                    originalIndex: index,
                    name: normalizeText(cells[0].textContent),
                    type: section.type,
                    typeLabel: section.typeLabel,
                    rarity: normalizeText(rarityLabel),
                    rarityLabel: rarityLabel,
                    rarityNumber: rarityNumber,
                    shopLevel: normalizeText(shopLabel),
                    shopLabel: shopLabel,
                    shopNumber: shopNumber,
                    attackNumber: maxNumeric(cells, [2, 3, 4])
                });
            });
        });

        var typeField = current ? "" : '<div class="data-filter-field"><label for="weapon-type-filter">武器種</label><select id="weapon-type-filter"></select></div>';
        var toolbar = document.createElement("div");
        toolbar.className = "data-toolbar";
        toolbar.setAttribute("role", "search");
        toolbar.innerHTML = [
            '<label for="weapon-search">武器名を検索</label>',
            '<div class="data-toolbar-row">',
            '<input id="weapon-search" type="search" inputmode="search" autocomplete="off" placeholder="' + (current ? current.label + '内を検索' : '例: ソード、アリスティン') + '">',
            '<output id="weapon-search-count" aria-live="polite"></output>',
            '</div>',
            '<div class="data-filter-grid' + (current ? ' is-single-type' : '') + '">',
            typeField,
            '<div class="data-filter-field"><label for="weapon-rarity-filter">レアリティ</label><select id="weapon-rarity-filter"></select></div>',
            '<div class="data-filter-field"><label for="weapon-shop-filter">ショップレベル</label><select id="weapon-shop-filter"></select></div>',
            '<div class="data-filter-field"><label for="weapon-sort">並び順</label><select id="weapon-sort">',
            '<option value="original">初期順序</option><option value="rarity-asc">レアリティ 昇順</option><option value="rarity-desc">レアリティ 降順</option>',
            '<option value="attack-asc">最大攻撃力 昇順</option><option value="attack-desc">最大攻撃力 降順</option>',
            '<option value="shop-asc">ショップレベル 昇順</option><option value="shop-desc">ショップレベル 降順</option>',
            '</select></div></div>'
        ].join("");

        var firstTable = sections[0].table;
        var insertionTarget = firstTable.closest(".table-scroll") || sections[0].details || firstTable;
        insertionTarget.parentNode.insertBefore(toolbar, insertionTarget);

        var input = document.getElementById("weapon-search");
        var typeFilter = document.getElementById("weapon-type-filter");
        var rarityFilter = document.getElementById("weapon-rarity-filter");
        var shopFilter = document.getElementById("weapon-shop-filter");
        var sortControl = document.getElementById("weapon-sort");
        var count = document.getElementById("weapon-search-count");

        populateSelect(typeFilter, uniqueInOrder(records, "type", "typeLabel"), "すべての武器種");
        populateSelect(rarityFilter, uniqueInOrder(records, "rarity", "rarityLabel"), "すべてのレアリティ");
        populateSelect(shopFilter, uniqueInOrder(records, "shopLevel", "shopLabel"), "すべてのショップレベル");

        function applySort() {
            var parts = sortControl.value.split("-");
            var key = parts[0];
            var direction = parts[1] === "desc" ? -1 : 1;
            sections.forEach(function (section) {
                var sectionRecords = records.filter(function (record) { return record.section === section; });
                sectionRecords.sort(function (left, right) {
                    if (key === "original") return left.originalIndex - right.originalIndex;
                    if (key === "rarity") return compareNullableNumbers(left.rarityNumber, right.rarityNumber, direction) || left.originalIndex - right.originalIndex;
                    if (key === "attack") return compareNullableNumbers(left.attackNumber, right.attackNumber, direction) || left.originalIndex - right.originalIndex;
                    if (key === "shop") return compareNullableNumbers(left.shopNumber, right.shopNumber, direction) || left.originalIndex - right.originalIndex;
                    return 0;
                });
                sectionRecords.forEach(function (record) { record.parent.appendChild(record.row); });
            });
        }

        function applyFilters() {
            var query = normalizeText(input.value);
            var selectedType = typeFilter ? typeFilter.value : "";
            var selectedRarity = rarityFilter.value;
            var selectedShop = shopFilter.value;
            var filtering = Boolean(query || selectedType || selectedRarity || selectedShop);
            var matches = 0;
            var visibleBySection = new Map();
            records.forEach(function (record) {
                var visible = (!query || record.name.indexOf(query) !== -1) && (!selectedType || record.type === selectedType) &&
                    (!selectedRarity || record.rarity === selectedRarity) && (!selectedShop || record.shopLevel === selectedShop);
                record.row.hidden = !visible;
                if (visible) {
                    matches += 1;
                    visibleBySection.set(record.section, (visibleBySection.get(record.section) || 0) + 1);
                }
            });
            if (filtering) {
                sections.forEach(function (section) {
                    if (section.details) section.details.open = Boolean(visibleBySection.get(section));
                });
            }
            count.textContent = matches + " / " + records.length + " 件";
        }

        input.addEventListener("input", applyFilters);
        if (typeFilter) typeFilter.addEventListener("change", applyFilters);
        rarityFilter.addEventListener("change", applyFilters);
        shopFilter.addEventListener("change", applyFilters);
        sortControl.addEventListener("change", function () { applySort(); applyFilters(); });
        applySort();
        applyFilters();
    }

    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initWeaponTools, { once: true });
    else initWeaponTools();
})();
