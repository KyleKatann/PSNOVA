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

    function headerRowFor(table) {
        if (table.tHead && table.tHead.rows.length) return table.tHead.rows[0];
        return table.rows.length ? table.rows[0] : null;
    }

    function identifyingColumnIndex(headerRow) {
        if (!headerRow || !headerRow.cells.length) return 0;

        var logicalColumn = 0;
        var fallback = 0;
        for (var i = 0; i < headerRow.cells.length; i += 1) {
            var cell = headerRow.cells[i];
            var label = normalizedLabel(cell.textContent);
            var span = Math.max(Number(cell.colSpan) || 1, 1);
            if (label === "名前" || label === "名称" || /名$/.test(label)) {
                return logicalColumn;
            }
            logicalColumn += span;
        }
        return fallback;
    }

    function decorateMobileKeyColumn(table) {
        var headerRow = headerRowFor(table);
        if (!headerRow) return;

        Array.prototype.slice.call(table.querySelectorAll(".mobile-key-cell")).forEach(function (cell) {
            cell.classList.remove("mobile-key-cell");
        });

        var targetColumn = identifyingColumnIndex(headerRow);
        table.setAttribute("data-mobile-key-column", String(targetColumn));

        var headerLogicalColumn = 0;
        Array.prototype.forEach.call(headerRow.cells, function (cell) {
            var span = Math.max(Number(cell.colSpan) || 1, 1);
            if (targetColumn >= headerLogicalColumn && targetColumn < headerLogicalColumn + span) {
                cell.classList.add("mobile-key-cell");
            }
            headerLogicalColumn += span;
        });

        var rows = Array.prototype.slice.call(table.rows).filter(function (row) {
            return row !== headerRow && (!table.tHead || !row.closest("thead"));
        });
        var activeRowspans = [];

        rows.forEach(function (row) {
            var occupied = activeRowspans.slice();
            var nextRowspans = activeRowspans.map(function (remaining) {
                return Math.max((remaining || 0) - 1, 0);
            });
            var logicalColumn = 0;

            Array.prototype.forEach.call(row.cells, function (cell) {
                while ((occupied[logicalColumn] || 0) > 0) logicalColumn += 1;

                var colSpan = Math.max(Number(cell.colSpan) || 1, 1);
                var rowSpan = Math.max(Number(cell.rowSpan) || 1, 1);
                var cellEnd = logicalColumn + colSpan;

                if (targetColumn >= logicalColumn && targetColumn < cellEnd) {
                    cell.classList.add("mobile-key-cell");
                }

                if (rowSpan > 1) {
                    for (var column = logicalColumn; column < cellEnd; column += 1) {
                        nextRowspans[column] = Math.max(nextRowspans[column] || 0, rowSpan - 1);
                    }
                }
                logicalColumn = cellEnd;
            });

            activeRowspans = nextRowspans;
        });
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
            decorateMobileKeyColumn(table);
            ensureScrollableTable(table);
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initTableEnhancements, { once: true });
    } else {
        initTableEnhancements();
    }
})();
