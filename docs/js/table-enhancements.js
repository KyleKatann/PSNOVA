(function () {
    function numericValue(cell) {
        var text = ((cell && cell.textContent) || "").replace(/,/g, "").trim();
        var match = text.match(/-?\d+(?:\.\d+)?/);
        return match ? Number(match[0]) : NaN;
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

                        var rarity = numericValue(cell);
                        if (!Number.isFinite(rarity) || rarity < 1 || rarity > 15) return;

                        cell.classList.add("rarity-cell");
                        cell.setAttribute("data-rarity", String(rarity));
                        cell.setAttribute("aria-label", "レアリティ " + rarity);

                        if (cell.textContent.indexOf("★") !== -1) {
                            cell.classList.add("rarity-source-star");
                        }
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
        if (!table) return;

        var wrapper = table.closest(".table-scroll");
        if (!wrapper) {
            wrapper = document.createElement("div");
            wrapper.className = "table-scroll";
            table.parentNode.insertBefore(wrapper, table);
            wrapper.appendChild(table);
        }

        wrapper.setAttribute("tabindex", "0");
        wrapper.setAttribute("role", "region");
        wrapper.setAttribute("aria-label", "横スクロール可能なデータ表");
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
