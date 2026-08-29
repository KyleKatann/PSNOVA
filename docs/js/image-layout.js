(function () {
    var knownDimensions = {
        "/PSNOVA/img/logo.png": { width: 660, height: 121 },
        "/PSNOVA/img/title.jpg": { width: 1000, height: 540 }
    };
    var eagerPaths = {
        "/PSNOVA/img/logo.png": true,
        "/PSNOVA/img/title.jpg": true
    };

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

        if (!eagerPaths[pathname] && !image.hasAttribute("loading")) {
            image.setAttribute("loading", "lazy");
        }
    }

    function applyExistingImages() {
        Array.prototype.slice.call(document.images || []).forEach(applyImageHints);
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
            applyExistingImages();
            observer.disconnect();
        }, { once: true });
    } else {
        applyExistingImages();
        observer.disconnect();
    }
})();
