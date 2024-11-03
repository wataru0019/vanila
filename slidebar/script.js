const slidebar = document.getElementById('slidebar');
const menu = document.getElementById('menu');
const main = document.getElementById('main');
const content = document.getElementById('content');
const inputForm = document.getElementById('inputForm');
const slidebarList = document.getElementById('slidebarList');

menu.addEventListener('click', function(e){
    console.log(e);
    slidebar.classList.toggle('slidebar-open')
    main.classList.toggle('open')
    content.classList.toggle('open')
})

inputForm.addEventListener('submit', function(e){
    e.preventDefault();
    const input = document.getElementById('sideMenu');
    const formData = new FormData(inputForm);
    const newItem = document.createElement('li');
    newItem.textContent = input.value
    slidebarList.appendChild(newItem);
    input.value = '';
})