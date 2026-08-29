(function () {
    function normalizeText(value) {
        return (value || "").normalize("NFKC").toLowerCase().trim();
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
            rows.forEach(function (row) {
                var cells = row.cells;
                if (!cells || !cells[0]) {
                    return;
                }

                var rarityLabel = cells[1] ? cells[1].textContent.trim() : "";
                var shopLabel = cells[5] ? cells[5].textContent.trim() : "";
                records.push({
                    row: row,
                    details: details,
                    name: normalizeText(cells[0].textContent),
                    type: type,
                    typeLabel: typeLabel,
                    rarity: normalizeText(rarityLabel),
                    rarityLabel: rarityLabel,
                    shopLevel: normalizeText(shopLabel),
                    shopLabel: shopLabel
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
            '</div>'
        ].join("");

        detailsSections[0].parentNode.insertBefore(toolbar, detailsSections[0]);

        var input = document.getElementById("weapon-search");
        var typeFilter = document.getElementById("weapon-type-filter");
        var rarityFilter = document.getElementById("weapon-rarity-filter");
        var shopFilter = document.getElementById("weapon-shop-filter");
        var count = document.getElementById("weapon-search-count");

        populateSelect(typeFilter, uniqueInOrder(records, "type", "typeLabel"), "すべての武器種");
        populateSelect(rarityFilter, uniqueInOrder(records, "rarity", "rarityLabel"), "すべてのレアリティ");
        populateSelect(shopFilter, uniqueInOrder(records, "shopLevel", "shopLabel"), "すべてのShop Lv");

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
        applyFilters();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initWeaponTools, { once: true });
    } else {
        initWeaponTools();
    }
})();
