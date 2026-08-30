(function () {
    function removeLegacyPresentation(element, attributes, styleProperties) {
        attributes.forEach(function (attribute) {
            element.removeAttribute(attribute);
        });

        styleProperties.forEach(function (property) {
            element.style.removeProperty(property);
        });

        if (element.hasAttribute("style") && !element.getAttribute("style").trim()) {
            element.removeAttribute("style");
        }
    }

    function stripLegacyTablePresentation(table) {
        removeLegacyPresentation(
            table,
            ["border", "cellpadding", "cellspacing", "bgcolor", "align", "valign"],
            ["border-collapse", "background-color", "background", "border"]
        );

        Array.prototype.slice.call(table.querySelectorAll("th, td")).forEach(function (cell) {
            removeLegacyPresentation(
                cell,
                ["bgcolor", "align", "valign"],
                ["background-color", "background", "border", "text-align", "vertical-align"]
            );
        });
    }

    function replaceElementTag(element, tagName) {
        if (!element || element.tagName.toLowerCase() === tagName.toLowerCase()) {
            return element;
        }

        var replacement = document.createElement(tagName);
        Array.prototype.slice.call(element.attributes || []).forEach(function (attribute) {
            replacement.setAttribute(attribute.name, attribute.value);
        });
        while (element.firstChild) {
            replacement.appendChild(element.firstChild);
        }
        element.parentNode.replaceChild(replacement, element);
        return replacement;
    }

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

    function normalizedLabel(value) {
        return String(value || "").replace(/\s+/g, "").toLowerCase();
    }

    function stripTrailingQuestionMark(cell) {
        if (!cell) {
            return;
        }

        var node = cell;
        while (node && node.lastChild) {
            node = node.lastChild;
            if (node.nodeType === 3) {
                node.nodeValue = node.nodeValue.replace(/[?？]+\s*$/, "");
                return;
            }
        }
    }

    function hasLegacyHeaderStyling(cell) {
        if (!cell) {
            return false;
        }

        if (cell.hasAttribute("bgcolor")) {
            return true;
        }

        return !!(cell.style && (cell.style.backgroundColor || cell.style.background));
    }

    function isLargeDataTable(table) {
        var rows = Array.prototype.slice.call(table.rows || []);
        if (rows.length < 2) {
            return false;
        }

        if (table.closest("details")) {
            return true;
        }

        var headerCells = rows[0] ? Array.prototype.slice.call(rows[0].cells || []) : [];
        if (headerCells.length >= 3) {
            var legacyHeaderCount = headerCells.filter(hasLegacyHeaderStyling).length;
            if (legacyHeaderCount >= Math.max(2, Math.ceil(headerCells.length / 2))) {
                return true;
            }
        }

        if (rows.length < 4 || !rows[0] || rows[0].cells.length < 3) {
            return false;
        }

        var headerCount = headerCells.filter(function (cell) {
            return cell.tagName && cell.tagName.toLowerCase() === "th";
        }).length;
        return headerCount >= Math.max(2, Math.ceil(headerCells.length / 2));
    }

    function decorateDataTable(table) {
        if (!table.tHead || !table.tHead.rows.length) {
            return;
        }

        var headerCells = Array.prototype.slice.call(table.tHead.rows[0].cells || []);
        var indexes = {};
        headerCells.forEach(function (cell, index) {
            var label = normalizedLabel(cell.textContent);
            if (label === "レアリティ") indexes.rarity = index;
            if (label === "打撃" || label === "打撃力") indexes.melee = index;
            if (label === "射撃" || label === "射撃力") indexes.ranged = index;
            if (label === "法撃" || label === "法撃力") indexes.tech = index;
            if (label === "ショップlv" || label === "shoplv") indexes.shop = index;
        });

        Array.prototype.slice.call(table.tBodies || []).forEach(function (tbody) {
            Array.prototype.slice.call(tbody.rows || []).forEach(function (row) {
                var cells = row.cells || [];

                stripTrailingQuestionMark(cells[0]);

                if (indexes.rarity !== undefined && cells[indexes.rarity]) {
                    var rarity = numericValue(cells[indexes.rarity].textContent);
                    cells[indexes.rarity].classList.add("rarity-cell");
                    if (rarity !== null) {
                        cells[indexes.rarity].setAttribute("data-rarity", String(rarity));
                        cells[indexes.rarity].setAttribute("data-rarity-band", rarityBand(rarity));
                        cells[indexes.rarity].setAttribute("aria-label", "レアリティ " + rarity);
                    }
                }

                [
                    ["melee", "weapon-stat-melee"],
                    ["ranged", "weapon-stat-ranged"],
                    ["tech", "weapon-stat-tech"]
                ].forEach(function (definition) {
                    var index = indexes[definition[0]];
                    if (index === undefined || !cells[index]) return;
                    var cell = cells[index];
                    cell.classList.add("weapon-stat-cell", definition[1]);
                    if (cell.textContent.trim()) {
                        cell.classList.add("has-value");
                    } else {
                        cell.classList.add("is-empty");
                    }
                });

                if (indexes.shop !== undefined && cells[indexes.shop]) {
                    cells[indexes.shop].classList.add("shop-level-cell");
                }
            });
        });
    }

    function normalizeDataTable(table) {
        if (table.dataset.psnovaSemantic === "true") {
            decorateDataTable(table);
            return;
        }

        stripLegacyTablePresentation(table);

        var rows = Array.prototype.slice.call(table.rows || []);
        if (rows.length < 2) {
            return;
        }

        var headerRow = rows[0];
        Array.prototype.slice.call(headerRow.cells || []).forEach(function (cell) {
            var headerCell = replaceElementTag(cell, "th");
            headerCell.setAttribute("scope", "col");
        });

        var thead = table.tHead || table.createTHead();
        thead.appendChild(headerRow);

        Array.prototype.slice.call(table.tBodies || []).forEach(function (tbody) {
            Array.prototype.slice.call(tbody.rows || []).forEach(function (row) {
                Array.prototype.slice.call(row.cells || []).forEach(function (cell) {
                    replaceElementTag(cell, "td");
                });
            });
        });

        table.dataset.psnovaSemantic = "true";
        decorateDataTable(table);
    }

    function ensureScrollableTable(table) {
        if (!table || !table.parentNode) {
            return;
        }

        if (table.parentElement && table.parentElement.classList.contains("table-scroll")) {
            return;
        }

        var wrapper = document.createElement("div");
        wrapper.className = "table-scroll";
        wrapper.setAttribute("role", "region");
        wrapper.setAttribute("tabindex", "0");
        wrapper.setAttribute("aria-label", "表を横スクロール");
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
    }

    function initTableSemantics() {
        var main = document.getElementById("main");
        if (!main) {
            return;
        }

        var tables = Array.prototype.slice.call(main.querySelectorAll("table"));
        tables.filter(isLargeDataTable).forEach(normalizeDataTable);
        tables.forEach(ensureScrollableTable);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initTableSemantics, { once: true });
    } else {
        initTableSemantics();
    }
})();