(function () {
    var banners = [
        '<a href="https://hb.afl.rakuten.co.jp/hsc/56f69858.0bc36ca9.161c2dce.b25f77a4/?link_type=pict&ut=eyJwYWdlIjoic2hvcCIsInR5cGUiOiJwaWN0IiwiY29sIjoxLCJjYXQiOiI1OCIsImJhbiI6MzIzMDk1MCwiYW1wIjpmYWxzZX0%3D" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;"><img src="https://hbb.afl.rakuten.co.jp/hsb/56f69858.0bc36ca9.161c2dce.b25f77a4/?me_id=1&me_adv_id=3230950&t=pict" border="0" style="margin:2px" alt="" title=""></a>',
        '<a href="https://hb.afl.rakuten.co.jp/hsc/56f6981d.83e8392f.161c2dce.b25f77a4/?link_type=pict&ut=eyJwYWdlIjoic2hvcCIsInR5cGUiOiJwaWN0IiwiY29sIjoxLCJjYXQiOiI0NCIsImJhbiI6Mjc5NDg1OCwiYW1wIjpmYWxzZX0%3D" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;"><img src="https://hbb.afl.rakuten.co.jp/hsb/56f6981d.83e8392f.161c2dce.b25f77a4/?me_id=1&me_adv_id=2794858&t=pict" border="0" style="margin:2px" alt="" title=""></a>',
        '<a href="https://hb.afl.rakuten.co.jp/hsc/56f699f4.e077cc17.161c2dce.b25f77a4/?link_type=pict&ut=eyJwYWdlIjoic2hvcCIsInR5cGUiOiJwaWN0IiwiY29sIjoxLCJjYXQiOiI5NSIsImJhbiI6MjA1MTk0MiwiYW1wIjpmYWxzZX0%3D" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;"><img src="https://hbb.afl.rakuten.co.jp/hsb/56f699f4.e077cc17.161c2dce.b25f77a4/?me_id=1&me_adv_id=2051942&t=pict" border="0" style="margin:2px" alt="" title=""></a>',
        '<a href="https://hb.afl.rakuten.co.jp/hsc/301b0604.e2433fa0.161c2dce.b25f77a4/?link_type=pict&ut=eyJwYWdlIjoic2hvcCIsInR5cGUiOiJwaWN0IiwiY29sIjoxLCJjYXQiOiI4MCIsImJhbiI6NDYzNjIsImFtcCI6ZmFsc2V9" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;"><img src="https://hbb.afl.rakuten.co.jp/hsb/301b0604.e2433fa0.161c2dce.b25f77a4/?me_id=1&me_adv_id=46362&t=pict" border="0" style="margin:2px" alt="" title=""></a>',
        '<a href="https://hb.afl.rakuten.co.jp/hsc/56f69d54.b499076e.161c2dce.b25f77a4/?link_type=pict&ut=eyJwYWdlIjoic2hvcCIsInR5cGUiOiJwaWN0IiwiY29sIjoxLCJjYXQiOiIxNCIsImJhbiI6Mzg0OTQ1LCJhbXAiOmZhbHNlfQ%3D%3D" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;"><img src="https://hbb.afl.rakuten.co.jp/hsb/56f69d54.b499076e.161c2dce.b25f77a4/?me_id=1&me_adv_id=384945&t=pict" border="0" style="margin:2px" alt="" title=""></a>',
        '<a href="https://hb.afl.rakuten.co.jp/hsc/56f69e04.e1b4b2a6.161c2dce.b25f77a4/?link_type=pict&ut=eyJwYWdlIjoic2hvcCIsInR5cGUiOiJwaWN0IiwiY29sIjoxLCJjYXQiOiI1IiwiYmFuIjozMjgyMDEzLCJhbXAiOmZhbHNlfQ%3D%3D" target="_blank" rel="nofollow sponsored noopener" style="word-wrap:break-word;"><img src="https://hbb.afl.rakuten.co.jp/hsb/56f69e04.e1b4b2a6.161c2dce.b25f77a4/?me_id=1&me_adv_id=3282013&t=pict" border="0" style="margin:2px" alt="" title=""></a>'
    ];

    function pathHash(value) {
        var hash = 0;
        for (var i = 0; i < value.length; i += 1) {
            hash = ((hash << 5) - hash + value.charCodeAt(i)) | 0;
        }
        return Math.abs(hash);
    }

    function pickBanner() {
        var day = Math.floor(Date.now() / 86400000);
        return banners[(day + pathHash(window.location.pathname)) % banners.length];
    }

    function insertBanner() {
        if (document.querySelector(".affiliate-banner")) return;
        if (/\/(copyright|issue)\.html$/.test(window.location.pathname)) return;

        var main = document.getElementById("main");
        if (!main) return;

        var section = main.querySelector("section") || main;
        var banner = document.createElement("aside");
        banner.className = "affiliate-banner";
        banner.setAttribute("aria-label", "楽天市場のPR");
        banner.innerHTML = '<span class="affiliate-disclosure">PR</span><div class="affiliate-banner-body">' + pickBanner() + "</div>";

        var children = Array.prototype.slice.call(section.children || []);
        var firstParagraph = children.find(function (child) {
            return child.tagName && child.tagName.toLowerCase() === "p";
        });

        if (firstParagraph && firstParagraph.nextSibling) {
            section.insertBefore(banner, firstParagraph.nextSibling);
        } else if (firstParagraph) {
            section.appendChild(banner);
        } else {
            var firstData = section.querySelector("details, table");
            if (firstData) {
                section.insertBefore(banner, firstData);
            } else {
                section.appendChild(banner);
            }
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", insertBanner, { once: true });
    } else {
        insertBanner();
    }
})();
