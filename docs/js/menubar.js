function menu(){
if(document.readyState!="complete"){
var html =`


<!--PC用（801px以上端末）メニュー-->
<nav id="menubar">
<ul>
<li><a href="https://kylekatann.github.io/PSNOVA/index.html">ホーム<span>HOME</span></a></li>
<li><a href="company.html">会社概要<span>COMPANY</span></a></li>
<li><a href="service.html">サービス紹介<span>SERVICE</span></a></li>
<li><a href="recruit.html">採用情報<span>RECRUIT</span></a></li>
<li><a href="faq.html">よく頂く質問<span>FAQ</span></a></li>
<li><a href="contact.html">お問い合わせ<span>CONTACT</span></a></li>
<li><a href="contact.html">お問い合わせ<span>CONTACT</span></a></li>
</ul>
</nav>

<!--小さな端末用（800px以下端末）メニュー-->
<nav id="menubar-s">
<ul>
<li><a href="https://kylekatann.github.io/PSNOVA/index.html">ホーム</a></li>
<li><a href="company.html">会社概要</a></li>
<li><a href="service.html">サービス紹介</a></li>
<li><a href="recruit.html">採用情報</a></li>
<li><a href="faq.html">よく頂く質問</a></li>
<li><a href="contact.html">お問い合わせ</a></li>
</ul>
</nav>

`;
document.write(html);
}else{
    var span = document.createElement("span");
    span.innerHTML = "hoge!!";
    document.body.appendChild("span");
    }
}

