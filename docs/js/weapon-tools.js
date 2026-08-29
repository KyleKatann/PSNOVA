(function () {
    function normalizeText(value) {
        return (value || "").normalize("NFKC").toLowerCase().trim();
    }

    function initWeaponSearch() {
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
            if (!table) {
                return;
            }

            var rows = Array.prototype.slice.call(table.querySelectorAll("tr"), 1);
            rows.forEach(function (row) {
                var firstCell = row.cells && row.cells[0];
                if (!firstCell) {
                    return;
                }
                records.push({
                    row: row,
                    details: details,
                    name: normalizeText(firstCell.textContent)
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
            '</div>'
        ].join("");

        detailsSections[0].parentNode.insertBefore(toolbar, detailsSections[0]);

        var input = document.getElementById("weapon-search");
        var count = document.getElementById("weapon-search-count");

        function applySearch() {
            var query = normalizeText(input.value);
            var matches = 0;
            var visibleBySection = new Map();

            records.forEach(function (record) {
                var visible = !query || record.name.indexOf(query) !== -1;
                record.row.hidden = !visible;
                if (visible) {
                    matches += 1;
                    visibleBySection.set(record.details, (visibleBySection.get(record.details) || 0) + 1);
                }
            });

            if (query) {
                detailsSections.forEach(function (details) {
                    if (visibleBySection.get(details)) {
                        details.open = true;
                    }
                });
            }

            count.textContent = matches + " / " + records.length + " 件";
        }

        input.addEventListener("input", applySearch);
        applySearch();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initWeaponSearch, { once: true });
    } else {
        initWeaponSearch();
    }
})();
