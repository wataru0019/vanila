// スムーズスクロール
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// コンタクトフォームの処理
document.getElementById('contact-form').addEventListener('submit', function(e) {
    e.preventDefault();
    alert('お問い合わせありがとうございます。\nこれはデモなので送信されません。');
}); 