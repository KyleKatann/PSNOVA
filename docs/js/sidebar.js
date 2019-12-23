function side(){
if(document.readyState!="complete"){
var html =`


<div id="sub">
<nav>
<h2>Contents</h2>
<ul class="submenu">
<li><a href="company.html">会社概要</a></li>
<li><a href="service.html">サービス紹介</a></li>
<li><a href="recruit.html">採用情報</a></li>
<li><a href="faq.html">よく頂く質問</a></li>
<li><a href="link.html">リンク</a></li>
<li><a href="contact.html">お問い合わせ</a></li>
</ul>
</nav>

<aside>
<!--
<a href="recruit.html"><img src="images/banner1.jpg" alt="採用情報" class="pc"></a>
<a href="recruit.html"><img src="images/banner1_sh.jpg" alt="採用情報" class="sh"></a>  
-->
</aside>
</div>


`;
document.write(html);
}else{
    var span = document.createElement("span");
    span.innerHTML = "hoge!!";
    document.body.appendChild("span");
    }
}
