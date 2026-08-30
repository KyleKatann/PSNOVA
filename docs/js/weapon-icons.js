(function () {
    var iconByLabel = {
        "ソード": "sword.png",
        "パルチザン": "partizan.png",
        "ダブルセイバー": "dsaber.png",
        "ナックル": "knuckle.png",
        "アサルトライフル": "rifle.png",
        "ツインマシンガン": "tmachineg.png",
        "ロッド": "rod.png",
        "タリス": "thalys.png",
        "ウォンド": "wand.png",
        "ヘイロウ": "halo.png",
        "パイル": "pile.png"
    };

    function addStyles() {
        if (document.getElementById("psnova-weapon-icon-styles")) return;
        var style = document.createElement("style");
        style.id = "psnova-weapon-icon-styles";
        style.textContent = [
            "#main details > summary.weapon-summary-with-icon{display:flex;align-items:center;gap:9px;}",
            "#main details > summary .weapon-type-icon{width:24px;height:24px;object-fit:contain;image-rendering:auto;flex:0 0 24px;}",
            "#main.weapon-detail-page h2 .weapon-type-icon{width:30px;height:30px;object-fit:contain;vertical-align:-5px;margin-right:8px;}",
            "#main details table thead th:first-child::before{content:'◆';margin-right:5px;color:var(--accent);font-size:.76em;}",
            "#main details table thead th:nth-child(2)::before{content:'★';margin-right:4px;color:var(--accent);font-size:.78em;}",
            "#main details table thead th:nth-child(6)::before{content:'Lv';display:inline-grid;place-items:center;min-width:20px;height:17px;margin-right:5px;padding:0 3px;border:1px solid var(--border-strong);border-radius:3px;color:var(--text-muted);background:var(--surface);font-size:9px;line-height:1;vertical-align:1px;}",
            "@media screen and (max-width:480px){#main details > summary .weapon-type-icon{width:21px;height:21px;flex-basis:21px;}}"
        ].join("");
        document.head.appendChild(style);
    }

    function iconFor(label) {
        var filename = iconByLabel[label];
        if (!filename) return null;
        var img = document.createElement("img");
        img.className = "weapon-type-icon";
        img.src = "/PSNOVA/img/weapon/" + filename;
        img.alt = "";
        img.width = 24;
        img.height = 24;
        img.loading = "lazy";
        img.decoding = "async";
        return img;
    }

    function decorate() {
        if (!/\/PSNOVA\/pages\/weapon(?:\/[^/]+)?\.html$/.test(window.location.pathname)) return;
        var main = document.getElementById("main");
        if (!main) return;
        addStyles();

        Array.prototype.slice.call(main.querySelectorAll("details > summary")).forEach(function (summary) {
            if (summary.querySelector(".weapon-type-icon")) return;
            var label = summary.textContent.trim();
            var icon = iconFor(label);
            if (!icon) return;
            summary.classList.add("weapon-summary-with-icon");
            summary.insertBefore(icon, summary.firstChild);
        });

        var heading = main.querySelector("h2");
        if (main.classList.contains("weapon-detail-page") && heading && !heading.querySelector(".weapon-type-icon")) {
            var label = heading.textContent.replace(/\s*武器データ\s*$/, "").trim();
            var icon = iconFor(label);
            if (icon) {
                icon.width = 30;
                icon.height = 30;
                heading.insertBefore(icon, heading.firstChild);
            }
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", function () {
            window.setTimeout(decorate, 0);
        }, { once: true });
    } else {
        window.setTimeout(decorate, 0);
    }
})();
