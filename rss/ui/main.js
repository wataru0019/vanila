fetch("http://127.0.0.1:8000/")
    .then(response => {
        if(!response.ok) {
            throw new Error("Network response was not ok");
        }
        console.log(response);
        return response.json();
    })
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error("Error:", error);
    })