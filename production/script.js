const menuBtn = document.getElementById('headerMenu');
const firstSection = document.getElementById('firstSection');

menuBtn.addEventListener('click', (e) => {
    firstSection.classList.toggle('open')
});