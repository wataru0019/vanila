fetch("http://127.0.0.1:8000/")
    .then(response => {
        if(!response.ok) {
            throw new Error("Network response was not ok");
        }
        console.log(response);
        return response.json();
    })
    .then(data => {
        const target = document.getElementById("article_point")
        for(let i = 0; i < data.length; i++) {
            target.insertAdjacentHTML('afterbegin',
                `<div class='article'>
                    <h3 class="article-title">${data[i]['title']}</h3>
                    <a href="${data[i]['link']}">記事リンク</a>
                </div>`)
        }
        console.log(data);
    })
    .catch(error => {
        console.error("Error:", error);
    })