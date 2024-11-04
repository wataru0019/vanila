const menuBtn = document.getElementById('headerMenu');
const firstSection = document.getElementById('firstSection');

menuBtn.addEventListener('click', (e) => {
    firstSection.classList.toggle('open')
});

document.addEventListener('DOMContentLoaded', (e) => {
    fetch("http://127.0.0.1:8000/")
    .then(response => {
        if(!response.ok) {
            throw new Error("Network response was not ok");
        }
        console.log(response);
        return response.json();
    })
    .then(data => {
        const target = document.getElementById("target")
        for(let i = 0; i < data.length; i++) {
            target.insertAdjacentHTML('afterbegin',
                `<div class='article'>
                    <h3 class="article-title">${data[i]['title']}</h3>
                    <p class="article-summary">${data[i]['summary']}</p>
                    <a class="atricle-link" href="${data[i]['link']}">read more...</a>
                </div>`
            )};
        console.log(data);
    })
    .catch(error => {
        console.error("Error:", error);
    })
})
