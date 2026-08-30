(function () {
    function numericValue(value) {
        var match = String(value || "").replace(/,/g, "").match(/-?\d+(?:\.\d+)?/);
        return match ? Number(match[0]) : null;
    }

    function rarityBand(value) {
        if (value === null) return "";
        if (value <= 3) return "blue";
        if (value <= 6) return "green";
        if (value <= 9) return "red";
        if (value <= 12) return "orange";
        return "violet";
    }

    function decorateStatCell(cell, className) {
        if (!cell) return;
        cell.classList.add("weapon-stat-cell", className);
        if (cell.textContent.trim()) {
            cell.classList.add("has-value");
            cell.classList.remove("is-empty");
        } else {
            cell.classList.add("is-empty");
            cell.classList.remove("has-value");
        }
    }

    function decorateRow(row) {
        var cells = row.cells;
        if (!cells || cells.length < 6) return;

        var rarity = numericValue(cells[1].textContent);
        if (rarity !== null) {
            cells[1].classList.add("rarity-cell");
            cells[1].setAttribute("data-rarity", String(rarity));
            cells[1].setAttribute("data-rarity-band", rarityBand(rarity));
        }

        decorateStatCell(cells[2], "weapon-stat-melee");
        decorateStatCell(cells[3], "weapon-stat-ranged");
        decorateStatCell(cells[4], "weapon-stat-tech");

        cells[5].classList.add("shop-level-cell");
    }

    function initWeaponTableStyle() {
        if (!/\/pages\/weapon\.html$/.test(window.location.pathname)) return;

        Array.prototype.slice.call(document.querySelectorAll("#main details table")).forEach(function (table) {
            var rows = Array.prototype.slice.call(table.rows || []);
            rows.slice(1).forEach(decorateRow);
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initWeaponTableStyle, { once: true });
    } else {
        initWeaponTableStyle();
    }
})();
