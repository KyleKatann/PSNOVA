(function loadPageTools(){
    var path = window.location.pathname;
    var isWeaponPage = /\/pages\/weapon(?:\.html|\/[^/]+\.html)$/.test(path);
    var isGigantesPage = /\/pages\/gigantes\.html$/.test(path);

    if (!isWeaponPage && !isGigantesPage) {
        return;
    }

    if (!document.querySelector('link[data-psnova-page-style="true"]')) {
        var stylesheet = document.createElement("link");
        stylesheet.rel = "stylesheet";
        stylesheet.href = "/PSNOVA/css/page.css";
        stylesheet.setAttribute("data-psnova-page-style", "true");
        document.head.appendChild(stylesheet);
    }
})();

(function () {
    var knownDimensions = {
        "/PSNOVA/img/logo.png": { width: 660, height: 121 }
    };
    var classIcons = {
        "ハンター": "/PSNOVA/img/job/hunter.png",
        "レンジャー": "/PSNOVA/img/job/ranger.png",
        "フォース": "/PSNOVA/img/job/force.png",
        "バスター": "/PSNOVA/img/job/buster.png"
    };

    function isInternalPage() {
        return /\/PSNOVA\/pages\/.+\.html$/.test(window.location.pathname);
    }

    if (isInternalPage() && document.documentElement) {
        document.documentElement.classList.add("internal-page");
    }

    function getPathname(image) {
        var rawSrc = image && image.getAttribute ? image.getAttribute("src") : null;
        if (!rawSrc) {
            return null;
        }
        try {
            return new URL(rawSrc, window.location.href).pathname;
        } catch (error) {
            return null;
        }
    }

    function applyImageHints(image) {
        if (!image || !image.getAttribute) {
            return;
        }
        var pathname = getPathname(image);
        if (!pathname) {
            return;
        }

        var dimensions = knownDimensions[pathname];
        if (dimensions) {
            if (!image.hasAttribute("width")) {
                image.setAttribute("width", String(dimensions.width));
            }
            if (!image.hasAttribute("height")) {
                image.setAttribute("height", String(dimensions.height));
            }
        }
    }

    function decorateSectionIcons() {
        if (!isInternalPage()) {
            return;
        }
        var main = document.getElementById("main");
        if (!main) {
            return;
        }

        Array.prototype.slice.call(main.querySelectorAll("h3")).forEach(function (heading) {
            var label = heading.textContent.trim();
            var icon = classIcons[label];
            if (icon) {
                heading.classList.add("native-icon-heading");
                heading.style.setProperty("--native-icon", 'url("' + icon + '")');
            }
        });
    }

    function applyExistingImages() {
        Array.prototype.slice.call(document.images || []).forEach(applyImageHints);
    }

    function finalizeMedia() {
        applyExistingImages();
        decorateSectionIcons();
    }

    var observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            Array.prototype.slice.call(mutation.addedNodes || []).forEach(function (node) {
                if (node.nodeType !== 1) {
                    return;
                }
                if (node.tagName === "IMG") {
                    applyImageHints(node);
                }
                if (node.querySelectorAll) {
                    Array.prototype.slice.call(node.querySelectorAll("img")).forEach(applyImageHints);
                }
            });
        });
    });

    if (document.documentElement) {
        observer.observe(document.documentElement, { childList: true, subtree: true });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", function () {
            finalizeMedia();
            observer.disconnect();
        }, { once: true });
    } else {
        finalizeMedia();
        observer.disconnect();
    }
})();

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

    var tableRegionLabelCounter = 0;

    function ensureLabelSourceId(element) {
        if (element.id) return element.id;

        var id;
        do {
            tableRegionLabelCounter += 1;
            id = "psnova-table-region-label-" + tableRegionLabelCounter;
        } while (document.getElementById(id));

        element.id = id;
        return id;
    }

    function findTableRegionLabelSource(table, wrapper) {
        if (table.caption && table.caption.textContent.trim()) {
            return table.caption;
        }

        var details = table.closest("details");
        if (details) {
            var summary = details.querySelector(":scope > summary");
            if (summary && summary.textContent.trim()) {
                return summary;
            }
        }

        var scope = table.closest("section") || document.getElementById("main");
        if (!scope) return null;

        var headings = scope.querySelectorAll("h2, h3, h4, h5, h6");
        var candidate = null;

        Array.prototype.forEach.call(headings, function (heading) {
            if (
                heading.textContent.trim() &&
                (heading.compareDocumentPosition(wrapper) & Node.DOCUMENT_POSITION_FOLLOWING)
            ) {
                candidate = heading;
            }
        });

        return candidate;
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

        wrapper.style.touchAction = "pan-x pan-y pinch-zoom";
        wrapper.setAttribute("tabindex", "0");
        wrapper.setAttribute("role", "region");

        var labelSource = findTableRegionLabelSource(table, wrapper);
        if (labelSource) {
            wrapper.setAttribute("aria-labelledby", ensureLabelSourceId(labelSource));
            wrapper.removeAttribute("aria-label");
        } else {
            wrapper.removeAttribute("aria-labelledby");
            wrapper.setAttribute("aria-label", "データ表");
        }
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

(function () {
    var banners = [
        '<a href="https://hb.afl.rakuten.co.jp/hsc/56f69858.0bc36ca9.161c2dce.b25f77a4/?link_type=pict&ut=eyJwYWdlIjoic2hvcCIsInR5cGUiOiJwaWN0IiwiY29sIjoxLCJjYXQiOiI1OCIsImJhbiI6MzIzMDk1MCwiYW1wIjpmYWxzZX0%3D" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;"><img src="https://hbb.afl.rakuten.co.jp/hsb/56f69858.0bc36ca9.161c2dce.b25f77a4/?me_id=1&me_adv_id=3230950&t=pict" border="0" style="margin:2px" alt="" title=""></a>',
        '<a href="https://hb.afl.rakuten.co.jp/hsc/56f6981d.83e8392f.161c2dce.b25f77a4/?link_type=pict&ut=eyJwYWdlIjoic2hvcCIsInR5cGUiOiJwaWN0IiwiY29sIjoxLCJjYXQiOiI0NCIsImJhbiI6Mjc5NDg1OCwiYW1wIjpmYWxzZX0%3D" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;"><img src="https://hbb.afl.rakuten.co.jp/hsb/56f6981d.83e8392f.161c2dce.b25f77a4/?me_id=1&me_adv_id=2794858&t=pict" border="0" style="margin:2px" alt="" title=""></a>',
        '<a href="https://hb.afl.rakuten.co.jp/hsc/56f699f4.e077cc17.161c2dce.b25f77a4/?link_type=pict&ut=eyJwYWdlIjoic2hvcCIsInR5cGUiOiJwaWN0IiwiY29sIjoxLCJjYXQiOiI5NSIsImJhbiI6MjA1MTk0MiwiYW1wIjpmYWxzZX0%3D" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;"><img src="https://hbb.afl.rakuten.co.jp/hsb/56f699f4.e077cc17.161c2dce.b25f77a4/?me_id=1&me_adv_id=2051942&t=pict" border="0" style="margin:2px" alt="" title=""></a>',
        '<a href="https://hb.afl.rakuten.co.jp/hsc/301b0604.e2433fa0.161c2dce.b25f77a4/?link_type=pict&ut=eyJwYWdlIjoic2hvcCIsInR5cGUiOiJwaWN0IiwiY29sIjoxLCJjYXQiOiI4MCIsImJhbiI6NDYzNjIsImFtcCI6ZmFsc2V9" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;"><img src="https://hbb.afl.rakuten.co.jp/hsb/301b0604.e2433fa0.161c2dce.b25f77a4/?me_id=1&me_adv_id=46362&t=pict" border="0" style="margin:2px" alt="" title=""></a>',
        '<a href="https://hb.afl.rakuten.co.jp/hsc/56f69d54.b499076e.161c2dce.b25f77a4/?link_type=pict&ut=eyJwYWdlIjoic2hvcCIsInR5cGUiOiJwaWN0IiwiY29sIjoxLCJjYXQiOiIxNCIsImJhbiI6Mzg0OTQ1LCJhbXAiOmZhbHNlfQ%3D%3D" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;"><img src="https://hbb.afl.rakuten.co.jp/hsb/56f69d54.b499076e.161c2dce.b25f77a4/?me_id=1&me_adv_id=384945&t=pict" border="0" style="margin:2px" alt="" title=""></a>',
        '<a href="https://hb.afl.rakuten.co.jp/hsc/56f69e04.e1b4b2a6.161c2dce.b25f77a4/?link_type=pict&ut=eyJwYWdlIjoic2hvcCIsInR5cGUiOiJwaWN0IiwiY29sIjoxLCJjYXQiOiI1IiwiYmFuIjozMjgyMDEzLCJhbXAiOmZhbHNlfQ%3D%3D" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;"><img src="https://hbb.afl.rakuten.co.jp/hsb/56f69e04.e1b4b2a6.161c2dce.b25f77a4/?me_id=1&me_adv_id=3282013&t=pict" border="0" style="margin:2px" alt="" title=""></a>'
    ];
    var products = [
        {
            href: "https://hb.afl.rakuten.co.jp/ichiba/57711f3b.456cbfab.57711f3c.3d9dd6e2/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fbookoffonline%2F0017284923%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D",
            image: "https://hbb.afl.rakuten.co.jp/hgb/57711f3b.456cbfab.57711f3c.3d9dd6e2/?me_id=1275488&item_id=13724931&pc=https%3A%2F%2Fthumbnail.image.rakuten.co.jp%2F%400_mall%2Fbookoffonline%2Fcabinet%2F1139%2F0017284923l.jpg%3F_ex%3D240x240&s=240x240&t=picttext",
            title: "ドラマCD『PHANTASY STAR NOVA』",
            price: "605円（税込、送料別）"
        },
        {
            href: "https://hb.afl.rakuten.co.jp/ichiba/57711f3d.d5733f35.57711f3e.71e23dfd/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Frenet3%2F0012072621%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D",
            image: "https://hbb.afl.rakuten.co.jp/hgb/57711f3d.d5733f35.57711f3e.71e23dfd/?me_id=1312593&item_id=10524822&pc=https%3A%2F%2Fthumbnail.image.rakuten.co.jp%2F%400_mall%2Frenet3%2Fcabinet%2F09%2F00044%2F0012072621.jpg%3F_ex%3D240x240&s=240x240&t=picttext",
            title: "PSVITA ファンタシースターノヴァ",
            price: "880円（税込、送料別）"
        },
        {
            href: "https://hb.afl.rakuten.co.jp/ichiba/57711f57.d0585281.57711f58.b4d205d6/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Frenet20%2Fr0012072621%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D",
            image: "https://hbb.afl.rakuten.co.jp/hgb/57711f57.d0585281.57711f58.b4d205d6/?me_id=1378792&item_id=10292447&pc=https%3A%2F%2Fthumbnail.image.rakuten.co.jp%2F%400_mall%2Frenet20%2Fcabinet%2Fitem_photo%2F001207%2F2%2F0012072621.jpg%3F_ex%3D240x240&s=240x240&t=picttext",
            title: "PSVITA ファンタシースターノヴァ",
            price: "980円（税込、送料無料）"
        },
        {
            href: "https://hb.afl.rakuten.co.jp/ichiba/57711f3b.456cbfab.57711f3c.3d9dd6e2/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fbookoffonline%2F0017303925%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D",
            image: "https://hbb.afl.rakuten.co.jp/hgb/57711f3b.456cbfab.57711f3c.3d9dd6e2/?me_id=1275488&item_id=13749466&pc=https%3A%2F%2Fthumbnail.image.rakuten.co.jp%2F%400_mall%2Fbookoffonline%2Fcabinet%2F1149%2F0017303925l.jpg%3F_ex%3D240x240&s=240x240&t=picttext",
            title: "ファンタシースターノヴァ パーフェクトバイブル",
            price: "1,089円（税込、送料別）"
        },
        {
            href: "https://hb.afl.rakuten.co.jp/ichiba/57711f69.98403100.57711f6a.e96bb110/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fkaitoriouji%2F260910sk170204%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D",
            image: "https://hbb.afl.rakuten.co.jp/hgb/57711f69.98403100.57711f6a.e96bb110/?me_id=1383704&item_id=28970777&pc=https%3A%2F%2Fthumbnail.image.rakuten.co.jp%2F%400_mall%2Fkaitoriouji%2Fcabinet%2F202101121129%2Fb00m6p7zvy.jpg%3F_ex%3D240x240&s=240x240&t=picttext",
            title: "ファンタシースターノヴァ",
            price: "1,133円（税込、送料別）"
        },
        {
            href: "https://hb.afl.rakuten.co.jp/ichiba/57711f6b.3e0c5d49.57711f6c.295c1f1f/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fkaitoriheroes%2F19137889%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D",
            image: "https://hbb.afl.rakuten.co.jp/hgb/57711f6b.3e0c5d49.57711f6c.295c1f1f/?me_id=1309599&item_id=10032568&pc=https%3A%2F%2Fthumbnail.image.rakuten.co.jp%2F%400_mall%2Fkaitoriheroes%2Fcabinet%2Fkaitoriheroes2023%2F23110800102.jpg%3F_ex%3D240x240&s=240x240&t=picttext",
            title: "DS ファンタシースター ZERO（箱説付き）",
            price: "1,320円（税込、送料別）"
        },
        {
            href: "https://hb.afl.rakuten.co.jp/ichiba/57711f71.024bda9e.57711f72.cf7e0881/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Frakutenkobo-ebooks%2F095e1b96f8ba33a595a637641fc85404%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D",
            image: "https://hbb.afl.rakuten.co.jp/hgb/57711f71.024bda9e.57711f72.cf7e0881/?me_id=1278256&item_id=13872762&pc=https%3A%2F%2Fthumbnail.image.rakuten.co.jp%2F%400_mall%2Frakutenkobo-ebooks%2Fcabinet%2F8964%2F2000002608964.jpg%3F_ex%3D240x240&s=240x240&t=picttext",
            title: "ファンタシースター ノヴァ ガイドブック【電子書籍】",
            price: "1,320円"
        },
        {
            href: "https://hb.afl.rakuten.co.jp/ichiba/57711f57.d0585281.57711f58.b4d205d6/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Frenet20%2Fr0011260872%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D",
            image: "https://hbb.afl.rakuten.co.jp/hgb/57711f57.d0585281.57711f58.b4d205d6/?me_id=1378792&item_id=10294876&pc=https%3A%2F%2Fthumbnail.image.rakuten.co.jp%2F%400_mall%2Frenet20%2Fcabinet%2Fitem_photo%2F001126%2F0%2F0011260872.jpg%3F_ex%3D240x240&s=240x240&t=picttext",
            title: "PSP ファンタシースターポータブル2 インフィニティ",
            price: "980円（税込、送料無料）"
        },
        {
            href: "https://hb.afl.rakuten.co.jp/ichiba/57711f57.d0585281.57711f58.b4d205d6/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Frenet20%2Fr0010765698%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D",
            image: "https://hbb.afl.rakuten.co.jp/hgb/57711f57.d0585281.57711f58.b4d205d6/?me_id=1378792&item_id=10294216&pc=https%3A%2F%2Fthumbnail.image.rakuten.co.jp%2F%400_mall%2Frenet20%2Fcabinet%2Fitem_photo%2F001076%2F5%2F0010765698.jpg%3F_ex%3D240x240&s=240x240&t=picttext",
            title: "NDS ファンタシースターZERO",
            price: "870円（税込、送料無料）"
        },
        {
            href: "https://hb.afl.rakuten.co.jp/ichiba/57711fd5.95c1a3ae.57711fd6.8be6f912/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fmediaworldkaitoriworld%2F10401037001%2F&link_type=picttext&ut=eyJwYWdlIjoiaXRlbSIsInR5cGUiOiJwaWN0dGV4dCIsInNpemUiOiIyNDB4MjQwIiwibmFtIjoxLCJuYW1wIjoicmlnaHQiLCJjb20iOjEsImNvbXAiOiJkb3duIiwicHJpY2UiOjEsImJvciI6MSwiY29sIjoxLCJiYnRuIjoxLCJwcm9kIjowLCJhbXAiOmZhbHNlfQ%3D%3D",
            image: "https://hbb.afl.rakuten.co.jp/hgb/57711fd5.95c1a3ae.57711fd6.8be6f912/?me_id=1333404&item_id=10155622&pc=https%3A%2F%2Fthumbnail.image.rakuten.co.jp%2F%400_mall%2Fmediaworldkaitoriworld%2Fcabinet%2F1040%2F1%2Fcg10401037.jpg%3F_ex%3D240x240&s=240x240&t=picttext",
            title: "PS2 SEGA AGES 2500 PHANTASY STAR generation:1 限定版",
            price: "3,579円（税込、送料別）"
        }
    ];
    var rakutenWidgetDocument = [
        '<!doctype html><html lang="ja"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<style>html,body{margin:0;padding:0;background:transparent;}body{overflow:hidden;text-align:center;}<\/style>',
        '</head><body>',
        '<script type="text/javascript">rakuten_design="slide";rakuten_affiliateId="1684437a.b247fdb8.1684437b.b272d4f6";rakuten_items="ranking";rakuten_genreId="566382";rakuten_size="728x200";rakuten_target="_blank";rakuten_theme="gray";rakuten_border="off";rakuten_auto_mode="on";rakuten_genre_title="off";rakuten_recommend="on";rakuten_ts="1789147399706";<\/script>',
        '<script type="text/javascript" src="https://xml.affiliate.rakuten.co.jp/widget/js/rakuten_widget.js?20230106"><\/script>',
        '</body></html>'
    ].join("");

    function pathHash(value) {
        var hash = 0;
        for (var i = 0; i < value.length; i += 1) {
            hash = ((hash << 5) - hash + value.charCodeAt(i)) | 0;
        }
        return Math.abs(hash);
    }

    function pickBanners(count) {
        var day = Math.floor(Date.now() / 86400000);
        var start = (day + pathHash(window.location.pathname)) % banners.length;
        var selected = [];

        for (var i = 0; i < count; i += 1) {
            selected.push(banners[(start + i) % banners.length]);
        }

        return selected;
    }

    function renderBannerItems() {
        return pickBanners(2).map(function (markup, index) {
            var accessibleMarkup = markup.replace(
                "<a ",
                '<a aria-label="楽天市場の商品広告 ' +
                    (index + 1) +
                    '（外部サイト）" '
            );

            return '<div class="affiliate-banner-item">' +
                accessibleMarkup +
                '</div>';
        }).join("");
    }

    function createCampaignBanner() {
        var banner = document.createElement("aside");
        banner.className = "affiliate-banner affiliate-campaign-banner";
        banner.setAttribute("aria-label", "楽天市場のPR");
        banner.innerHTML = '<span class="affiliate-disclosure">PR</span><div class="affiliate-banner-body">' + renderBannerItems() + "</div>";
        return banner;
    }

    function createRakutenWidget() {
        var widget = document.createElement("aside");
        widget.className = "affiliate-banner rakuten-motion-widget";
        widget.setAttribute("aria-label", "楽天市場の商品ランキングPR");
        widget.innerHTML = '<span class="affiliate-disclosure">PR</span>';

        var frame = document.createElement("iframe");
        frame.className = "rakuten-motion-widget-frame";
        frame.title = "楽天市場の商品ランキング広告";
        frame.setAttribute("width", "728");
        frame.setAttribute("height", "200");
        frame.setAttribute("sandbox", "allow-scripts allow-forms allow-popups allow-popups-to-escape-sandbox");
        frame.style.display = "block";
        frame.style.width = "100%";
        frame.style.maxWidth = "728px";
        frame.style.height = "200px";
        frame.style.margin = "0 auto";
        frame.style.border = "0";
        frame.srcdoc = rakutenWidgetDocument;
        widget.appendChild(frame);

        return widget;
    }

    function createProductCard(product) {
        var card = document.createElement("article");
        card.className = "affiliate-product-card";
        card.style.display = "grid";
        card.style.gridTemplateColumns = "112px minmax(0, 1fr)";
        card.style.gap = "12px";
        card.style.flex = "0 0 min(420px, 82vw)";
        card.style.minHeight = "160px";
        card.style.padding = "10px";
        card.style.border = "1px solid var(--border)";
        card.style.borderRadius = "8px";
        card.style.background = "var(--surface)";
        card.style.scrollSnapAlign = "start";
        card.style.boxSizing = "border-box";

        var imageLink = document.createElement("a");
        imageLink.href = product.href;
        imageLink.target = "_blank";
        imageLink.rel = "nofollow sponsored noopener";
        imageLink.setAttribute("aria-label", product.title + "（楽天市場）");
        imageLink.style.display = "flex";
        imageLink.style.alignItems = "center";
        imageLink.style.justifyContent = "center";

        var image = document.createElement("img");
        image.src = product.image;
        image.alt = product.title;
        image.loading = "lazy";
        image.style.display = "block";
        image.style.width = "100%";
        image.style.maxWidth = "112px";
        image.style.height = "112px";
        image.style.objectFit = "contain";
        image.style.margin = "0";
        imageLink.appendChild(image);

        var body = document.createElement("div");
        body.style.display = "flex";
        body.style.flexDirection = "column";
        body.style.minWidth = "0";

        var title = document.createElement("a");
        title.href = product.href;
        title.target = "_blank";
        title.rel = "nofollow sponsored noopener";
        title.textContent = product.title;
        title.style.color = "var(--text-strong)";
        title.style.fontSize = "13px";
        title.style.fontWeight = "700";
        title.style.lineHeight = "1.45";
        title.style.textDecoration = "none";

        var price = document.createElement("div");
        price.textContent = "価格：" + product.price;
        price.style.marginTop = "8px";
        price.style.fontSize = "12px";
        price.style.lineHeight = "1.4";
        price.style.color = "var(--text)";

        var date = document.createElement("div");
        date.textContent = "2026/9/12時点";
        date.style.marginTop = "2px";
        date.style.fontSize = "10px";
        date.style.color = "var(--text-muted)";

        var purchase = document.createElement("a");
        purchase.href = product.href;
        purchase.target = "_blank";
        purchase.rel = "nofollow sponsored noopener";
        purchase.textContent = "楽天で購入";
        purchase.style.display = "inline-flex";
        purchase.style.alignItems = "center";
        purchase.style.justifyContent = "center";
        purchase.style.width = "max-content";
        purchase.style.marginTop = "auto";
        purchase.style.padding = "6px 14px";
        purchase.style.borderRadius = "999px";
        purchase.style.background = "#bf0000";
        purchase.style.color = "#fff";
        purchase.style.fontSize = "12px";
        purchase.style.fontWeight = "700";
        purchase.style.lineHeight = "1.2";
        purchase.style.textDecoration = "none";

        body.appendChild(title);
        body.appendChild(price);
        body.appendChild(date);
        body.appendChild(purchase);
        card.appendChild(imageLink);
        card.appendChild(body);
        return card;
    }

    function createProductCarousel() {
        var carousel = document.createElement("aside");
        carousel.className = "affiliate-banner affiliate-product-carousel";
        carousel.setAttribute("aria-label", "PSNOVA関連商品のPR");

        var header = document.createElement("div");
        header.style.display = "flex";
        header.style.alignItems = "center";
        header.style.justifyContent = "space-between";
        header.style.gap = "12px";
        header.style.marginBottom = "8px";

        var heading = document.createElement("div");
        heading.style.display = "flex";
        heading.style.alignItems = "center";
        heading.style.gap = "8px";
        heading.innerHTML = '<span class="affiliate-disclosure" style="margin:0">PR</span><strong style="font-size:13px;color:var(--text-strong)">PSNOVA関連商品</strong>';

        var controls = document.createElement("div");
        controls.style.display = "flex";
        controls.style.gap = "6px";

        var previous = document.createElement("button");
        previous.type = "button";
        previous.textContent = "‹";
        previous.setAttribute("aria-label", "前の商品へ");

        var next = document.createElement("button");
        next.type = "button";
        next.textContent = "›";
        next.setAttribute("aria-label", "次の商品へ");

        [previous, next].forEach(function (button) {
            button.style.width = "34px";
            button.style.height = "30px";
            button.style.padding = "0";
            button.style.border = "1px solid var(--border)";
            button.style.borderRadius = "6px";
            button.style.background = "var(--surface)";
            button.style.color = "var(--text-strong)";
            button.style.fontSize = "22px";
            button.style.lineHeight = "1";
            button.style.cursor = "pointer";
        });

        controls.appendChild(previous);
        controls.appendChild(next);
        header.appendChild(heading);
        header.appendChild(controls);

        var viewport = document.createElement("div");
        viewport.className = "affiliate-product-carousel-viewport";
        viewport.setAttribute("role", "region");
        viewport.setAttribute("aria-label", "楽天市場のPSNOVA関連商品一覧");
        viewport.setAttribute("tabindex", "0");
        viewport.style.width = "100%";
        viewport.style.overflowX = "hidden";
        viewport.style.overflowY = "hidden";
        viewport.style.touchAction = "pan-y";

        var track = document.createElement("div");
        track.className = "affiliate-product-carousel-track";
        track.style.display = "flex";
        track.style.gap = "12px";
        track.style.width = "max-content";
        track.style.minWidth = "100%";
        track.style.padding = "0 1px";

        var cards = products.map(function (product) {
            var card = createProductCard(product);
            track.appendChild(card);
            return card;
        });
        var duplicateCards = products.map(function (product) {
            var card = createProductCard(product);
            card.setAttribute("aria-hidden", "true");
            Array.prototype.slice.call(card.querySelectorAll("a")).forEach(function (link) {
                link.setAttribute("tabindex", "-1");
            });
            track.appendChild(card);
            return card;
        });

        viewport.appendChild(track);
        carousel.appendChild(header);
        carousel.appendChild(viewport);

        var animationFrame = null;
        var lastFrame = null;
        var pixelsPerSecond = 34;

        function loopWidth() {
            if (!duplicateCards.length) return 0;
            return duplicateCards[0].offsetLeft - track.offsetLeft;
        }

        function normalizeScrollPosition() {
            var width = loopWidth();
            if (!width) return;
            while (viewport.scrollLeft >= width) {
                viewport.scrollLeft -= width;
            }
            while (viewport.scrollLeft < 0) {
                viewport.scrollLeft += width;
            }
        }

        function stepSize() {
            if (!cards.length) return 0;
            return cards[0].getBoundingClientRect().width + 12;
        }

        function autoScroll(timestamp) {
            if (lastFrame === null) {
                lastFrame = timestamp;
            } else {
                var elapsed = Math.min(timestamp - lastFrame, 64);
                lastFrame = timestamp;
                viewport.scrollLeft += pixelsPerSecond * elapsed / 1000;
                normalizeScrollPosition();
            }
            animationFrame = window.requestAnimationFrame(autoScroll);
        }

        function startAutoScroll() {
            if (animationFrame !== null) return;
            lastFrame = null;
            animationFrame = window.requestAnimationFrame(autoScroll);
        }

        function stopAutoScroll() {
            if (animationFrame === null) return;
            window.cancelAnimationFrame(animationFrame);
            animationFrame = null;
            lastFrame = null;
        }

        previous.addEventListener("click", function () {
            var width = loopWidth();
            var step = stepSize();
            if (width && viewport.scrollLeft < step) {
                viewport.scrollLeft += width;
            }
            viewport.scrollLeft -= step;
            normalizeScrollPosition();
        });

        next.addEventListener("click", function () {
            viewport.scrollLeft += stepSize();
            normalizeScrollPosition();
        });

        document.addEventListener("visibilitychange", function () {
            if (document.hidden) {
                stopAutoScroll();
            } else {
                startAutoScroll();
            }
        });

        startAutoScroll();
        return carousel;
    }


    function insertAtPrimaryPosition(section, node) {
        var children = Array.prototype.slice.call(section.children || []);
        var firstParagraph = children.find(function (child) {
            return child.tagName && child.tagName.toLowerCase() === "p";
        });

        if (firstParagraph && firstParagraph.nextSibling) {
            section.insertBefore(node, firstParagraph.nextSibling);
        } else if (firstParagraph) {
            section.appendChild(node);
        } else {
            var firstData = section.querySelector("details, table");
            if (firstData) {
                section.insertBefore(node, firstData);
            } else {
                section.appendChild(node);
            }
        }
    }

    function insertBanner() {
        if (document.querySelector(".affiliate-banner")) return;
        if (/\/(copyright|issue)\.html$/.test(window.location.pathname)) return;

        var main = document.getElementById("main");
        if (!main) return;

        var section = main.querySelector("section") || main;
        insertAtPrimaryPosition(section, createProductCarousel());
        main.appendChild(createRakutenWidget());
        main.appendChild(createCampaignBanner());
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", insertBanner, { once: true });
    } else {
        insertBanner();
    }
})();
