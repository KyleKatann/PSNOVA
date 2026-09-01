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

    function sectionModels(main, current) {
        if (!current) return [];

        var staticTable = main.querySelector('table.weapon-data-table[data-weapon-static="true"]');
        if (!staticTable) return [];

        return [{
            table: staticTable,
            type: normalizeText(current.label),
            typeLabel: current.label
        }];
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
        var insertionTarget = firstTable.closest(".table-scroll") || firstTable;
        insertionTarget.parentNode.insertBefore(toolbar, insertionTarget);

        function syncStickyTableHeaderOffset() {
            if (!window.matchMedia("(min-width: 801px)").matches) {
                main.style.removeProperty("--weapon-table-header-sticky-top");
                return;
            }

            var toolbarStyle = window.getComputedStyle(toolbar);
            var stickyTop = parseFloat(toolbarStyle.top);
            var marginBottom = parseFloat(toolbarStyle.marginBottom);

            if (!Number.isFinite(stickyTop)) stickyTop = 0;
            if (!Number.isFinite(marginBottom)) marginBottom = 0;

            var offset = (
                stickyTop +
                toolbar.getBoundingClientRect().height +
                marginBottom
            );

            main.style.setProperty(
                "--weapon-table-header-sticky-top",
                Math.ceil(offset) + "px"
            );
        }

        syncStickyTableHeaderOffset();

        window.addEventListener(
            "resize",
            syncStickyTableHeaderOffset
        );

        if ("ResizeObserver" in window) {
            var toolbarResizeObserver = new ResizeObserver(
                syncStickyTableHeaderOffset
            );
            toolbarResizeObserver.observe(toolbar);
        }

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
            var matches = 0;
            records.forEach(function (record) {
                var visible = (!query || record.name.indexOf(query) !== -1) && (!selectedType || record.type === selectedType) &&
                    (!selectedRarity || record.rarity === selectedRarity) && (!selectedShop || record.shopLevel === selectedShop);
                record.row.hidden = !visible;
                if (visible) matches += 1;
            });
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
