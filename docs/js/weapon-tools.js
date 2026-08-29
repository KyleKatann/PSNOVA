(function () {
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

    function uniqueInOrder(records, key, labelKey) {
        var seen = new Set();
        var values = [];
        records.forEach(function (record) {
            var value = record[key];
            if (!value || seen.has(value)) {
                return;
            }
            seen.add(value);
            values.push({ value: value, label: record[labelKey] });
        });
        return values;
    }

    function populateSelect(select, values, allLabel) {
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
        if (left === null && right === null) {
            return 0;
        }
        if (left === null) {
            return 1;
        }
        if (right === null) {
            return -1;
        }
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
    }

    function initWeaponTools() {
        var main = document.getElementById("main");
        if (!main || document.getElementById("weapon-search")) {
            return;
        }

        var detailsSections = Array.prototype.slice.call(main.querySelectorAll("details"));
        if (!detailsSections.length) {
            return;
        }

        var records = [];
        detailsSections.forEach(function (details) {
            var table = details.querySelector("table");
            var summary = details.querySelector("summary");
            if (!table || !summary) {
                return;
            }

            var typeLabel = summary.textContent.trim();
            var type = normalizeText(typeLabel);
            var rows = Array.prototype.slice.call(table.querySelectorAll("tr"), 1);
            rows.forEach(function (row, index) {
                var cells = row.cells;
                if (!cells || !cells[0]) {
                    return;
                }

                var rarityLabel = cells[1] ? cells[1].textContent.trim() : "";
                var shopLabel = cells[5] ? cells[5].textContent.trim() : "";
                var rarityNumber = numericValue(rarityLabel);
                var shopNumber = numericValue(shopLabel);
                decorateCompactCells(cells, rarityNumber, shopNumber);
                records.push({
                    row: row,
                    parent: row.parentNode,
                    details: details,
                    originalIndex: index,
                    name: normalizeText(cells[0].textContent),
                    type: type,
                    typeLabel: typeLabel,
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

        var toolbar = document.createElement("div");
        toolbar.className = "data-toolbar";
        toolbar.setAttribute("role", "search");
        toolbar.innerHTML = [
            '<label for="weapon-search">武器名を検索</label>',
            '<div class="data-toolbar-row">',
            '<input id="weapon-search" type="search" inputmode="search" autocomplete="off" placeholder="例: ソード、アリスティン">',
            '<output id="weapon-search-count" aria-live="polite"></output>',
            '</div>',
            '<div class="data-filter-grid">',
            '<div class="data-filter-field"><label for="weapon-type-filter">武器種</label><select id="weapon-type-filter"></select></div>',
            '<div class="data-filter-field"><label for="weapon-rarity-filter">レアリティ</label><select id="weapon-rarity-filter"></select></div>',
            '<div class="data-filter-field"><label for="weapon-shop-filter">Shop Lv</label><select id="weapon-shop-filter"></select></div>',
            '<div class="data-filter-field"><label for="weapon-sort">並び順</label><select id="weapon-sort">',
            '<option value="original">初期順序</option>',
            '<option value="rarity-asc">レアリティ 昇順</option>',
            '<option value="rarity-desc">レアリティ 降順</option>',
            '<option value="attack-asc">最大攻撃力 昇順</option>',
            '<option value="attack-desc">最大攻撃力 降順</option>',
            '<option value="shop-asc">Shop Lv 昇順</option>',
            '<option value="shop-desc">Shop Lv 降順</option>',
            '</select></div>',
            '</div>'
        ].join("");

        detailsSections[0].parentNode.insertBefore(toolbar, detailsSections[0]);

        var input = document.getElementById("weapon-search");
        var typeFilter = document.getElementById("weapon-type-filter");
        var rarityFilter = document.getElementById("weapon-rarity-filter");
        var shopFilter = document.getElementById("weapon-shop-filter");
        var sortControl = document.getElementById("weapon-sort");
        var count = document.getElementById("weapon-search-count");

        populateSelect(typeFilter, uniqueInOrder(records, "type", "typeLabel"), "すべての武器種");
        populateSelect(rarityFilter, uniqueInOrder(records, "rarity", "rarityLabel"), "すべてのレアリティ");
        populateSelect(shopFilter, uniqueInOrder(records, "shopLevel", "shopLabel"), "すべてのShop Lv");

        function applySort() {
            var sortValue = sortControl.value;
            var parts = sortValue.split("-");
            var key = parts[0];
            var direction = parts[1] === "desc" ? -1 : 1;

            detailsSections.forEach(function (details) {
                var sectionRecords = records.filter(function (record) {
                    return record.details === details;
                });

                sectionRecords.sort(function (left, right) {
                    if (key === "original") {
                        return left.originalIndex - right.originalIndex;
                    }
                    if (key === "rarity") {
                        return compareNullableNumbers(left.rarityNumber, right.rarityNumber, direction) || left.originalIndex - right.originalIndex;
                    }
                    if (key === "attack") {
                        return compareNullableNumbers(left.attackNumber, right.attackNumber, direction) || left.originalIndex - right.originalIndex;
                    }
                    if (key === "shop") {
                        return compareNullableNumbers(left.shopNumber, right.shopNumber, direction) || left.originalIndex - right.originalIndex;
                    }
                    return 0;
                });

                sectionRecords.forEach(function (record) {
                    record.parent.appendChild(record.row);
                });
            });
        }

        function applyFilters() {
            var query = normalizeText(input.value);
            var selectedType = typeFilter.value;
            var selectedRarity = rarityFilter.value;
            var selectedShop = shopFilter.value;
            var filtering = Boolean(query || selectedType || selectedRarity || selectedShop);
            var matches = 0;
            var visibleBySection = new Map();

            records.forEach(function (record) {
                var visible = (!query || record.name.indexOf(query) !== -1) &&
                    (!selectedType || record.type === selectedType) &&
                    (!selectedRarity || record.rarity === selectedRarity) &&
                    (!selectedShop || record.shopLevel === selectedShop);

                record.row.hidden = !visible;
                if (visible) {
                    matches += 1;
                    visibleBySection.set(record.details, (visibleBySection.get(record.details) || 0) + 1);
                }
            });

            if (filtering) {
                detailsSections.forEach(function (details) {
                    details.open = Boolean(visibleBySection.get(details));
                });
            }

            count.textContent = matches + " / " + records.length + " 件";
        }

        input.addEventListener("input", applyFilters);
        typeFilter.addEventListener("change", applyFilters);
        rarityFilter.addEventListener("change", applyFilters);
        shopFilter.addEventListener("change", applyFilters);
        sortControl.addEventListener("change", function () {
            applySort();
            applyFilters();
        });
        applySort();
        applyFilters();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initWeaponTools, { once: true });
    } else {
        initWeaponTools();
    }
})();
