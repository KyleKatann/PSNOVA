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

    function normalizeDataTable(table) {
        if (table.dataset.psnovaSemantic === "true") {
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
    }

    function initTableSemantics() {
        var main = document.getElementById("main");
        if (!main) {
            return;
        }
        Array.prototype.slice.call(main.querySelectorAll("details table")).forEach(normalizeDataTable);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initTableSemantics, { once: true });
    } else {
        initTableSemantics();
    }
})();
