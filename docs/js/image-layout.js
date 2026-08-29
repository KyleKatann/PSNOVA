(function () {
    var knownDimensions = {
        "/PSNOVA/img/logo.png": { width: 660, height: 121 },
        "/PSNOVA/img/title.jpg": { width: 1000, height: 540 }
    };

    function applyDimensions(image) {
        if (!image || !image.getAttribute) {
            return;
        }
        var rawSrc = image.getAttribute("src");
        if (!rawSrc) {
            return;
        }
        var pathname;
        try {
            pathname = new URL(rawSrc, window.location.href).pathname;
        } catch (error) {
            return;
        }
        var dimensions = knownDimensions[pathname];
        if (!dimensions) {
            return;
        }
        if (!image.hasAttribute("width")) {
            image.setAttribute("width", String(dimensions.width));
        }
        if (!image.hasAttribute("height")) {
            image.setAttribute("height", String(dimensions.height));
        }
    }

    function applyExistingImages() {
        Array.prototype.slice.call(document.images || []).forEach(applyDimensions);
    }

    var observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            Array.prototype.slice.call(mutation.addedNodes || []).forEach(function (node) {
                if (node.nodeType !== 1) {
                    return;
                }
                if (node.tagName === "IMG") {
                    applyDimensions(node);
                }
                if (node.querySelectorAll) {
                    Array.prototype.slice.call(node.querySelectorAll("img")).forEach(applyDimensions);
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
