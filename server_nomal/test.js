document.getElementById('fetch-data').addEventListener('click', () => {
  fetch('http://localhost:8000')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json(); // Use json() to parse the JSON response
    })
    .then(data => {
      console.log(data);
      const container = document.getElementById('data-container');
      container.innerHTML = ''; // Clear previous data
      data.forEach(item => {
        const div = document.createElement('div');
        div.textContent = `Name: ${item.name}, Age: ${item.age}, City: ${item.city}`;
        container.appendChild(div);
      });
    })
    .catch(error => console.error('Error:', error));
});