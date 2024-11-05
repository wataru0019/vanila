const target = document.getElementById('target');

document.addEventListener('DOMContentLoaded', async function(e) {
    console.log(e);
    try {
        const response = await fetch('http://127.0.0.1:8000/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log(data);

        const target = document.getElementById('target'); // Ensure you have an element with id 'target'
        for (let i = 0; i < data.length; i++) {
            const item = document.createElement('div');
            item.textContent = `${data[i]}`;
            target.appendChild(item);
        }
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
});