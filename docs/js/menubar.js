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
        '<a href="https://hb.afl.rakuten.co.jp/hsc/56f69d54.b499076e.161c2dce.b25f77a4/?link_type=pict&ut=eyJwYWdlIjoic2hvcCIsInR5cGUiOiJwaWN0IiwiY29sIjoxLCJjYXQiOiI1NCIsImJhbiI6Mzg0OTQ1LCJhbXAiOmZhbHNlfQ%3D%3D" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;"><img src="https://hbb.afl.rakuten.co.jp/hsb/56f69d54.b499076e.161c2dce.b25f77a4/?me_id=1&me_adv_id=384945&t=pict" border="0" style="margin:2px" alt="" title=""></a>',
        '<a href="https://hb.afl.rakuten.co.jp/hsc/56f69e04.e1b4b2a6.161c2dce.b25f77a4/?link_type=pict&ut=eyJwYWdlIjoic2hvcCIsInR5cGUiOiJwaWN0IiwiY29sIjoxLCJjYXQiOiI1IiwiYmFuIjozMjgyMDEzLCJhbXAiOmZhbHNlfQ%3D%3D" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;"><img src="https://hbb.afl.rakuten.co.jp/hsb/56f69e04.e1b4b2a6.161c2dce.b25f77a4/?me_id=1&me_adv_id=3282013&t=pict" border="0" style="margin:2px" alt="" title=""></a>'
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
        insertAtPrimaryPosition(section, createRakutenWidget());
        main.appendChild(createCampaignBanner());
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", insertBanner, { once: true });
    } else {
        insertBanner();
    }
})();