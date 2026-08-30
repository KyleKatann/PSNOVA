(function () {
    function numericValue(cell) {
        var text = ((cell && cell.textContent) || "").replace(/,/g, "").trim();
        var match = text.match(/-?\d+(?:\.\d+)?/);
        return match ? Number(match[0]) : NaN;
    }

    function rarityBand(value) {
        if (!Number.isFinite(value)) return "";
        if (value >= 13) return "rarity-high";
        if (value >= 10) return "rarity-mid";
        if (value >= 7) return "rarity-low";
        return "";
    }

    function normalizedLabel(value) {
        return (value || "").replace(/\s+/g, "").toLowerCase();
    }

    function decorateSemanticDataTable(table) {
        if (!table || !table.tHead || !table.tBodies.length) return;

        var headerRow = table.tHead.rows[0];
        if (!headerRow) return;

        var labels = Array.prototype.map.call(headerRow.cells, function (cell) {
            return normalizedLabel(cell.textContent);
        });

        labels.forEach(function (label, index) {
            if (label.indexOf("レア") !== -1 || label.indexOf("rarity") !== -1) {
                Array.prototype.forEach.call(table.tBodies, function (tbody) {
                    Array.prototype.forEach.call(tbody.rows, function (row) {
                        var cell = row.cells[index];
                        if (!cell) return;
                        var band = rarityBand(numericValue(cell));
                        if (band) cell.classList.add("rarity-cell", band);
                    });
                });
            }

            var statClass = "";
            if (label.indexOf("打撃") !== -1) statClass = "stat-melee";
            else if (label.indexOf("射撃") !== -1) statClass = "stat-ranged";
            else if (label.indexOf("法撃") !== -1) statClass = "stat-tech";

            if (statClass) {
                headerRow.cells[index].classList.add(statClass);
                Array.prototype.forEach.call(table.tBodies, function (tbody) {
                    Array.prototype.forEach.call(tbody.rows, function (row) {
                        if (row.cells[index]) row.cells[index].classList.add(statClass);
                    });
                });
            }
        });
    }

    function ensureScrollableTable(table) {
        if (!table || table.closest(".table-scroll")) return;

        var wrapper = document.createElement("div");
        wrapper.className = "table-scroll";
        wrapper.setAttribute("role", "region");
        wrapper.setAttribute("aria-label", "横スクロール可能なデータ表");
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
    }

    function initTableEnhancements() {
        Array.prototype.slice.call(document.querySelectorAll("#main table")).forEach(function (table) {
            decorateSemanticDataTable(table);
            ensureScrollableTable(table);
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initTableEnhancements, { once: true });
    } else {
        initTableEnhancements();
    }
})();
