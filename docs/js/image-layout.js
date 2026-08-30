(function () {
    var knownDimensions = {
        "/PSNOVA/img/logo.png": { width: 660, height: 121 },
        "/PSNOVA/img/gigantes/gigantes.jpg": { width: 1000, height: 540 }
    };
    var eagerPaths = {
        "/PSNOVA/img/logo.png": true,
        "/PSNOVA/img/gigantes/gigantes.jpg": true
    };
    var weaponIcons = {
        "ソード": "/PSNOVA/img/weapon/sword.png",
        "パルチザン": "/PSNOVA/img/weapon/partizan.png",
        "ダブルセイバー": "/PSNOVA/img/weapon/dsaber.png",
        "ナックル": "/PSNOVA/img/weapon/knuckle.png",
        "アサルトライフル": "/PSNOVA/img/weapon/rifle.png",
        "ツインマシンガン": "/PSNOVA/img/weapon/tmachineg.png",
        "ロッド": "/PSNOVA/img/weapon/rod.png",
        "タリス": "/PSNOVA/img/weapon/thalys.png",
        "ウォンド": "/PSNOVA/img/weapon/wand.png",
        "ヘイロウ": "/PSNOVA/img/weapon/halo.png",
        "パイル": "/PSNOVA/img/weapon/pile.png"
    };
    var classIcons = {
        "ハンター": "/PSNOVA/img/job/hunter.png",
        "レンジャー": "/PSNOVA/img/job/ranger.png",
        "フォース": "/PSNOVA/img/job/force.png",
        "バスター": "/PSNOVA/img/job/buster.png"
    };

    function isInternalPage() {
        return /\/PSNOVA\/pages\/[^/]+\.html$/.test(window.location.pathname);
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

    function isInternalScreenshot(image, pathname) {
        return isInternalPage() && pathname && /\.jpe?g$/i.test(pathname) && image.closest && image.closest("#main");
    }

    function applyImageHints(image) {
        if (!image || !image.getAttribute) {
            return;
        }
        var pathname = getPathname(image);
        if (!pathname) {
            return;
        }

        if (isInternalScreenshot(image, pathname)) {
            image.remove();
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

        if (!eagerPaths[pathname] && !image.hasAttribute("loading")) {
            image.setAttribute("loading", "lazy");
        }
    }

    function removeInternalScreenshots() {
        if (!isInternalPage()) {
            return;
        }
        var main = document.getElementById("main");
        if (!main) {
            return;
        }
        Array.prototype.slice.call(main.querySelectorAll("img")).forEach(function (image) {
            var pathname = getPathname(image);
            if (pathname && /\.jpe?g$/i.test(pathname)) {
                image.remove();
            }
        });
    }

    function decorateSectionIcons() {
        if (!isInternalPage()) {
            return;
        }
        var main = document.getElementById("main");
        if (!main) {
            return;
        }

        Array.prototype.slice.call(main.querySelectorAll("details > summary")).forEach(function (summary) {
            var label = summary.textContent.trim();
            var icon = weaponIcons[label];
            if (icon) {
                summary.classList.add("native-icon-heading");
                summary.style.setProperty("--native-icon", 'url("' + icon + '")');
            }
        });

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
        removeInternalScreenshots();
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
